import cv2
import numpy as np

def apply_color_filter(image, filter_type):
    """Apply the specified color filter to the image."""
    # Create a copy of the image to avoid modifying the original
    filtered_image = image.copy()
    if filter_type == "red_tint":
        # Remove blue and green channels for red tint
        filtered_image[:, :, 1] = 0  # Green channel to 0
        filtered_image[:, :, 0] = 0  # Blue channel to 0
    elif filter_type == "blue_tint":
        # Remove red and green channels for blue tint
        filtered_image[:, :, 1] = 0  # Green channel to 0
        filtered_image[:, :, 2] = 0  # Red channel to 0
    elif filter_type == "green_tint":
        # Remove blue and red channels for green tint
        filtered_image[:, :, 0] = 0  # Blue channel to 0
        filtered_image[:, :, 2] = 0  # Red channel to 0
    elif filter_type == "increase_red":
        # Increase the intensity of the red channel
        filtered_image[:, :, 2] = cv2.add(filtered_image[:, :, 2], 50)  # Increase red channel
    elif filter_type == "decrease_blue":
        # Decrease the intensity of the blue channel
        filtered_image[:, :, 0] = cv2.subtract(filtered_image[:, :, 0], 50)  # Decrease blue channel
    return filtered_image
  
def sepia_filter(image):

    sepia_matrix = np.array([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]
    ])

    sepia_image = cv2.transform(image, sepia_matrix)

    sepia_image = np.clip(sepia_image, 0, 255)

    cv2.imshow("Sepia Filter", sepia_image)
    cv2.waitKey(0)
  
def sharpen_filter(image):

    kernel = np.array([
        [0,-1,0],
        [-1,5,-1],
        [0,-1,0]
    ])

    sharpened = cv2.filter2D(image, -1, kernel)

    cv2.imshow("Sharpened Filter", sharpened)
    cv2.waitKey(0)
  
def multiple_filter_combination(image):
    
    sepia = sepia_filter(image)

    sharp = sharpen_filter(sepia)

    cv2.imshow("Combined Filter", sharp)
    cv2.waitKey(0)


# Load the image
image_path = 'E:\Codingal\AI\Module_2\Day_5\Radish.jpg'  # Provide your image path
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found!")
else:
    filter_type = "original"  # Default filter type

    print("Press the following keys to apply filters:")
    print("r - Red Tint")
    print("b - Blue Tint")
    print("g - Green Tint")
    print("i - Increase Red Intensity")
    print("d - Decrease Blue Intensity")
    print("s - Sepia Filter")
    print("h - Sharpening Filter")
    print("m - Multiple Filter Combination")
    print("q - Quit")

    while True:
        # Apply the selected filter
        filtered_image = apply_color_filter(image, filter_type)
        # Display the filtered image
        cv2.imshow("Filtered Image", filtered_image)
        # Wait for key press
        key = cv2.waitKey(0) & 0xFF

        # Map key presses to filters
        if key == ord('r'):
            filter_type = "red_tint"
        elif key == ord('b'):
            filter_type = "blue_tint"
        elif key == ord('g'):
            filter_type = "green_tint"
        elif key == ord('i'):
            filter_type = "increase_red"
        elif key == ord('d'):
            filter_type = "decrease_blue"
        elif key == ord("s"):
            image = sepia_filter(image)
        elif key == ord("h"):
            image = sharpen_filter(image)
        elif key == ord("m"):
            image = multiple_filter_combination(image)
        elif key == ord('q'):
            print("Exiting...")
            break
        else:
            print("Invalid key! Please use 'r', 'b', 'g', 'i', 'd', or 'q'.")

cv2.destroyAllWindows()