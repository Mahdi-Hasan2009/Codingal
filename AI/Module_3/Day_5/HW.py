import cv2, time, pyautogui
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import numpy as np   #*******

#Load model
model_path = 'E:\\Codingal\\AI\\Module_3\\Day_5\\hand_landmarker.task'
if not os.path.exists(model_path):
    print("Model file not found!")
    exit()

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,#******
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7
)
detector = vision.HandLandmarker.create_from_options(options)

# Configurations
SCROLL_SPEED = 300
SCROLL_DELAY = 1
CAM_WIDTH, CAM_HEIGHT = 640, 480

# 🖥️ screen size
screen_w, screen_h = pyautogui.size()
# whole screen is 1920x1080, webcam is 640x480, so we need to map webcam coords to screen coords

# 🎯 smoothing
prev_x, prev_y = 0, 0 # in middle of the screen
smooth_factor = 5 # higher is smoother but more lag


def detect_gesture(landmarks, handedness):
    fingers = []

    tips = [8, 12, 16, 20]

    for tip in tips:
        if landmarks[tip].y < landmarks[tip - 2].y:# আঙুলের টিপের উপর-নিচ অবস্থান যদি তার মাঝের জয়েন্টের উপর-নিচ  অবস্থান থেকে উপরে থাকে, তাহলে ধরে নাও যে আঙুলটি খোলা আছে 
            fingers.append(1)

    thumb_tip = landmarks[4]# thumb tip
    thumb_ip = landmarks[3]# thumb finger's middle joint

    if (handedness == "Right" and thumb_tip.x > thumb_ip.x) or \
       (handedness == "Left" and thumb_tip.x < thumb_ip.x): # থাম্বের টিপের ডান-বা-বাম অবস্থান যদি তার মধ্যবর্তী জয়েন্টের ডান-বা-বাম অবস্থান থেকে ডান-বা-বাম থাকে, তাহলে ধরে নাও যে থাম্ব খোলা আছে
        fingers.append(1)

    return "scroll_up" if sum(fingers) == 5 else "scroll_down" if len(fingers) == 0 else "none"


cap = cv2.VideoCapture(0)
cap.set(3, CAM_WIDTH)#ক্যামেরার width ৬৪০ সেট করো (3 = width-এর code)
cap.set(4, CAM_HEIGHT)#ক্যামেরার height ৪৮০ সেট করো (4 = height-এর code)

last_scroll = p_time = 0 #শুরুতে সবই ০, last_scroll হলো শেষবার স্ক্রল করার সময়, p_time হলো শেষবার ফ্রেম রেন্ডার করার সময়
last_click_time = 0

print("Gesture Scroll Control Active\nOpen palm: Scroll Up\nFist: Scroll Down\nPress 'q' to exit")
#******
prev_zoom_dist = 0 # আগের frame-এ দুই হাতের দূরত্ব = 0, অর্থাৎ প্রথমবার দুই হাতের দূরত্ব মাপা হবে না
ZOOM_THRESHOLD = 15# দুই হাতের দূরত্বে ১৫ পিক্সেল এর বেশি পরিবর্তন হলে জুম ইন/আউট হবে, ছোট পরিবর্তনগুলো স্ক্রল হিসেবে বিবেচিত হবে না যাতে ভুল স্ক্রল না হয়
#LOOP START
while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)# OpenCV ক্যামেরা থেকে BGR ফরম্যাটে ছবি দেয়, কিন্তু MediaPipe RGB ফরম্যাটে কাজ করে, তাই রঙের ফরম্যাট পরিবর্তন করা হচ্ছে

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_image)

    gesture, handedness = "none", "Unknown"

    if result.hand_landmarks:# যদি হাতের landmark পাওয়া যায়, তাহলে প্রতিটি হাতের জন্য লুপ চালাও
        for i in range(len(result.hand_landmarks)):

            hand = result.hand_landmarks[i]

            if result.handedness and len(result.handedness) > i:
                handedness = result.handedness[i][0].category_name

            gesture = detect_gesture(hand, handedness)

            #DRAW AREA
            h, w = img.shape[:2]

            for lm in hand:
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 3, (0,255,0), -1)

            #CURSOR CONTROL
            ix = int(hand[8].x * w)#তর্জনীর (index finger, landmark 8) pixel position বের করো।
            iy = int(hand[8].y * h)

            screen_x = np.interp(ix, [0, w], [0, screen_w])
            screen_y = np.interp(iy, [0, h], [0, screen_h])

            curr_x = prev_x + (screen_x - prev_x) / smooth_factor
            curr_y = prev_y + (screen_y - prev_y) / smooth_factor

            pyautogui.moveTo(curr_x, curr_y)#*******

            prev_x, prev_y = curr_x, curr_y
            
            # TWO HAND ZOOM START
            if len(result.hand_landmarks) == 2:

                hand1 = result.hand_landmarks[0]
                hand2 = result.hand_landmarks[1]

                h, w = img.shape[:2]

                # two hand's index finger
                x1, y1 = int(hand1[8].x * w), int(hand1[8].y * h)# convert normalized landmark coordinates to pixel coordinates for hand 1
                x2, y2 = int(hand2[8].x * w), int(hand2[8].y * h)# convert normalized landmark coordinates to pixel coordinates for hand 2

                # distance
                dist = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

                # draw line
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 3)

                if prev_zoom_dist != 0:

                    if dist - prev_zoom_dist > ZOOM_THRESHOLD:
                        pyautogui.hotkey('ctrl', '+')   # zoom in

                    elif prev_zoom_dist - dist > ZOOM_THRESHOLD:
                        pyautogui.hotkey('ctrl', '-')   # zoom out

                prev_zoom_dist = dist
            # TWO HAND ZOOM END

            # PINCH CLICK
            x1, y1 = int(hand[4].x * w), int(hand[4].y * h)
            x2, y2 = int(hand[8].x * w), int(hand[8].y * h)

            dist = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

            if dist < 20:
                if (time.time() - last_click_time) > 0.5:
                    pyautogui.click()#*******
                    last_click_time = time.time()

            # SCROLL
            if (time.time() - last_scroll) > SCROLL_DELAY:
                if gesture == "scroll_up":
                    pyautogui.scroll(SCROLL_SPEED)
                elif gesture == "scroll_down":
                    pyautogui.scroll(-SCROLL_SPEED)
                last_scroll = time.time()
                
# FPS ও Display
    fps = 1/(time.time()-p_time) if (time.time()-p_time) > 0 else 0
    p_time = time.time()

    cv2.putText(img, f"FPS: {int(fps)} | Hand: {handedness} | Gesture: {gesture}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

    cv2.imshow("Gesture Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# LOOP END

cap.release()
cv2.destroyAllWindows()