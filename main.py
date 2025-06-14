import cv2
import mediapipe as mp
import time
import numpy as np
import pyautogui
import ctypes
import math

# Initialize MediaPipe for hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.9, min_tracking_confidence=0.9)
mp_draw = mp.solutions.drawing_utils

# Define virtual keyboard layout and properties
keys = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
        'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
        'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Backspace', ' ']

key_size = (55, 60)
start_x, start_y = 20, 100
gap = 10
key_rects = []

# Set key positions
for i, key in enumerate(keys):
    x = start_x + (i % 10) * (key_size[0] + gap)
    y = start_y + (i // 10) * (key_size[1] + gap)
    key_rects.append(((x, y), (x + key_size[0], y + key_size[1])))


# Function to set window always on top
def set_always_on_top(window_name):
    hwnd = ctypes.windll.user32.FindWindowW(None, window_name)
    if hwnd:
        ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)


# Function to calculate Euclidean distance
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# Function to apply Gaussian blur for smoothing
def smooth_landmarks(landmarks, alpha=0.3):
    smoothed = []
    if not landmarks:
        return smoothed
    smoothed.append(np.array(landmarks[0]))  # Initialize with the first landmark
    for i in range(1, len(landmarks)):
        smoothed.append(smoothed[-1] * (1 - alpha) + np.array(landmarks[i]) * alpha)
    return smoothed


# Function to find the closest key index based on hand direction
def get_closest_key_index(finger_tip, key_rects, threshold=100):
    min_distance = float('inf')
    closest_key_index = None
    for i, rect in enumerate(key_rects):
        key_center_x = (rect[0][0] + rect[1][0]) // 2
        key_center_y = (rect[0][1] + rect[1][1]) // 2
        distance = euclidean_distance((finger_tip[0], finger_tip[1]), (key_center_x, key_center_y))
        if distance < min_distance and distance < threshold:
            min_distance = distance
            closest_key_index = i
    return closest_key_index


# Main function
cap = cv2.VideoCapture(0)
selected_key = None
key_start_times = {}
key_pressed_flags = {key: False for key in keys}
typed_text = ""
hand_in_frame = False

# Create a separate window for the virtual keyboard
keyboard_window = np.zeros((600, 1000, 3), dtype=np.uint8)
cv2.namedWindow("Virtual Keyboard", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Virtual Keyboard", 1000, 600)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Draw the virtual keyboard on a separate window
    keyboard_window[:] = (255, 255, 255)
    if hand_in_frame:
        for i, rect in enumerate(key_rects):
            color = (0, 0, 0)
            if selected_key == keys[i]:
                color = (0, 255, 0)
                # Draw a pulsating effect
                current_time = time.time()
                pulse_radius = int(10 * math.sin(current_time * 5) ** 2)
                cv2.circle(keyboard_window, (rect[0][0] + key_size[0] // 2, rect[0][1] + key_size[1] // 2),
                           pulse_radius, (0, 255, 0), -1)

                if keys[i] not in key_start_times:
                    key_start_times[keys[i]] = current_time
                filled_portion = int((current_time - key_start_times[keys[i]]) / 1.2 * (rect[1][0] - rect[0][0]))
                cv2.rectangle(keyboard_window, (rect[0][0], rect[1][1]), (rect[0][0] + filled_portion, rect[1][1] + 5),
                              (0, 255, 0), -1)
                if current_time - key_start_times[keys[i]] > 1.2:
                    if not key_pressed_flags[keys[i]]:
                        if keys[i] == 'Backspace':
                            typed_text = typed_text[:-1]
                        else:
                            pyautogui.press(keys[i])
                            typed_text += keys[i]
                        key_pressed_flags[keys[i]] = True
                    key_start_times[keys[i]] = current_time
            else:
                if selected_key == keys[i]:
                    selected_key = None
                    key_pressed_flags[keys[i]] = False
                    key_start_times.pop(keys[i], None)
            cv2.rectangle(keyboard_window, rect[0], rect[1], color, 2)
            cv2.putText(keyboard_window, keys[i], (rect[0][0] + 30, rect[0][1] + 65), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        color, 2)
    else:
        selected_key = None
        key_start_times.clear()
        key_pressed_flags = {key: False for key in keys}

    # Draw typed text box
    text_box_rect = (20, 20, 960, 60)
    cv2.rectangle(keyboard_window, (text_box_rect[0], text_box_rect[1]),
                  (text_box_rect[0] + text_box_rect[2], text_box_rect[1] + text_box_rect[3]), (0, 0, 0), 2)
    cv2.putText(keyboard_window, typed_text, (text_box_rect[0] + 10, text_box_rect[1] + 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 0), 2)

    # Display the virtual keyboard window
    cv2.imshow("Virtual Keyboard", keyboard_window)

    # Hand detection and gesture recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        hand_in_frame = True
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmark coordinates
            landmarks = [(lm.x * w, lm.y * h) for lm in hand_landmarks.landmark]
            smoothed_landmarks = smooth_landmarks(landmarks)

            # Extract index finger tip coordinates
            index_finger_tip = smoothed_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            finger_x, finger_y = int(index_finger_tip[0]), int(index_finger_tip[1])

            # Find the closest key based on hand direction
            closest_key_index = get_closest_key_index((finger_x, finger_y), key_rects, threshold=150)

            if closest_key_index is not None:
                if selected_key != keys[closest_key_index]:
                    selected_key = keys[closest_key_index]
                    if selected_key in key_start_times:
                        key_start_times[selected_key] = time.time()
                    else:
                        key_start_times[selected_key] = time.time()

                if selected_key in key_start_times:
                    if time.time() - key_start_times[selected_key] > 1.2:
                        if not key_pressed_flags[selected_key]:
                            if selected_key == 'Backspace':
                                typed_text = typed_text[:-1]
                            else:
                                pyautogui.press(selected_key)
                                typed_text += selected_key
                            key_pressed_flags[selected_key] = True
                        key_start_times[selected_key] = time.time()
            else:
                selected_key = None

    else:
        hand_in_frame = False

    cv2.imshow("Camera Feed", frame)

    set_always_on_top("Virtual Keyboard")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
