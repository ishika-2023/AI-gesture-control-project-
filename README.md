# AI-Based Cross-Platform Gesture Control System Using Computer Vision

A final-year engineering project that transforms hand gestures captured via camera into OS cursor movement and mouse actions (clicks, dragging, scrolling). Supports both **Desktop Mode (Webcam)** and **Mobile Mode (Android/Wi-Fi Remote Controller)** using pure Python.

---

## 🌟 Key Features

- **Mode A — Desktop Gesture Mouse**: Direct real-time computer control using a computer webcam.
- **Mode B — Mobile Gesture Controller**: Control a computer wirelessly using an Android phone's camera over a local Wi-Fi connection.
- **Hand Tracking**: Powered by MediaPipe 21 3D-landmark extraction.
- **6 Built-In Gestures**:
  1. **Cursor Movement**: Index finger extended (`Landmark 8`).
  2. **Left Click**: Thumb + Index pinch (`Landmark 4 ↔ Landmark 8`).
  3. **Right Click**: Thumb + Middle pinch (`Landmark 4 ↔ Landmark 12`).
  4. **Scroll**: Two fingers extended (Index + Middle) with vertical motion tracking.
  5. **Click & Drag**: Sustained Thumb-Index pinch + hand movement.
  6. **Pause / Safety**: Open Palm (all 5 fingers extended).
- **Smooth & Stable**:
  - Exponential Moving Average (EMA) cursor smoothing.
  - Active Camera Region mapping (no extreme hand stretching required).
  - Dead zone filtering for micro-jitter.
  - Debounced click cooldowns via a multi-frame State Machine.
- **GUI & Calibration**:
  - Dark-themed Tkinter GUI with live webcam preview.
  - Step-by-step Interactive Calibration Wizard.
  - Manual Emergency Stop (`ESC` key shortcut + UI button + Open Palm gesture).
  - Pure Python architecture (**No JavaScript / React / Node.js**).

---

## 🏗️ System Architecture

```
[ Webcam / Android Phone Camera ]
               ↓
       [ OpenCV Video Capture ]
               ↓
    [ MediaPipe 21 Hand Tracking ]
               ↓
  [ Landmark Extraction (0-1 Coords) ]
               ↓
      [ Gesture Detector ]
               ↓
   [ Gesture State Machine (Stability & Cooldown) ]
               ↓
  [ Cursor Controller (Active Region, EMA, Deadzone) ]
               ↓
 [ PyAutoGUI / OS Mouse Control ]
```

### Mobile Wi-Fi Extension Architecture
```
[ Phone Camera ] → [ Mobile Gesture Detector ] → [ TCP Client ]
                                                       ↓ (Local Wi-Fi)
[ OS Mouse ] ← [ PyAutoGUI ] ← [ Command Whitelist ] ← [ Python Socket Server ]
```

---

## 📁 Directory Structure

```
gesture_control_project/
│
├── desktop/                  # Desktop application core
│   ├── __init__.py
│   ├── main.py               # Application entry point (GUI / Headless / Test)
│   ├── camera.py             # OpenCV webcam manager & FPS tracker
│   ├── hand_tracker.py       # MediaPipe 21 landmark detector & visualizer
│   ├── gesture_detector.py   # Pure landmark geometric gesture classifier
│   ├── gesture_state.py      # Frame-stability & debouncing state machine
│   ├── cursor_controller.py  # Active region mapping, EMA smoothing, deadzone
│   ├── mouse_controller.py   # PyAutoGUI wrapper with failsafe & emergency stop
│   ├── calibration.py        # Interactive calibration wizard
│   ├── network_server.py     # TCP socket server for mobile controller
│   ├── config.py             # Config schema (JSON persistence)
│   └── ui.py                 # Modern Tkinter dark theme GUI
│
├── mobile/                   # Mobile application
│   ├── __init__.py
│   ├── main.py               # Kivy Android/Desktop entry point
│   └── network_client.py     # TCP socket client with command throttling
│
├── tests/                    # Automated unit tests
│   ├── test_gestures.py      # Landmark gesture classification tests
│   ├── test_coordinates.py   # Coordinate transformation & clamping tests
│   ├── test_smoothing.py     # EMA exponential smoothing tests
│   └── test_network.py       # Network server command whitelist & security tests
│
├── assets/                   # Project icons & screenshots
├── requirements.txt          # Dependencies list
├── PROJECT_DOCUMENTATION.md  # Detailed technical project report
└── README.md                 # System overview and quick start guide
```

