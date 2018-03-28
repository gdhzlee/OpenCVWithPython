import cv2
import numpy as np
import time

"""
CaptureManager类对一些差异进行了抽象，并提供了更高级的接口从获取流中分配图像，再将图像分到一个或多个输出中（如图像文件、视频文件或窗口）
"""
class CaptureManager(object):

    #init初始化构造函数
    def __init__(self, capture, previewWindowManager = None, shouldMirrorPreview = False ):

        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview

        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFilename = None
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None

        self._startTime = None
        self._framesElapsed = 0
        self._fpsEstimate = None

    # setter\getter 方法
    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            # _ 可以代表一个临时变量
            _, retrieve = self._capture.retrieve()
            print("CaptureManager.frame getRetrieve: " + str(_))
            self._frame = retrieve
        return self._frame

    @property
    def isWritingImage(self):
        return self._imageFilename is not None

    @property
    def isWritingVideo(self):
        return self._videoFilename is not None

    #
    def enterFrame(self):
        assert not self._enteredFrame, \
            'previous enterFrame() had no matching exitFrame()'

        if self._capture is not None:
            retval = self._capture.grab()
            self._enteredFrame = retval
            print("CaptureManager.enterFrame _enteredFrame: " + str(retval))

    def exitFrame(self):
        if self.frame is None:
            self._enteredFrame = False
            return

        # 估计帧数率，动态获取fps
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1

        # 是否镜像翻转
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirroredFrame = np.fliplr(self._frame).copy()
                self.previewWindowManager.show(mirroredFrame)
            else:
                self.previewWindowManager.show(self._frame)

        # 输出图片
        if self.isWritingImage:
            cv2.imwrite(self._imageFilename, self._frame)
            self._imageFilename = None

        # 输出视频
        if self.isWritingVideo:
            self._writeVideoFrame()
            self._frame = None
            self._enteredFrame = False

    # 输出图片
    def writeImage(self, filename):
        self._imageFilename = filename

    # 开始输出视频
    def startWritingVideo(self, filename, encoding = cv2.VideoWriter_fourcc("I","4","2","0")):
        self._videoFilename = filename
        self._videoEncoding = encoding

    # 停止输出视频
    def stopWritingVideo(self):
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None

    # 输出视频
    def _writeVideoFrame(self):

        if not self.isWritingVideo:
            return

        # _videoWriter为Null，则初始化VideoWriter
        if self._videoWriter is None:
            # 获取fps
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps == 0.0:
                if self._enteredFrame < 20:
                    return
                else:
                    fps = self._fpsEstimate

            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv2.VideoWriter(self._videoFilename, self._videoEncoding, fps, size)

        self._videoWriter.write(self._frame)


"""窗口管理

"""
class WindowManager(object):

    def __init__(self, windowName, keypressCallback = None):
        self.keypressCallback = keypressCallback

        self._windowName = windowName
        self._isWindowCreated = False

    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    # 创建窗口
    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True

    # 显示窗口
    def show(self, frame):
        cv2.imshow(self._windowName, frame)

    # 关闭窗口
    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False

    #键盘管理
    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            keycode &= 0xFF
            self.keypressCallback(keycode)

