"""
Camera Diagnostic Test Script

Run this script to test if OpenCV can access your webcam directly:
    python test_camera.py
"""

import cv2
import sys
import time


def test_camera():
    print("=" * 60)
    print("  GESTURE CONTROL SYSTEM — CAMERA DIAGNOSTIC TEST")
    print("=" * 60)
    print(f"Python Version : {sys.version}")
    print(f"OpenCV Version : {cv2.__version__}")
    print("-" * 60)
    
    backends = [
        ("DirectShow (CAP_DSHOW)", cv2.CAP_DSHOW),
        ("Default (CAP_ANY)", cv2.CAP_ANY),
        ("MSMF (CAP_MSMF)", getattr(cv2, "CAP_MSMF", cv2.CAP_ANY))
    ]
    
    found_camera = False
    
    for idx in range(3):
        print(f"\n[Testing Camera Index {idx}]")
        for name, backend in backends:
            print(f"  Attempting {name} backend...")
            cap = cv2.VideoCapture(idx, backend) if backend != cv2.CAP_ANY else cv2.VideoCapture(idx)
            
            if not cap.isOpened():
                print(f"  |-- Failed to open index {idx} with {name}")
                cap.release()
                continue
            
            ret, frame = cap.read()
            if ret and frame is not None:
                h, w, _ = frame.shape
                print(f"  +-- SUCCESS! Opened Camera Index {idx} ({w}x{h}) using {name}")
                found_camera = True
                
                print("\nOpening test window for 3 seconds...")
                start_time = time.time()
                while time.time() - start_time < 3.0:
                    r, f = cap.read()
                    if r and f is not None:
                        cv2.putText(f, f"Camera {idx} OK - Press Q to close", (20, 40),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.imshow("Camera Diagnostic Test", f)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                cv2.destroyAllWindows()
                cap.release()
                print("\n[DIAGNOSTIC PASSED] Your webcam is working perfectly!")
                return True
            else:
                print(f"  |-- Opened index {idx} but frame capture returned empty.")
            
            cap.release()
    
    if not found_camera:
        print("\n" + "!" * 60)
        print("[DIAGNOSTIC FAILED] Could not open any camera.")
        print("Possible causes:")
        print(" 1. Camera is in use by another app (Zoom, MS Teams, Browser, Windows Camera app).")
        print(" 2. Camera privacy settings in Windows (Settings -> Privacy -> Camera -> Allow desktop apps).")
        print(" 3. Physical camera toggle switch or sliding cover is closed.")
        print("!" * 60)
        return False

if __name__ == "__main__":
    test_camera()