---

## 🚀 Quick Start & Installation

### 1. Requirements
Ensure Python 3.9+ is installed on your system.

### 2. Installation
Clone or navigate to the project directory and install dependencies:
```bash
cd gesture_control_project
pip install -r requirements.txt
```

---

## 💻 Running Desktop Mode

### Option 1: Full GUI Mode (Recommended)
```bash
python desktop/main.py
```
- Click **▶ Start Camera** to preview your webcam feed.
- Click **🖐 Start Gesture Control** (or press `F5`) to enable system mouse control.
- Click **🎯 Calibrate** to launch the step-by-step calibration wizard.
- Press `ESC` at any time for **Emergency Stop**.

### Option 2: Headless Mode (OpenCV Window Only)
```bash
python desktop/main.py --headless
```
- Press `SPACE` to toggle gesture control on/off.
- Press `P` to pause control.
- Press `C` to calibrate.
- Press `Q` or `ESC` to quit.

### Option 3: Camera & Landmark Verification Test
```bash
python desktop/main.py --test
```
Displays camera preview, MediaPipe hand landmarks, FPS, and raw coordinates without triggering mouse movements.

---

## 📱 Running Mobile Controller Mode

1. **Start Desktop Server**:
   - Open the Desktop GUI (`python desktop/main.py`).
   - In the **Network Server** panel, click **Start Server**.
   - Note the displayed IP (e.g. `192.168.1.50`) and Port (`5050`).

2. **Launch Mobile App**:
   ```bash
   python mobile/main.py
   ```
   - Enter the Desktop IP address and Port.
   - Click **Connect**.
   - Click **▶ START** to begin tracking gestures using the mobile camera and controlling the desktop cursor over Wi-Fi.

---

## 🖐 Gesture Quick Reference

| Gesture Name | Hand Pose | Mechanism | Triggered Command |
|--------------|-----------|-----------|-------------------|
| **Cursor Move** | Index finger extended | Index Tip (Lm 8) position | OS Mouse Cursor Move |
| **Left Click** | Thumb + Index Pinch | Lm 4 ↔ Lm 8 distance < threshold | Left Mouse Click |
| **Right Click** | Thumb + Middle Pinch | Lm 4 ↔ Lm 12 distance < threshold | Right Mouse Click |
| **Scroll** | Index + Middle extended | Vertical displacement of fingertips | Mouse Wheel Up / Down |
| **Click & Drag** | Sustained Thumb + Index Pinch | Pinch hold + hand movement | Mouse Down → Move → Up |
| **Pause / Safety**| Open Palm (all 5 fingers) | All 5 fingertip heights above joints | Temporarily disables control |

---

## 🧪 Running Automated Tests

Run the full suite of unit tests for gesture classification, coordinate mapping, smoothing algorithms, and network command verification:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 🛡️ Security & Safety Measures

1. **PyAutoGUI Failsafe**: Moving the cursor manually to any corner of the screen immediately aborts gesture control.
2. **Emergency Stop Shortcut**: Pressing `ESC` instantly disables mouse execution.
3. **Open Palm Safety Gesture**: Raising an open palm immediately halts all mouse movement.
4. **Command Whitelisting**: The network server strictly accepts pre-approved commands (`MOVE`, `LEFT_CLICK`, `RIGHT_CLICK`, `SCROLL_UP`, `SCROLL_DOWN`, `DRAG_START`, `DRAG_END`, `PAUSE`). Any unknown payload is safely rejected.

---

## 📜 License & Academic Usage
Created as a 4th-Year Computer Science / Engineering Final Year Capstone Project demonstrating real-time computer vision, gesture recognition, human-computer interaction (HCI), and network computing in Python.
