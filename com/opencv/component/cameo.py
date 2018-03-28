import cv2
from com.opencv.component.managers import *
from com.opencv.component.filters import *

class Cameo(object):
    def __init__(self):

        # 初始化窗口
        self._windowManger = WindowManager("Cameo", self.onKeypress)
        # 初始化视频
        videoCapture = cv2.VideoCapture("../../../resources/video/1.mp4")
        self._captureManager = CaptureManager(videoCapture, self._windowManger, False)
        # 初始化滤波器
        self._curveFilter = BlurFilter()

    def run(self):
        self._windowManger.createWindow()
        while self._windowManger.isWindowCreated:
            # 抓取下一帧
            self._captureManager.enterFrame()
            # 获取下一帧
            frame = self._captureManager.frame
            # 图像处理
            Filters.strokeEdges(frame, frame)
            # self._curveFilter.apply(src=frame, dst=frame)

            # 显示视频
            cv2.imshow("Cameo", frame)
            cv2.waitKey(3000)
            # 对视频进行处理
            self._captureManager.exitFrame()
            # 监听键盘输入
            self._windowManger.processEvents()
            break

    # 获取键盘输入
    def onKeypress(self, keycode):

        """获取键盘输入

        space  -> Take a screenbar
        tab    -> Start/stop recording a screencast
        escape -> Quit
        """
        if keycode == 32: #space
            self._captureManager.writeImage('screenshot.png')
        elif keycode == 9: #tab
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo("screenshot.avi")
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27: # escape
            self._windowManger.destroyWindow()

if __name__ == "__main__":
    Cameo().run()

