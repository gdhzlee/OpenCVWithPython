import cv2

# 读取图像
img = cv2.imread("../../../../resources/image/8.jpg")
# 颜色空间转换
img = cv2.resize(img, (400, 400),cv2.INTER_CUBIC);

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 创建窗口
cv2.namedWindow("canny")

def todoNonthing(x):
    pass

# 创建两个范围为0至255跟踪条，分别代表threshold1和threshold2
cv2.createTrackbar('threshold1','canny',0,255,todoNonthing)
cv2.createTrackbar("threshold2","canny",0,255,todoNonthing)

edges = gray.copy()
while(True):

    # 显示图像
    cv2.imshow("canny",edges)

    # 从跟踪条中获取值
    threshold1 = cv2.getTrackbarPos("threshold1","canny")
    threshold2 = cv2.getTrackbarPos("threshold2","canny")

    # 边缘检测
    edges = cv2.Canny(img, threshold1, threshold2)

    # 监控键盘输入
    k = cv2.waitKey(2) & 0xFF
    if k == 27:
        break