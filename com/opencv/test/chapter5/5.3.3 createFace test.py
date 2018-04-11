import cv2

img = cv2.imread("../../../../resources/image/1.jpg")
cv2.imshow("roi", img[0:100, 0:200])
cv2.waitKey(0)