import cv2
import numpy as np

img = cv2.imread("../../../../resources/image/7.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)

""" 

第三个参数为Sobel算子的中控（aperture），定义了角点检测的铭感度，其取值介于3-31之间的奇数。

"""
dst = cv2.cornerHarris(gray, 2, 23, 0.04)
print(dst[0])
img[dst > 0.01 * dst.max()] = [0, 255, 0]

cv2.imshow("corners", img)
cv2.waitKey(0)
