import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import os

model_path = 'hand_landmarker.task'
if not os.path.exists(model_path):
    print("Model file not found!")
    input("Press Enter...")
    exit()

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7
)
detector = vision.HandLandmarker.create_from_options(options)

try:
    dev = AudioUtilities.GetDefaultOutputDevice()
except:
    dev = AudioUtilities.GetSpeakers()

try:
    volctl = dev.EndpointVolume.QueryInterface(IAudioEndpointVolume)
    minv, maxv = volctl.GetVolumeRange()[:2]
except:
    volctl = None
    minv, maxv = -65.25, 0.0

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera error!")
    exit()

prev_dist = 0
smooth = 0.7
last_brightness = -1

print("System Started...")

while True:
    ok, img = cap.read()
    if not ok:
        break

    img = cv2.flip(img, 1)
    h, w = img.shape[:2]

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_image)

    if result.hand_landmarks:
        for i in range(len(result.hand_landmarks)):

            hand = result.hand_landmarks[i]

            
            if result.handedness and len(result.handedness) > i:
                label = result.handedness[i][0].category_name
            else:
                label = "Unknown"

           
            tp = (int(hand[4].x * w), int(hand[4].y * h))
            ip = (int(hand[8].x * w), int(hand[8].y * h))

            cv2.circle(img, tp, 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, ip, 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, tp, ip, (0, 255, 0), 3)

           
            dist = float(np.hypot(ip[0] - tp[0], ip[1] - tp[1]))
            dist = max(30, min(300, dist))

            # smooth
            dist = smooth * prev_dist + (1 - smooth) * dist
            prev_dist = dist

            
            cx = (tp[0] + ip[0]) // 2

            
            if label == "Left" or cx < w // 2:

                if volctl:
                    v = np.interp(dist, [30, 300], [minv, maxv])
                    try:
                        volctl.SetMasterVolumeLevel(v, None)
                    except:
                        pass

                pct = int(np.interp(dist, [30, 300], [0, 100]))

                cv2.putText(img, f"VOL {pct}%", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

           
            else:

                b = int(np.interp(dist, [30, 300], [0, 100]))

                # throttle
                if abs(b - last_brightness) > 2:
                    try:
                        sbc.set_brightness(b)
                        last_brightness = b
                    except:
                        pass

                cv2.putText(img, f"BRT {b}%", (w - 250, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            
            cv2.putText(img, label, (tp[0], tp[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imshow("Hand Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()