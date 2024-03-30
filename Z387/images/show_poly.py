import numpy as np
import cv2

# Create a black image
image = cv2.imread('Z387_channel_no_3.jpg')

# Define points for multiple polygons
polygons = [
    np.array([[0, 720], [1280, 720], [1278, 423],[0,287]], np.int32),  # E
    np.array([[0, 287], [1278, 423], [1278, 203],[0,62]], np.int32),  # L1
    np.array([[0, 62], [712, 137], [703, 0], [0,0]], np.int32)  # L2
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
