import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

# ==== Load model ====
model_path = "E:\\Codingal\\AI\\Module_3\\Day_3\\hand_landmarker.task"
if not os.path.exists(model_path):
    print("Model file not found!")
    exit()

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7
)
detector = vision.HandLandmarker.create_from_options(options)

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

print("Hand Tracking Started! Press 'q' to quit.")

# Gesture detection function (UNCHANGED LOGIC)
def detect_gesture(hand_landmarks):
    landmarks = hand_landmarks
    tip_ids = [4, 8, 12, 16, 20]
    pip_ids = [2, 6, 10, 14, 18]
    extended = 0

    # Thumb check (x-axis)
    if abs(landmarks[tip_ids[0]].x - landmarks[pip_ids[0]].x) > 0.04:
        extended += 1

    # Other fingers check (y-axis)
    for i in range(1, 5):
        if landmarks[tip_ids[i]].y < landmarks[pip_ids[i]].y:
            extended += 1

    # Decide gesture
    if extended >= 4:
        return "Open"
    elif extended <= 1:
        return "Closed Fist"
    else:
        return "Partial"

# Main loop
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    results = detector.detect(mp_image)

    gesture = "No hand detected"

    if results.hand_landmarks:
        for idx in range(len(results.hand_landmarks)):

            hand_landmarks = results.hand_landmarks[idx]

            # handedness
            if results.handedness and len(results.handedness) > idx:
                hand_label = results.handedness[idx][0].category_name
            else:
                hand_label = "Unknown"

            gesture = detect_gesture(hand_landmarks)

            # Draw fingertips (same logic)
            fingertip_ids = [4, 8, 12, 16, 20]
            for tip_id in fingertip_ids:
                lm = hand_landmarks[tip_id]
                x, y = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (x, y), 10, (255, 0, 255), cv2.FILLED)
                cv2.putText(frame, str(tip_id), (x - 5, y - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

            # Draw hand label near wrist
            wrist = hand_landmarks[0]
            wrist_x, wrist_y = int(wrist.x * w), int(wrist.y * h)
            cv2.putText(frame, f"{hand_label} Hand", (wrist_x - 40, wrist_y + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Draw simple connections (manual lines)
            connections = [
                (0,1),(1,2),(2,3),(3,4),
                (0,5),(5,6),(6,7),(7,8),
                (5,9),(9,10),(10,11),(11,12),
                (9,13),(13,14),(14,15),(15,16),
                (13,17),(17,18),(18,19),(19,20),
                (0,17)
            ]

            for c in connections:
                x1, y1 = int(hand_landmarks[c[0]].x * w), int(hand_landmarks[c[0]].y * h)
                x2, y2 = int(hand_landmarks[c[1]].x * w), int(hand_landmarks[c[1]].y * h)
                cv2.line(frame, (x1, y1), (x2, y2), (0,255,0), 2)

    # Display gesture status
    status_color = (0, 255, 0) if gesture in ["Open", "Closed Fist"] else (0, 165, 255)
    cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)

    cv2.imshow("Hand Gesture Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()