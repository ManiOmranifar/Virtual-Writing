# ✋ Virtual Hand Gesture Keyboard

A **real-time virtual keyboard** powered by **MediaPipe**, **OpenCV**, and **hand gesture recognition**, allowing users to type using only finger movements captured via webcam. Perfect for **touchless interaction**, **accessibility**, and **futuristic UI experiments**.

---

## 🚀 Features

- 🖐️ Hand tracking with MediaPipe
- 💡 Hover-based key selection using the index finger
- ⌛ Timed activation (~1.2s) to confirm key presses
- 🖼️ Virtual QWERTY keyboard layout
- ⌨️ Supports `Backspace` and `Space`
- 💬 Live typed-text display
- 🔄 Animated pulse feedback on active key
- 📌 Always-on-top keyboard window (Windows only)

---

## 🛠 Requirements

- Python 3.8+
- Windows OS (for always-on-top feature)
- Webcam

### 🔧 Installation

Install required libraries:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

---

## 🧠 How It Works

1. **Camera Feed**: Captures webcam input and flips for mirror view.
2. **Hand Detection**: MediaPipe detects hand landmarks in real time.
3. **Finger Tracking**: Tracks the index fingertip position.
4. **Key Matching**: Finds the closest virtual key using Euclidean distance.
5. **Hold Detection**: If the finger remains over a key > 1.2 seconds → key is pressed.
6. **Feedback**: Pulsating green circle on active key + text box showing input.

---

## 🎮 Controls

| Action              | Gesture / Key              |
|---------------------|----------------------------|
| Select a Key        | Hover index finger          |
| Confirm Key Press   | Hold for 1.2 seconds        |
| Delete a Character  | Hover over `Backspace` key  |
| Insert Space        | Hover over `Space` key      |
| Quit Program        | Press `Q` on keyboard       |

---

## 🖼️ Screenshots

> You can add screenshots below when you test the application.

| Camera Feed | Virtual Keyboard |
|-------------|------------------|
| *(screenshot)* | *(screenshot)* |

---

## 🛠 Customization

- 🔤 **Keyboard Layout**: Modify the `keys` list to change layout.
- 📏 **Key Size & Position**: Adjust `key_size`, `gap`, `start_x`, and `start_y`.
- ⏱️ **Hold Duration**: Change `1.2` seconds to increase/decrease key activation time.
- 🔊 **Add Sound Feedback**: Use `playsound` or `winsound` for audio cues.

---

## ⚠️ Limitations

- Windows only (due to `ctypes.windll`)
- Works best under good lighting conditions
- Currently supports only one hand and index finger

---

## 💡 Future Ideas

- 🧠 Add Shift, Enter, and other keys
- 🗣️ Voice or sound feedback
- 🌐 Cross-platform support
- 🤲 Multi-hand tracking
- 📱 Port to mobile using phone camera

---

## 👨‍💻 Author

**Mani Omranifar**  
AI & Backend Developer  
📧 [maniomranifar@gmail.com](mailto:maniomranifar@gmail.com)

---

## 📄 License

Licensed under the MIT License.  
Free to use, modify, and distribute with proper attribution.

---

## ⭐ Support

If you like this project, consider starring it on GitHub and sharing your feedback!
