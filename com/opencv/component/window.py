# -*- coding:utf-8 -*-
import wx
import cv2
import os
from time import ctime, sleep
from threading import Thread
from com.opencv.component.facerecognizer import *

class MyWindows(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title = "人脸识别系统", size=(1000, 800), style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX))

        # 一、初始化菜单栏
        self._menuBar = wx.MenuBar(style=wx.MB_DOCKABLE)
        self._fileMenu = wx.Menu()
        self._menuItem1 = wx.MenuItem(self._fileMenu, wx.NewId(), text="从本地导入单张图像", kind=wx.ITEM_NORMAL)
        self._menuItem2 = wx.MenuItem(self._fileMenu, wx.NewId(), text="从本地导入视频", kind=wx.ITEM_NORMAL)
        self._menuItem3 = wx.MenuItem(self._fileMenu, wx.NewId(), text="从摄像头导入视频帧", kind=wx.ITEM_NORMAL)
        # 绑定事件
        self.Bind(wx.EVT_MENU, self.importFromLocal, self._menuItem1)
        self.Bind(wx.EVT_MENU, self.importFromVideo, self._menuItem2)
        self.Bind(wx.EVT_MENU, self.importFromCapture, self._menuItem3)
        self._fileMenu.Append(self._menuItem1)
        self._fileMenu.Append(self._menuItem2)
        self._fileMenu.Append(self._menuItem3)
        self._menuBar.Append(self._fileMenu, "文件")
        self.SetMenuBar(self._menuBar)

        # 二、初始化控制版块
        self._controlPanel = wx.Panel(self)
        self._controlPanelSizer = wx.GridBagSizer(0, 0)
        # 按钮
        self._detectButton = wx.Button(self._controlPanel, wx.NewId(), "检测")
        self._controlPanelSizer.Add(self._detectButton, pos=(3, 5), flag=wx.ALL, border=5)
        self._tipText = wx.StaticText(self._controlPanel, label="人脸信息：")
        self._controlPanelSizer.Add(self._tipText, pos=(4, 5), flag=wx.ALL, border=5)
        self._input = wx.TextCtrl(self._controlPanel)
        self._controlPanelSizer.Add(self._input, pos=(5, 5), flag=wx.ALL, border=5)
        self._identifyButton = wx.Button(self._controlPanel, wx.NewId(), "识别")
        self._controlPanelSizer.Add(self._identifyButton, pos=(8, 5), flag=wx.ALL, border=5)
        # 事件绑定
        self._controlPanel.Bind(wx.EVT_BUTTON, self.startDetect, self._detectButton)
        self._controlPanel.Bind(wx.EVT_BUTTON, self.startIdentify, self._identifyButton)

        # 三、初始化布局管理器
        # 初始化控制版块布局管理器
        self._controlPanel.SetSizerAndFit(self._controlPanelSizer)
        # 初始化全局布局管理器
        self._globalSizer = wx.GridBagSizer(0, 0)
        self._globalSizer.Add(self._controlPanel, pos=(0,70),span=(35,30),flag=wx.EXPAND | wx.ALL ,border=4)
        self.SetSizerAndFit(self._globalSizer)

        # 四、初始化成员变量
        # 缓冲图像
        self._imageBuffer = "../../../resources/tem/tem.jpg"

        self._faceDetect = Detect()
        self._faceRecognizar = Recognize()

        # 控制
        """
        0 - 不做任何处理
        1 - 检测
        2 - 识别
       """
        self._control = 0

        # 是否在进行视频线程
        self._vidowThread = None

        # 五、绑定事件
        self.Bind(wx.EVT_CLOSE, self.closeEvent)

    """
        绑定函数
    """
    # 从本地导入单张图像
    def importFromLocal(self, event):
        self._vidowThread = None
        self._control = 0
        dlg = wx.FileDialog(self, message="选择文件",
                            defaultDir=os.getcwd(),
                            wildcard="JPG files (*.jpg)|*.jpg|BMP files (*.bmp)|*.bmp|PNG files (*.png)|*.png",
                            style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()[0]
            print("图像路径：" + str(path))
            try:
                img = cv2.imread(path)
                if img is None:
                    print("img is None")
                    raise Exception
                height, width = img.shape[0:2]
                while height > 800 or width > 700:
                    img = cv2.pyrDown(img)
                    height, width = img.shape[0:2]
                cv2.imwrite(self._imageBuffer, img)
                self.cleanCanvas()
                self.OnPaint()
            except:
                wx.MessageBox("不是标准的图片格式", "消息", wx.OK | wx.ICON_INFORMATION)
            finally:
                dlg.Destroy()

    # 从本地导入视频
    def importFromVideo(self, event):
        self._vidowThread = None
        self._control = 0

        # 读取视频
        dlg = wx.FileDialog(self, message="选择文件",
                            defaultDir=os.getcwd(),
                            wildcard="MP4 files (*.mp4)|*.mp4|RMVB files (*.rmvb)|*.rmvb|AVI files (*.avi)|*.avi|MKV files (*.mkv)|*.mkv",
                            style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()[0]
            print("视频路径: " + str(path))

            try:
               cap =  cv2.VideoCapture(path)
               print(cap.isOpened())
               if cap.isOpened() is False:
                   raise Exception

               # 显示视频帧
               self.cleanCanvas()
               self._vidowThread = Thread(target=self.showVideo,args=(cap,), name="showVideo")
               self._vidowThread.start()
            except:
                wx.MessageBox("不是标准的视频文件", "消息", wx.OK | wx.ICON_INFORMATION)
            finally:
                dlg.Destroy()

    # 从摄像头导入视频帧
    def importFromCapture(self, event):
        self._vidowThread = False
        self._control = 0

        try:
            # 调用摄像头
            cap = cv2.VideoCapture(0)
            if cap.isOpened() is False:
                raise Exception

            # 显示视频帧
            self.cleanCanvas()
            self._vidowThread = Thread(target=self.showVideo, args=(cap,), name="showCap")
            self._vidowThread.start()
        except:
            wx.MessageBox("无法获取摄像头", "消息", wx.OK | wx.ICON_INFORMATION)

    # 开启检测
    def startDetect(self, event):
        input = self._input.GetValue()
        print("输入：" + str(input))
        if input == "":
            wx.MessageBox("请输入人脸信息", "消息", wx.OK | wx.ICON_INFORMATION)
            return

        # 开启检测
        self._control = 1
        self.OnPaint()
    # 开启识别
    def startIdentify(self, event):
        if cv2.imread(self._imageBuffer) is None:
            wx.MessageBox("当前没有图像输入", "消息", wx.OK | wx.ICON_INFORMATION)
            return

        # 开启识别
        self._control = 2
        self.OnPaint()

    # 关闭程序
    def closeEvent(self, event):
        self._vidowThread = None
        self.Destroy()

    """
        内部函数
    """
    def process(self):
        if self._control == 1:
            input = self._input.GetValue()
            print("输入：" + str(input))
            if input == "":
                wx.MessageBox("请输入人脸信息", "消息", wx.OK | wx.ICON_INFORMATION)
                self._control = 0
                return
            imgBuffer = cv2.imread(self._imageBuffer)
            imgBuffer = self._faceDetect.detect(img = imgBuffer,faceInfos=input)
            cv2.imwrite(self._imageBuffer, imgBuffer)
            return
        if self._control == 2:
            imgBuffer = cv2.imread(self._imageBuffer)
            imgBuffer = self._faceRecognizar.recognize(img=imgBuffer)
            cv2.imwrite(self._imageBuffer, imgBuffer)
            return

    # 显示视频
    def showVideo(self, cap):
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if ret is False or self._vidowThread is None:
                    break
                height, width = frame.shape[0:2]
                while height > 800 or width > 700:
                    frame = cv2.pyrDown(frame)
                    height, width = frame.shape[0:2]
                cv2.imwrite(self._imageBuffer, frame)
                self.OnPaint()
                sleep(0.05)
            print("视频完毕")
        except Exception as e:
            print(e)

    def OnPaint(self):
        try:
            self.process()
            dc = wx.ClientDC(self)
            bitImage = wx.Bitmap(self._imageBuffer)
            dc.DrawBitmap(bitImage, 0, 0)
            dc.Destroy()
        except Exception as e:
            print(e)

    def cleanCanvas(self):
        try:
            dc = wx.ClientDC(self)
            dc.Clear()
            dc.Destroy()
        except Exception as e:
            print(e)

if __name__=="__main__":
    app = wx.App()
    myWindow = MyWindows(parent=None, id =wx.NewId())
    myWindow.Show()
    app.MainLoop()
