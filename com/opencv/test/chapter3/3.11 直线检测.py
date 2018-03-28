import cv2
import numpy as np

img = cv2.imread("../../../../resources/image/3.png")
gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 120)
cv2.imshow("edges", edges)
minLineLength = 20
maxLineGap = 10
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)

for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(gray, (x1, y1), (x2, y2), (0, 0, 0), 2)

cv2.imshow("lines", gray)
cv2.waitKey(30000)
cv2.destroyAllWindows()