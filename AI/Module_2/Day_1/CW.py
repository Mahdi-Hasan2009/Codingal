import cv2  # Import the OpenCV library

# Step 1: Load the image from file
image = cv2.imread(r'E:\Codingal\AI\Module_2\Day_1\Carrot-Orange.jpg')

# Step 2: Display the original image in a resizable window
cv2.namedWindow('Loaded Image', cv2.WINDOW_NORMAL)   # Make the window resizable
cv2.resizeWindow('Loaded Image', 800, 500)           # Set window size (does not resize the image itself)
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

# Step 8: If 'S' or 's' key is pressed, save the processed image
if key == ord('s') or key == ord('S'):
    cv2.imwrite('grayscale_resized_image.jpg', resized_image)
    print("Image saved as grayscale_resized_image.jpg")
else:
    print("Image not saved")

# Step 9: Close all OpenCV windows
cv2.destroyAllWindows()

# Step 10: Print the dimensions of the processed image
print(f"Processed Image Dimensions: {resized_image.shape}")
