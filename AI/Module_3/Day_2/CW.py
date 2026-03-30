import cv2
import numpy as np
import time

def apply_filter(image, ftype,t1=100,t2=200):
    """Apply a filter to the image based on the filter type."""
    img = image.copy()
    if ftype == "red_tint":
        img[:, :, 1] = img[:, :, 0] = 0
    elif ftype == "green_tint":
        img[:, :, 0] = img[:, :, 2] = 0
    elif ftype == "blue_tint":
        img[:, :, 1] = img[:, :, 2] = 0
    elif ftype == "original":
        return img
    elif ftype == "negative":
        img = 255 - img
    elif ftype == "sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
        img = cv2.transform(image, kernel)
        img = np.clip(img, 0, 255).astype(np.uint8)
    elif ftype == "sobel":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sob = cv2.bitwise_or(sx.astype('uint8'), sy.astype('uint8'))
        img = cv2.cvtColor(sob, cv2.COLOR_GRAY2BGR)
    elif ftype == "canny":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        can = cv2.Canny(gray, t1, t2)
        img = cv2.cvtColor(can, cv2.COLOR_GRAY2BGR)
    elif ftype == "cartoon":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
        )
        color = cv2.bilateralFilter(image, 9, 300, 300)
        img = cv2.bitwise_and(color, color, mask=edges)
    return img

def main():
    t1 = 100
    t2 = 200
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return
    ftype = "original"
    print("Keys: r=Red, g=Green, b=Blue, s=Sobel, c=Canny, t=Cartoon, o=original, n=negative, e=sepia, q=Quit")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame")
            break
        out = apply_filter(frame, ftype,t1,t2)
        cv2.imshow("Filter", out)
        key = cv2.waitKey(1)
        if key == ord('r'):
            ftype = "red_tint"
        elif key == ord("o"):
            ftype = "original"
        elif key == ord('g'):
            ftype = "green_tint"
        elif key == ord('b'):
            ftype = "blue_tint"
        elif key == ord('s'):
            ftype = "sobel"
        elif key == ord('c'):
            ftype = "canny"
        elif key == 2490368:   # UP arrow
            t1 += 10
            t2 += 10
            print(f"Canny Threshold: {t1}, {t2}")
        elif key == 2621440:  # DOWN arrow
            t1 -= 10
            t2 -= 10
            print(f"Canny Threshold: {t1}, {t2}")
        
     
        elif key == ord('t'):
            ftype = "cartoon"
        elif key == ord('n'):
            ftype = "negative"
        elif key == ord('e'):
            ftype = "sepia"
        elif key == ord("q"):
          break
        t1 = max(0, min(255, t1))
        t2 = max(0, min(255, t2))
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
