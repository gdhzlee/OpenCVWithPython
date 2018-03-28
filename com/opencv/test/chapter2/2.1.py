import cv2
import numpy as np
import os

img = np.zeros((3,3), dtype = np.uint8);
print(img);

img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR);
print(img)

randomByteArray = bytearray(os.urandom(120000));
# print(randomByteArray);
flatNumpyArray = np.array(randomByteArray);

grayImage = flatNumpyArray.reshape(300,400);
cv2.imshow("grayImage",grayImage);

bgrImage = flatNumpyArray.reshape(100,400,3)
cv2.imshow("bgrImage",bgrImage);
cv2.waitKey(3000);

print();
# 第一二个参数代表，像素的坐标；第三个参数代表通道
print(bgrImage.item(1,1,0));
bgrImage.itemset((1,1,0),255);
print(bgrImage.item(1,1,0));