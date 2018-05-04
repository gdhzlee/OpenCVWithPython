
import os
import cv2

def sdf():
    faceInfos = []
    [FACE, COUNT] = [], []
    count = 0

    path = "../../../resources/facedatabase"
    for personName in os.listdir(path):

        # 排除文件
        personFile = os.path.join(path, personName)
        if os.path.isfile(personFile):
            continue

        # 记录人脸信息
        faceInfos.append(personName)
        print(personName)
        for face in os.listdir(personFile):
            faceFile = os.path.join(personFile, face)

            if os.path.isdir(faceFile):
                continue

            faceImg = cv2.imread(faceFile)
            if faceImg is None:
                continue

            FACE.append(faceImg)
            COUNT.append(count)

            print("     " + face)

        count += 1

    return [FACE, COUNT], faceInfos

if __name__=="__main__":
    [FACE, COUNT], faceInfos = sdf()

    print(COUNT)
    print(faceInfos)