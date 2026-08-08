import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import simpledialog, messagebox
from tkinter import filedialog

def display_image(title, image):
    """Utility function to display an image."""
    plt.figure(figsize=(8, 8))
    if len(image.shape) == 2:  # Grayscale image
        plt.imshow(image, cmap='gray')
    else:  # Color image
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

    
def interactive_edge_detection(image_path):
    """Interactive activity for edge detection and filtering."""
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found!")
        return


    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_image("Original Grayscale Image", gray_image)

    print("Select an option:")
    print("1. Sobel Edge Detection")
    print("2. Canny Edge Detection")
    print("3. Laplacian Edge Detection")
    print("4. Gaussian Smoothing")
    print("5. Median Filtering")
    print("6. Manual Threshold")
    print("7. Otsu Threshold")
    print("8. Adaptive Threshold")
    print("9. Brightness and contrast")
    print("10. Erosion")
    print("11. Dilation")
    print("12. Opening")
    print("13. Closing")
    print("14. Contour Detection")
    print("15. Exit")

    while True:
        choice = input("Enter your choice (1-15): ")

        if choice == "1":
            # Sobel Edge Detection
            sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
            combined_sobel = cv2.bitwise_or(sobel_x.astype(np.uint8), sobel_y.astype(np.uint8))
            display_image("Sobel Edge Detection", combined_sobel)

        elif choice == "2":
            # Canny Edge Detection
            print("Adjust thresholds for Canny (default: 100 and 200)")
            lower_thresh = int(input("Enter Lower threshold: "))
            upper_thresh = int(input("Enter Upper threshold: "))
            edges = cv2.Canny(gray_image, lower_thresh, upper_thresh)
            display_image("Canny Edge Detection", edges)

        elif choice == "3":
            # Laplacian Edge Detection
            laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
            display_image("Laplacian Edge Detection", np.abs(laplacian).astype(np.uint8))

        elif choice == "4":
            # Gaussian Smoothing
            print("Adjust kernel size for Gaussian blur (must be odd, default: 5)")
            kernel_size = int(input("Enter kernel size (odd number): "))
            blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
            display_image("Gaussian Smoothed Image", blurred)

        elif choice == "5":
            # Median Filtering
            print("Adjust kernel size for Median filtering (must be odd, default: 5)")
            kernel_size = int(input("Enter kernel size (odd number): "))
            median_filtered = cv2.medianBlur(image, kernel_size)
            display_image("Median Filtered Image", median_filtered)
        
        
        elif choice == "6":
          print("Enter threshold value (0-255): ")
          thresh_val = int(input("Threshold: "))

          ret, thresh_img = cv2.threshold(gray_image,   thresh_val, 255, cv2.THRESH_BINARY)

          display_image("Threshold Image", thresh_img)     
          
        elif choice == "7":
          ret, otsu_thresh = cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
          display_image("Otsu Threshold Image", otsu_thresh)

          print("Otsu threshold value:", ret)
        
        elif choice == "8":
            adaptive = cv2.adaptiveThreshold(gray_image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
            display_image("Adaptive Threshold Image", adaptive)
        
        elif choice == "9":

            alpha = simpledialog.askfloat("Contrast", "Enter        contrast (1.0 = original):")
            beta = simpledialog.askfloat("Brightness", "Enter brightness (0 = original):")

            if alpha is None:
                alpha = 1.0
            if beta is None:
                beta = 0

            contrast_img = cv2.convertScaleAbs(gray_image, alpha=alpha, beta=beta)

            display_image("Brightness & Contrast Adjusted", contrast_img)
            
        elif choice == "10":

            print("Enter kernel size (odd number): ")
            k = int(input())

            kernel = np.ones((k, k), np.uint8)

            eroded = cv2.erode(gray_image, kernel, iterations=1)

            display_image("Erosion Result", eroded)
        
        elif choice == "11":

            print("Enter kernel size (odd number): ")
            k = int(input())

            kernel = np.ones((k, k), np.uint8)

            dilated = cv2.dilate(gray_image, kernel, iterations=1)

            display_image("Dilation Result", dilated)
            
        elif choice == "12":
            k = int(input("Enter kernel size: "))

            kernel = np.ones((k,k), np.uint8)

            opening = cv2.morphologyEx(gray_image, cv2.MORPH_OPEN, kernel)

            display_image("Opening Result", opening)
           
           
        elif choice == "13":

            k = int(input("Enter kernel size: "))

            kernel = np.ones((k,k), np.uint8)

            closing = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)

            display_image("Closing Result", closing)
            
        elif choice == "14":
    
            # First make a binary image
            ret, thresh = cv2.threshold(gray_image, 127, 255,   cv2.THRESH_BINARY)
    
            # Find contours
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
             # Draw contours
            contour_img = gray_image.copy()
            cv2.drawContours(contour_img, contours, -1, (0,255,0), 2)
    
            display_image("Contour Detection", contour_img)
    
            print("Number of objects detected:", len(contours)) 

        elif choice == "15":
            # Exit
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a number between 1 and 15.")

# Provide the path to an image for the activity
interactive_edge_detection('E:\Codingal\AI\Module_2\Day_4\Carrot-Orange.jpg')