import cv2
import numpy as np
from scipy import ndimage
import os

kernal_3x3 = np.array([[-1, -1, -1],
                  [-1,  8, -1],
                  [-1, -1, -1]])
kernal_5x5 = np.array([[-1, -1, -1, -1, -1],
                      [-1,  1,  2,  1, -1],
                      [-1,  2,  4,  2, -1],
                      [-1,  1,  2,  1, -1],
                      [-1, -1, -1, -1, -1]])

img = cv2.imread("../../../../resources/image/1.jpg",0)
print(img is None)
file = os.path.dirname("../../../../resources/image/1.jpg")
print(file)

k3 = ndimage.convolve(img, kernal_3x3)
k5 = ndimage.convolve(img, kernal_5x5)

blurred = cv2.GaussianBlur(img, (11, 11), 0)
g_hpf = img - blurred
cv2.imshow("k3", k3)
cv2.imshow("k5", k5)
cv2.imshow("gaussian", g_hpf)
cv2.waitKey(3000)
cv2.destroyAllWindows()