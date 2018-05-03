import wx
import cv2

if __name__ == '__main__':
    img = cv2.imread("../../../resources/image/1.jpg")
    cv2.imshow("",img)
    print(img.shape[0:2])

    height, width = img.shape[0:2]
    print(height)
    cv2.waitKey(0)
