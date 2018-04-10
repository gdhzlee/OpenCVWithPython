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

    names = ['Joe', 'Jane', 'Jack']
    # if len(sys.argv) < 2:
    #     print("缺少参数 </path/to/images>"
    #           "[</path/to/store/images/at>]")
    #     sys.exit()

    [X, Y] = read_images("../../../../resources/face")
    y = np.asarray(Y, dtype=np.int32)

    # if len(sys.argv) == 3:
    #     out_dir = sys.argv[2]

    # 需要安装opencv_contrib模块
    # cv2.face

if __name__ == "__main__":

    # read_images("../../../../resources/face")
    face_rec()