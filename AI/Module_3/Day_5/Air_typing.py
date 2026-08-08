import cv2
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import numpy as np

# =============================================
# MODEL LOAD
# =============================================
model_path = 'E:\\Codingal\\AI\\Module_3\\Day_5\\hand_landmarker.task'
if not os.path.exists(model_path):
    print("Model file not found!")
    exit()

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7
)
detector = vision.HandLandmarker.create_from_options(options)

# =============================================
# CAMERA SETUP
# =============================================
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# =============================================
# VIRTUAL KEYBOARD LAYOUT
# =============================================
keys = [
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L"],
    ["Z","X","C","V","B","N","M","BCK"],  # BCK = Backspace
    ["SPACE"]
]

KEY_W   = 50    # প্রতিটা key এর width
KEY_H   = 42    # ছোট করা হলো যাতে নিচে না যায়
GAP     = 4     # key এর মাঝে ফাঁক
START_X = 10    # keyboard বাম থেকে শুরু
START_Y = 210   # উপরে তোলা হলো — আগে ছিল 270

typed_text    = ""
last_key_time = 0
KEY_COOLDOWN  = 0.6   # একটা key press এর পর কতক্ষণ অপেক্ষা

# =============================================
# FUNCTION: প্রতিটা key এর position বের করো
# =============================================
def get_key_rect(row_i, col_i, key):
    """
    একটা key এর বাম-উপর (x1,y1) এবং ডান-নিচ (x2,y2) কোণা বের করো
    """
    if key == "SPACE":
        # SPACE bar লম্বা হবে
        x1 = START_X
        y1 = START_Y + row_i * (KEY_H + GAP)
        x2 = x1 + KEY_W * 5
        y2 = y1 + KEY_H
    elif key == "BCK":
        x1 = START_X + col_i * (KEY_W + GAP)
        y1 = START_Y + row_i * (KEY_H + GAP)
        x2 = x1 + KEY_W + 20   # backspace একটু চওড়া
        y2 = y1 + KEY_H
    else:
        x1 = START_X + col_i * (KEY_W + GAP)
        y1 = START_Y + row_i * (KEY_H + GAP)
        x2 = x1 + KEY_W
        y2 = y1 + KEY_H

    return x1, y1, x2, y2

