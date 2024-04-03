import numpy as np
import cv2

# Create a black image
image = cv2.imread('Z585_channel_no_1.jpg')

# Define points for multiple polygons
polygons = [
    np.array([[0, 123], [0, 720], [1175, 720],[170,118]], np.int32),  # E
    np.array([[170, 118],[1020, 621], [1195, 363],[390,41]], np.int32),  # L1
    np.array([[390, 41], [1195, 363], [1138, 168], [643,8]], np.int32)  # L2
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
