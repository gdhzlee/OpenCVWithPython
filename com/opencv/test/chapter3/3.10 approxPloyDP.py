import cv2

img = cv2.imread("../../../../resources/image/4.jpg")
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(grayImg, 127, 255, cv2.THRESH_BINARY)
grayImg, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

cnt = contours[0]
maxArea = cv2.contourArea(cnt)
for cont in contours:
    # cv2.imshow("image", cv2.pyrDown(cv2.drawContours(img.copy(), cont, -1, (0, 255, 0), 10)))
    area = cv2.contourArea(cont)
    if area > maxArea:
        cnt = cont
        maxArea = area
cv2.imshow("image1", cv2.drawContours(img.copy(), cnt, -1, (0, 255, 0), 1))

epsilon = 0.01 * cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)
print(approx)


cv2.waitKey(3000)
cv2.destroyAllWindows()