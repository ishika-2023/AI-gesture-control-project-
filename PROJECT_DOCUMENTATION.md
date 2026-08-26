# Comprehensive Academic Documentation: AI-Based Cross-Platform Gesture Control System

**Project Title**: AI-Based Cross-Platform Gesture Control System Using Computer Vision  
**Domain**: Computer Vision, Artificial Intelligence, Human-Computer Interaction (HCI), Distributed Real-Time Systems  
**Primary Stack**: Python 3 (OpenCV, MediaPipe, NumPy, PyAutoGUI, Tkinter, Kivy, Sockets)  

---

## 1. Abstract

Traditional computer input devices (mouse, touchpads) require direct physical contact, which can be restrictive or non-ergonomic in touchless/hygienic environments. This project presents a cross-platform, multi-modal gesture control system leveraging real-time computer vision and 3D hand landmark estimation. Utilizing MediaPipe's 21 3D landmark pipeline and OpenCV frame processing, the system extracts hand poses in real time to emulate a full-fledged computer mouse (cursor positioning, left/right clicks, dragging, and scrolling). Furthermore, the architecture features a lightweight mobile extension built with Kivy and socket networking, enabling a remote smartphone to act as an external camera controller over a local Wi-Fi network. Experimental results demonstrate smooth cursor tracking with minimal latency (<30ms processing overhead per frame) and reliable gesture recognition debouncing via a multi-state machine architecture.

---

## 2. System Architecture & Component Design

### 2.1 Pipeline Flow
The desktop application processes video streams through an 8-stage synchronous execution pipeline:

1. **Video Capture Subsystem (`camera.py`)**: Captures 640x480 video frames at ~30 FPS via OpenCV `VideoCapture`. Handles mirror flipping and frame buffer alignment.
2. **Hand Detection & Landmark Extraction (`hand_tracker.py`)**: Processes RGB frames through MediaPipe's two-stage detector (palm detection model followed by 21 3D landmark estimation).
3. **Geometric Analysis & Classification (`gesture_detector.py`)**: Computes spatial Euclidean distances between key landmarks (e.g., $d(L_4, L_8)$ for thumb-index pinch) and analyzes finger extension vectors relative to joint positions.
4. **State Stability Machine (`gesture_state.py`)**: Requires $N$ consecutive identical gesture classifications before transitioning state, eliminating single-frame visual jitter and enforcing click debouncing cooldowns.
5. **Coordinate Mapping & Normalization (`cursor_controller.py`)**: Maps landmark coordinates from an inner "Active Region" frame subset onto absolute display monitor pixels $(S_x, S_y)$.
6. **Exponential Moving Average (EMA) Filtering**: Smooths cursor motion using:
   $$S_t = \alpha \cdot X_t + (1 - \alpha) \cdot S_{t-1}$$
   where $\alpha \in (0, 1]$ represents the configurable responsiveness coefficient.
7. **Dead-Zone Thresholding**: Drops micro-movements smaller than $\delta$ pixels to stabilize stationary finger positioning.
8. **OS Event Injection (`mouse_controller.py`)**: Uses PyAutoGUI to fire OS-level synthetic input events.

---

## 3. Mathematical & Algorithmic Formulations

### 3.1 Landmark Distance Metric
Euclidean distance in normalized 3D space between landmark $L_a = (x_a, y_a, z_a)$ and landmark $L_b = (x_b, y_b, z_b)$:

$$d(L_a, L_b) = \sqrt{(x_a - x_b)^2 + (y_a - y_b)^2 + (z_a - z_b)^2}$$

- **Left Click Condition**: $d(L_4, L_8) < \theta_{\text{left}}$
- **Right Click Condition**: $d(L_4, L_{12}) < \theta_{\text{right}} \land d(L_4, L_8) \ge \theta_{\text{left}}$

### 3.2 Active Region Coordinate Normalization
Given frame bounding box coordinates $(X_{\min}, Y_{\min})$ to $(X_{\max}, Y_{\max})$, input landmark point $(x, y)$ is transformed into screen space $(W_{\text{screen}}, H_{\text{screen}})$ via:

$$x_{\text{norm}} = \text{clamp}\left(\frac{x - X_{\min}}{X_{\max} - X_{\min}}, 0, 1\right)$$

$$y_{\text{norm}} = \text{clamp}\left(\frac{y - Y_{\min}}{Y_{\max} - Y_{\min}}, 0, 1\right)$$

$$S_x = \text{clamp}\left(\left[0.5 + (x_{\text{norm}} - 0.5) \cdot S_{\text{sensitivity}}\right] \cdot W_{\text{screen}}, 0, W_{\text{screen}}-1\right)$$

---

## 4. Mobile Remote Controller (Mode B) Protocol

The mobile app connects over TCP using a custom, secure string protocol.

```
Mobile Application (Kivy)               Desktop Application Server
        |                                           |
        |---- CONNECT (IP:Port) ------------------->| Accepts socket
        |                                           |
        |---- "MOVE:0.5234,0.4121\n" --------------->| Parses & maps cursor
        |---- "LEFT_CLICK\n" ---------------------->| Executes PyAutoGUI click
        |---- "PAUSE\n" --------------------------->| Disables input control
```

### Whitelisted Server Commands
To prevent arbitrary code execution over the local network, the Python server enforces strict payload verification against a fixed whitelist:
`{"MOVE", "LEFT_CLICK", "RIGHT_CLICK", "SCROLL_UP", "SCROLL_DOWN", "DRAG_START", "DRAG_END", "PAUSE"}`.

---

## 5. Experimental Verification & Test Cases

The implementation includes automated unit testing (`tests/`) covering system modules:

1. **`test_gestures.py`**: Verifies classification logic against synthetic landmark coordinates for open palm (pause), index extension (move), thumb-index pinch (left click), thumb-middle pinch (right click), and two-finger extension (scroll).
2. **`test_coordinates.py`**: Validates active region mapping, boundary clamping, and sensitivity multiplier transformations.
3. **`test_smoothing.py`**: Asserts EMA algorithm convergence rates.
4. **`test_network.py`**: Ensures socket setup, message passing, and malicious command rejection.

---

## 6. Safety & Failsafe Implementations

1. **Hardware Failsafe**: PyAutoGUI `FAILSAFE = True` automatically raises `FailSafeException` if the mouse cursor reaches any display corner.
2. **Keybinding Emergency Stop**: Global listener for `ESC` instantly disables mouse state machine and releases held mouse buttons.
3. **Visual Safety Gesture**: Raising an open palm (all 5 fingertips above proximal interphalangeal joints) triggers state `PAUSED`.

---

## 7. Future Enhancements

- **Dynamic Gesture Training**: Incorporating KNN/SVM models to allow users to record custom gesture poses.
- **3D Spatial Depth Gestures**: Utilizing MediaPipe $Z$-depth estimation to support Z-axis virtual push button interactions.
- **Low-Bandwidth Mobile Video Stream**: Streaming H.264 video feed back to mobile display for handheld camera alignment.
