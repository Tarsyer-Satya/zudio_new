import numpy as np
import cv2

# Create a black image
image = cv2.imread('Z143_channel_no_3.jpg')

# Define points for multiple polygons
polygons = [
    np.array([[1065, 717], [1280, 0], [926, 0],[382,641],[500,719]], np.int32),  # E
    np.array([[382, 641],[926, 0], [610, 0],[47,554]], np.int32),  # L1
    np.array([[47, 554], [610, 0], [411, 0], [20,332]], np.int32)  # L2
]

# Reshape the points array into a 3D array with one entry for each polygon
polygons = [polygon.reshape((-1, 1, 2)) for polygon in polygons]

# Draw each polygon on the image
for polygon in polygons:
    cv2.polylines(image, [polygon], isClosed=True, color=(0, 255, 0), thickness=2)

# Display the image
cv2.imshow('Polygons', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
