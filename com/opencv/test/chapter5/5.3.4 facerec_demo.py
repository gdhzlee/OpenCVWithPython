import cv2
import os
import sys
import numpy as np

def read_images (path, sz = None) :

    c = 0
    X, Y = [], []

    for filename in os.listdir(path):
        try:
            file_path = os.path.join(path, filename)
            if os.path.isdir(file_path):
                continue

            im = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if sz is not None:
                im = cv2.resize(im, (200, 200))

            X.append(np.asarray(im, dtype=np.uint8))
            Y.append(c)

        except IOError as e:
            print("I/O错误({0}): {1} ".format(e.errno, e.strerror))
        except Exception:
            print("未知错误")
            raise
        c += 1

    return [X, Y]


def face_rec():

    names = ['ZhangXueYou','Katerina','Annia','Catherine', 'Dilraba']
    # if len(sys.argv) < 2:
    #     print("缺少参数 </path/to/images>"
    #           "[</path/to/store/images/at>]")
    #     sys.exit()

    [X, Y] = read_images("../../../../resources/face")
    y = np.asarray(Y, dtype=np.int32)

    # if len(sys.argv) == 3:
    #     out_dir = sys.argv[2]

    # 需要安装opencv_contrib模块
    model = cv2.face.FisherFaceRecognizer_create()
    model.train(np.asarray(X), np.asarray(y))

    face_cascade = cv2.CascadeClassifier("../../cascades/haarcascade_frontalface_default.xml")
    img = cv2.imread("../../../../resources/image/13.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img.copy(), (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi = gray[y:(y+h), x:(x+w)]
        try:
            roi = cv2.resize(roi, (200, 200), interpolation=cv2.INTER_LINEAR)
            params = model.predict(roi)
            print("Label: {0}, Confidence: {1}".format(params[0], params[1]))

            # print(names[params[0]])
            cv2.putText(img, str(names[params[0]]), (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
        except Exception as e:
            print(e)
            continue

    cv2.imshow("faces", cv2.pyrDown(img))
    cv2.waitKey(0)

if __name__ == "__main__":

    # read_images("../../../../resources/face")
    face_rec()