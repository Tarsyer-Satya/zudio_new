import numpy as np
import cv2

# Create a black image
image = cv2.imread('Z341_channel_no_9.jpg')

# Define points for multiple polygons
polygons = [
    np.array([[419, 720], [1070, 717], [1124, 600],[256,126],[19,267]], np.int32),  # E
    np.array([[256, 126],[1124, 600], [1201, 404],[419,63]], np.int32),  # L1
    np.array([[419, 63], [1201, 404], [1234, 275], [571,18]], np.int32)  # L2
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
