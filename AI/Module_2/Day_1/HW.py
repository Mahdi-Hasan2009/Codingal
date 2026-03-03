import cv2  # Import the OpenCV library
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # Hide main window

# Step 1: Load the image from file
image = cv2.imread(r'E:\Codingal\AI\Module_2\Day_1\Carrot-Orange.jpg')

# Step 2: Display the original image in a resizable window
cv2.namedWindow('Loaded Image', cv2.WINDOW_NORMAL)   # Make the window resizable
cv2.resizeWindow('Loaded Image', 500, 500)           # Set window size (does not resize the image itself)
cv2.imshow('Loaded Image', image)                    # Show the image

# Step 3: Print the original image dimensions (Height, Width, Channels)
print(f"Original Image Dimensions: {image.shape}")

# Step 4: Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 5: Resize the grayscale image to 224x224 pixels
resized_image = cv2.resize(gray_image, (224, 224))

# Step 6: Show the resized grayscale image
cv2.imshow('Processed Image', resized_image)

# Step 7: Wait for a key press
key = cv2.waitKey(0)
print("Pressed key code:", key)#####

# Step 8: If 'S' or 's' key is pressed, save the processed image
if key == ord('s') or key == ord('S'):
    # Ask user for width, height, filename
    w = simpledialog.askinteger("Width", "Enter width:", minvalue=1)
    h = simpledialog.askinteger("Height", "Enter height:", minvalue=1)

    # Ask user where to save (folder + filename)
    save_path = filedialog.asksaveasfilename(defaultextension=".jpg",
    filetypes=[("JPEG files","*.jpg"),("All files","*.*")],
    title="Save Image As")
    if save_path and w and h:
        resized = cv2.resize(resized_image, (w, h))
        cv2.imwrite(save_path, resized)
        messagebox.showinfo("Saved", f"Image saved as {save_path}")
    else:
        messagebox.showwarning("Cancelled", "Save cancelled")
else: 
    print("Image not saved")
    

if key == ord('E') or key == ord('e'):
    edges = cv2.Canny(resized_image, 100, 200)

    cv2.imshow("Canny Edge Detection", edges)
    cv2.namedWindow("Canny Edge Detection", cv2.WINDOW_NORMAL)
    cv2.imshow("Canny Edge Detection", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Edge detection not applied.")
    
if key == ord('G') or key == ord('g'):
    blurred = cv2.GaussianBlur(resized_image, (5,5), 0)
    cv2.imshow("Blurred Image", blurred)
    cv2.waitKey(0)
    
if key == ord('F') or key == ord('f'):
    # Ask user flip direction
    direction = simpledialog.askstring("Flip", "Enter direction (h=horizontal, v=vertical, b=both):")
    if direction:
        if direction.lower() == 'h':
            flipped = cv2.flip(resized_image, 1)
        elif direction.lower() == 'v':
            flipped = cv2.flip(resized_image, 0)
        elif direction.lower() == 'b':
            flipped = cv2.flip(resized_image, -1)
        else:
            messagebox.showwarning("Error", "Invalid input")
            flipped = resized_image

        cv2.imshow("Flipped Image", flipped)
        cv2.waitKey(0)
        
if key == ord('R') or key == ord('r'):
    # Ask user angle
    angle = simpledialog.askfloat("Rotate", "Enter angle (degrees, clockwise):")
    if angle is not None:
        (h, w) = resized_image.shape[:2]
        center = (w//2, h//2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(resized_image, M, (w, h))
        cv2.imshow("Rotated Image", rotated)
        cv2.waitKey(0)
    
if key == ord('C') or key == ord('c'):
    # Ask user contrast (alpha) and brightness (beta)
    alpha = simpledialog.askfloat("Contrast", "Enter contrast (1.0=original):")
    beta = simpledialog.askfloat("Brightness", "Enter brightness (0=original):")
    if alpha is None:
        alpha = 1.0
    if beta is None:
        beta = 0

    contrast_img = cv2.convertScaleAbs(resized_image, alpha=alpha, beta=beta)
    cv2.imshow("Contrast / Brightness Adjusted", contrast_img)
    cv2.waitKey(0)
    
# Step 9: Close all OpenCV windows
cv2.destroyAllWindows()

# Step 10: Print the dimensions of the processed image
print(f"Processed Image Dimensions: {resized_image.shape}")
