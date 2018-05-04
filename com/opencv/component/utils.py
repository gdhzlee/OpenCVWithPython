import cv2
import os

class ImageUtils(object):

    def __init__(self):
        # 初始化人脸库
        self._databaseDir  = "../../../resources/facedatabase"

    # 获取人脸库的数据
    def readface(self):
        faceInfos = []
        [FACE, COUNT] = [], []
        count = 0
        for personName in os.listdir(self._databaseDir):

            # 排除文件
            personDir = os.path.join(self._databaseDir, personName)
            if os.path.isfile(personDir):
                continue

            # 记录人脸信息
            faceInfos.append(personName)
            # print(personName)
            for faceName in os.listdir(personDir):
                faceDir = os.path.join(personDir, faceName)

                if os.path.isdir(faceDir):
                    continue
                faceImg = cv2.imread(faceDir)
                faceImgGray = cv2.cvtColor(faceImg, cv2.COLOR_BGR2GRAY)
                if faceImg is None:
                    continue

                FACE.append(faceImgGray)
                COUNT.append(count)
                # print("     " + face)
            count += 1

        return [FACE, COUNT], faceInfos

    # 输出人脸数据
    def writeface(self, personName, faceImg):

        # 创建人脸库
        if os.path.exists(self._databaseDir) is False:
            os.mkdir(self._databaseDir)

        # 创建指定人脸数据
        personDir = os.path.join(self._databaseDir, personName)
        if os.path.exists(personDir) is False:
            os.mkdir(personDir)

        # 保存图像
        count = 0
        for face in os.listdir(personDir):
            count += 1
        count += 1
        faceDir = os.path.join(personDir, str(count) + ".jpg")
        faceImg = cv2.resize(faceImg, (200,200))
        cv2.imwrite(faceDir, faceImg)

if __name__=="__main__":
    img = ImageUtils()
    face =cv2.imread("../../../resources/face/0.jpg")




