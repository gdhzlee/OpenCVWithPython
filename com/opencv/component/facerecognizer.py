import cv2
import numpy as np
from com.opencv.component.utils import ImageUtils

class Detect(object):

    def __init__(self):
        # 初始化特征识别
        self._faceCascade = cv2.CascadeClassifier("../../cascades/haarcascade_frontalface_default.xml")
        # 初始化图片工具
        self._imageUtils = ImageUtils()

    def detect(self, img, save):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self._faceCascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces[0]:
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 5)

            face = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
        return faces

class Recognize(object):

    def __init__(self):
        # 初始化特征识别
        self._faceCascade = cv2.CascadeClassifier("../../cascades/haarcascade_frontalface_default.xml")
        # 初始化图片工具
        self._imageUtils = ImageUtils()
        #
        self._faceRecognize =  cv2.face.LBPHFaceRecognizer_create()


    def recognize(self, img):

        # 读取人脸库数据
        [FACES, COUNT], faceInfos = self._imageUtils.readface()

        # 对人脸库数据进行特征训练
        self._faceRecognize.train(np.asarray(FACES), np.asarray(COUNT))

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
                cv2.putText(img, faceInfos[params[0]], (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
            except Exception as e:
                print(e)

        return img