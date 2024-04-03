import cv2
image = cv2.imread('Z139_channel_no_6.jpg')
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()