import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import os

# ১. মডেল ফাইলের সঠিক পাথ চেক করা
model_path = 'hand_landmarker.task'
if not os.path.exists(model_path):
    print(f"Error: {model_path} ফাইলটি খুঁজে পাওয়া যায়নি!")
    input("Press Enter to exit...")
    exit()

# ২. মিডিয়াপাইপ ডিটেক্টর সেটআপ
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7
)
detector = vision.HandLandmarker.create_from_options(options)

# ৩. অডিও কন্ট্রোল সেটআপ
try:
    dev = AudioUtilities.GetDefaultOutputDevice()
    volctl = dev.EndpointVolume.QueryInterface(IAudioEndpointVolume)
    minv, maxv = volctl.GetVolumeRange()[:2]
except Exception as e:
    print(f"Audio setup error: {e}")
    minv, maxv = -65.25, 0.0 # ডিফল্ট মান যদি এরর দেয়

# ৪. ক্যামেরা ওপেন করা
cap = cv2.VideoCapture(0) # যদি কাজ না করে তবে 1 দিয়ে চেষ্টা করো
if not cap.isOpened():
    print("Error: ক্যামেরা খুঁজে পাওয়া যাচ্ছে না!")
    exit()

print("ম্যাজিক শুরু হচ্ছে... ক্যামেরা উইন্ডো ওপেন হওয়া পর্যন্ত অপেক্ষা করো।")

while True:
    ok, img = cap.read()
    if not ok:
        print("ফ্রেম পাওয়া যাচ্ছে না!")
        break
    
    img = cv2.flip(img, 1)
    h, w = img.shape[:2]
    
    # ইমেজ কনভার্ট
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_image)

    if result.hand_landmarks:
        for i, hand in enumerate(result.hand_landmarks):
            # হাত শনাক্ত করা (Left/Right)
            label = result.handedness[i][0].category_name 
            
            # ল্যান্ডমার্ক ৪ (Thumb) এবং ৮ (Index)
            tp = (int(hand[4].x * w), int(hand[4].y * h))
            ip = (int(hand[8].x * w), int(hand[8].y * h))

            cv2.circle(img, tp, 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, ip, 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, tp, ip, (0, 255, 0), 3)
            
            dist = float(np.hypot(ip[0] - tp[0], ip[1] - tp[1]))

            # ভলিউম কন্ট্রোল (ডান হাত দিয়ে - যা ক্যামেরায় Left দেখাবে)
            if label == "Left": 
                v = np.interp(dist, [30, 250], [minv, maxv])
                try: volctl.SetMasterVolumeLevel(v, None)
                except: pass
                pct = int(np.interp(dist, [30, 250], [0, 100]))
                cv2.putText(img, f"Vol: {pct}%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # ব্রাইটনেস কন্ট্রোল (বাম হাত দিয়ে - যা ক্যামেরায় Right দেখাবে)
            elif label == "Right":
                b = int(np.interp(dist, [30, 250], [0, 100]))
                try: sbc.set_brightness(b)
                except: pass
                cv2.putText(img, f"Bright: {b}%", (w-250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Control Window", img)
    
    # কি-বোর্ড থেকে 'q' চাপলে বন্ধ হবে
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()























































import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import os

# =========================
# ✅ MODEL CHECK
# =========================
model_path = 'hand_landmarker.task'
if not os.path.exists(model_path):
    print("Model file not found!")
    input("Press Enter...")
    exit()

# =========================
# ✅ MEDIAPIPE SETUP
# =========================
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7
)
detector = vision.HandLandmarker.create_from_options(options)

# =========================
# ✅ AUDIO SETUP
# =========================
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

# =========================
# ✅ CAMERA
# =========================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera error!")
    exit()

# =========================
# ✅ SMOOTH + CONTROL
# =========================
prev_dist = 0
smooth = 0.7
last_brightness = -1

print("🔥 System Started...")

# =========================
# 🔁 MAIN LOOP
# =========================
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

            # =========================
            # ✅ SAFE HANDEDNESS
            # =========================
            if result.handedness and len(result.handedness) > i:
                label = result.handedness[i][0].category_name
            else:
                label = "Unknown"

            # =========================
            # ✅ LANDMARKS
            # =========================
            tp = (int(hand[4].x * w), int(hand[4].y * h))
            ip = (int(hand[8].x * w), int(hand[8].y * h))

            cv2.circle(img, tp, 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, ip, 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, tp, ip, (0, 255, 0), 3)

            # =========================
            # ✅ DISTANCE
            # =========================
            dist = float(np.hypot(ip[0] - tp[0], ip[1] - tp[1]))
            dist = max(30, min(300, dist))

            # smooth
            dist = smooth * prev_dist + (1 - smooth) * dist
            prev_dist = dist

            # =========================
            # ✅ FALLBACK (POSITION BASED)
            # =========================
            cx = (tp[0] + ip[0]) // 2

            # =========================
            # 🔊 VOLUME CONTROL
            # =========================
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

            # =========================
            # 🌞 BRIGHTNESS CONTROL
            # =========================
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

            # =========================
            # DEBUG LABEL SHOW
            # =========================
            cv2.putText(img, label, (tp[0], tp[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imshow("🔥 Hand Control PRO", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()