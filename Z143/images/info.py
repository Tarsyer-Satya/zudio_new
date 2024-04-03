import cv2
image = cv2.imread('Z143_channel_no_3.jpg')
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()