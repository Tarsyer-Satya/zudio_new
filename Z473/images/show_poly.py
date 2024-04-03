import numpy as np
import cv2

# Create a black image
image = cv2.imread('Z473_channel_no_9.jpg')

# Define points for multiple polygons
polygons = [
    np.array([[0, 372], [0, 720], [837, 720],[923,494],[172,222]], np.int32),  # E
    np.array([[172, 222],[923, 494], [1065, 316],[390,83]], np.int32),  # L1
    np.array([[390, 83], [1065, 316], [1117, 147], [551,0]], np.int32)  # L2
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
 