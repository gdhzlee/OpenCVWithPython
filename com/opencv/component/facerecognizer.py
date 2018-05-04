import cv2
import numpy as np
from time import ctime
from com.opencv.component.utils import ImageUtils

class FaceRecognization(object):

    def __init__(self):
        # 初始化特征识别
        self._faceCascade = cv2.CascadeClassifier("../cascades/haarcascade_frontalface_default.xml")
        # 初始化图片工具
        self._imageUtils = ImageUtils()

class Detect(FaceRecognization):

    def __init__(self):
        FaceRecognization.__init__(self)

    def detect(self, img, faceInfos):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self._faceCascade.detectMultiScale(gray, 1.3, 5)
        print(faces)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 5)

            # 存储人脸
            faceImg = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
            self._imageUtils.writeface(personName=faceInfos, faceImg=faceImg)
        return img

class Recognize(FaceRecognization):

    def __init__(self):
        FaceRecognization.__init__(self)
        # 初始化特征训练
        self._faceRecognize =  cv2.face.LBPHFaceRecognizer_create()

        # 读取人脸库数据
        [FACES, COUNT], faceInfos = self._imageUtils.readface()
        self._faceRecognize.train(np.asarray(FACES), np.asarray(COUNT, dtype=np.int32))
        self._faceCount = COUNT

    def recognize(self, img):

        # 读取人脸库数据
        [FACES, COUNT], faceInfos = self._imageUtils.readface()

        # 对人脸库数据进行特征训练
        if COUNT != self._faceCount:
            print("出现新数据，重新训练")
            self._faceCount = COUNT
            self._faceRecognize.train(np.asarray(FACES), np.asarray(COUNT, dtype=np.int32))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self._faceCascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img.copy(), (x, y), (x + w, y + h), (0, 0, 255), 2)
            roi = gray[y:(y + h), x:(x + w)]
            try:
                roi = cv2.resize(roi, (200, 200), interpolation=cv2.INTER_LINEAR)

                # 预测识别人脸
                params = self._faceRecognize.predict(roi)
                print("识别人脸: {0}, 可信度: {1}".format(faceInfos[params[0]], params[1]))
                if params[1] > 50:
                    cv2.putText(img, "unKnown", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
                else:
                    cv2.putText(img, faceInfos[params[0]], (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
            except Exception as e:
                print(e)

        return img

if __name__=="__main__":

    img = cv2.imread("../../../resources/image/11.jpg")
    detect =  Detect()
    img = detect.detect(img=img, faceInfos="lili")
    cv2.imshow("",img)



    # img = cv2.imread("../../../resources/image/12.jpg")
    # recongnization =  Recognize()
    # img1 = recongnization.recognize(img)
    # cv2.imshow("de",img1)
    # cv2.waitKey(0)

    # detect = Detect()
    # cap = cv2.VideoCapture("../../../resources/video/2.mp4")
    # while cap.isOpened():
    #     ret, frame = cap.read()
    #     if ret is False:
    #         break
    #
    #     img = detect.detect(img=frame, faceInfos="lixiaojun")
    #     cv2.imshow("检测",img)
    #     cv2.waitKey(50)

    # recongnization = Recognize()
    # cap = cv2.VideoCapture("../../../resources/video/2.mp4")
    # while cap.isOpened():
    #     ret, frame = cap.read()
    #     if ret is False:
    #         break
    #
    #     img = recongnization.recognize(frame)
    #     cv2.imshow("识别",img)
    #     cv2.waitKey(1)