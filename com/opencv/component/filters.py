import cv2
import numpy as np
from com.opencv.component import utils

class Filters(object):
    def strokeEdges(src, dst, blurKsize = 7, edgeKsize = 5):

        if blurKsize >= 3:
            blurredSrc = cv2.medianBlur(src, blurKsize)
            graySrc = cv2.cvtColor(blurredSrc, cv2.COLOR_BGR2GRAY)
        else:
            graySrc = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

        cv2.Laplacian(graySrc, cv2.CV_8U, graySrc, ksize = edgeKsize)
        normalizedInverseAlpha = (1.0 / 255) * (255 - graySrc)
        channels = cv2.split(src)
        for channel in channels:
            channel[:] = channel * normalizedInverseAlpha
        cv2.merge(channels, dst)

# 卷积滤波器
class VConvolutionFilter(object):

    def __init__(self, kernel):
        self._kernel = kernel

    def apply(self, src, dst):
        # 第二个参数为位深度，当为-1即表示目标图像和原图像有同样的位深度
        cv2.filter2D(src, -1, self._kernel, dst)

# 锐化滤波器
class SharpenFilter(VConvolutionFilter):

    def __init__(self):
        kernel = np.array([[-1, -1, -1],
                           [-1,  9, -1],
                           [-1, -1, -1]])
        VConvolutionFilter.__init__(self, kernel)

# 边缘检测滤波器
class FindEdgesFilter(VConvolutionFilter):

    def __init__(self):
        kernel = np.array([[-1, -1, -1],
                           [-1,  8, -1],
                           [-1, -1, -1]])
        VConvolutionFilter.__init__(self, kernel)

# 模糊滤波器
class BlurFilter(VConvolutionFilter):

    def __init__(self):
        kernel = np.array([[0.04, 0.04, 0.04, 0.04, 0.04, ],
                           [0.04, 0.04, 0.04, 0.04, 0.04, ],
                           [0.04, 0.04, 0.04, 0.04, 0.04, ],
                           [0.04, 0.04, 0.04, 0.04, 0.04, ],
                           [0.04, 0.04, 0.04, 0.04, 0.04, ]])
        VConvolutionFilter.__init__(self, kernel)

# 模糊和锐化滤波器
class EmbossFilter(VConvolutionFilter):

    def __init__(self):
        kernel = np.array([[-2, -1, 0],
                          [-1,  1, 1],
                          [ 0,  1, 2]])
        VConvolutionFilter.__init__(self, kernel)