# =============================================
# FUNCTION: Keyboard আঁকো
# =============================================
def draw_keyboard(img, hover_key=None, pressing=False):
    for row_i, row in enumerate(keys):
        for col_i, key in enumerate(row):

            x1, y1, x2, y2 = get_key_rect(row_i, col_i, key)

            # রঙ ঠিক করো
            if key == hover_key and pressing:
                bg_color = (0, 255, 0)       # সবুজ = press হচ্ছে
            elif key == hover_key:
                bg_color = (200, 130, 0)     # কমলা = hover
            elif key == "BCK":
                bg_color = (0, 0, 180)       # লাল = backspace
            elif key == "SPACE":
                bg_color = (80, 80, 80)      # ধূসর = space
            else:
                bg_color = (40, 40, 40)      # গাঢ় = normal key

            # আধা-স্বচ্ছ (transparent) effect
            overlay = img.copy()
            cv2.rectangle(overlay, (x1, y1), (x2, y2), bg_color, -1)
            cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)

            # border আঁকো
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 1)

            # letter লেখো — SPACE আর BCK আলাদাভাবে
            if key == "SPACE":
                text_x = x1 + 80
                font_scale = 0.6
            elif key == "BCK":
                text_x = x1 + 5
                font_scale = 0.5
            else:
                text_x = x1 + 15
                font_scale = 0.75

            text_y = y1 + 28
            cv2.putText(img, key, (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, (255, 255, 255), 2)

    return img

# =============================================
# FUNCTION: আঙুল কোন key এর উপর আছে
# =============================================
def get_hovered_key(fx, fy):
    """
    fx, fy = আঙুলের ক্যামেরা pixel position
    return: hover করা key অথবা None
    """
    for row_i, row in enumerate(keys):
        for col_i, key in enumerate(row):
            x1, y1, x2, y2 = get_key_rect(row_i, col_i, key)
            if x1 < fx < x2 and y1 < fy < y2:
                return key
    return None

# =============================================
# FUNCTION: Pinch detect করো
# =============================================
def is_pinching(hand, w, h):
    """
    বুড়ো আঙুল (4) আর তর্জনী (8) এর দূরত্ব 50 পিক্সেলের কম হলে pinch
    """
    x1 = int(hand[4].x * w)
    y1 = int(hand[4].y * h)
    x2 = int(hand[8].x * w)
    y2 = int(hand[8].y * h)
    dist = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

    # দুই আঙুলের মাঝে লাইন আঁকার জন্য points ও return করছি
    return dist < 50, (x1, y1), (x2, y2), dist

# =============================================
# MAIN LOOP
# =============================================
p_time = 0

print("=== Air Typing Keyboard ===")
print("হাতের তর্জনী দিয়ে key hover করো")
print("বুড়ো আঙুল + তর্জনী pinch করলে key press হবে")
print("'q' চাপো বের হতে")

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    # ক্যামেরা mirror করো
    img = cv2.flip(img, 1)
    h, w = img.shape[:2]

    # MediaPipe এর জন্য RGB convert
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_image)

    hover_key = None
    pressing  = False

    if result.hand_landmarks:
        hand = result.hand_landmarks[0]   # প্রথম হাত নাও

        # তর্জনীর ক্যামেরা position
        fx = int(hand[8].x * w)
        fy = int(hand[8].y * h)

        # আঙুলের উপর বৃত্ত আঁকো
        cv2.circle(img, (fx, fy), 10, (0, 255, 255), -1)  # হলুদ বৃত্ত
        cv2.circle(img, (fx, fy), 12, (255, 255, 255), 2) # সাদা border

        # কোন key hover হচ্ছে
        hover_key = get_hovered_key(fx, fy)

        # Pinch check করো
        pinched, pt1, pt2, dist = is_pinching(hand, w, h)

        # pinch line আঁকো
        line_color = (0, 255, 0) if pinched else (255, 0, 255)
        cv2.line(img, pt1, pt2, line_color, 2)

        # distance দেখাও
        mid_x = (pt1[0] + pt2[0]) // 2
        mid_y = (pt1[1] + pt2[1]) // 2
        cv2.putText(img, f"{int(dist)}px", (mid_x, mid_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # Key press logic
        if pinched and hover_key:
            pressing = True
            if (time.time() - last_key_time) > KEY_COOLDOWN:
                if hover_key == "BCK":
                    typed_text = typed_text[:-1]   # শেষ letter মুছো
                elif hover_key == "SPACE":
                    typed_text += " "              # space যোগ করো
                else:
                    typed_text += hover_key        # letter যোগ করো

                last_key_time = time.time()

    # =============================================
    # KEYBOARD আঁকো
    # =============================================
    img = draw_keyboard(img, hover_key, pressing)

    # =============================================
    # TYPED TEXT দেখাও উপরে
    # =============================================
    # Text box background
    cv2.rectangle(img, (5, 5), (635, 55), (20, 20, 20), -1)
    cv2.rectangle(img, (5, 5), (635, 55), (100, 100, 100), 1)

    # শুধু শেষ ৩০টা character দেখাও (বেশি হলে কেটে যায়)
    display_text = typed_text[-30:] if len(typed_text) > 30 else typed_text
    cv2.putText(img, display_text + "|", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    # =============================================
    # STATUS দেখাও
    # =============================================
    status = f"Hover: {hover_key if hover_key else 'None'}"
    if pressing:
        status += "  [PRESSED!]"

    cv2.putText(img, status, (10, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)

    # FPS
    fps = 1 / (time.time() - p_time) if (time.time() - p_time) > 0 else 0
    p_time = time.time()
    cv2.putText(img, f"FPS: {int(fps)}", (560, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)

    # =============================================
    # WINDOW দেখাও
    # =============================================
    cv2.imshow("Air Typing Keyboard", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
