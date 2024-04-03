import numpy as np
import cv2

# Create a black image
image = cv2.imread('Z139_channel_no_6.jpg')

# Define points for multiple polygons
polygons = [
    np.array([[0, 720], [1280, 720], [1280, 190],[0,180]], np.int32),  # Polygon 1
    np.array([[0, 180], [1280, 190], [1280, 0],[0,0]], np.int32),  # Polygon 2
    # np.array([[1112, 350], [1021, 231], [786, 140], [777,241]], np.int32)  # Polygon 3
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
