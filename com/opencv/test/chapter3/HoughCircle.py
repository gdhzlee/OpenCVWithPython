import cv2
import numpy as np

img = cv2.imread("../../../../resources/image/5.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 5)
cimg = cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=1, minRadius=0, maxRadius=0)

circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
    cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

cv2.imshow("image", img)
cv2.waitKey(4000)
