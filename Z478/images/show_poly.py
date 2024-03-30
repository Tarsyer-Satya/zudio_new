import numpy as np
import cv2

# Create a black image
image = cv2.imread('Z478_channel_no_5.jpg')

# Define points for multiple polygons
polygons = [
    np.array([[96, 720], [698, 719], [309, 0],[71,6]], np.int32),  # E
    np.array([[309, 0],[698, 719], [1052, 719],[561,115]], np.int32),  # L1
    np.array([[561, 115], [1052, 719], [1244, 718], [756,189]], np.int32)  # L2
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
