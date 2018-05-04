# -*- coding:utf-8 -*-
import wx
import cv2
import os
from time import ctime, sleep
from threading import Thread

class MyWindows(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title = "人脸识别系统", size=(1000, 800), style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX))

        # 一、初始化菜单栏
        menuBar = wx.MenuBar(style=wx.MB_DOCKABLE)
        fileMenu = wx.Menu()
        item1 = wx.MenuItem(fileMenu, wx.NewId(), text= "从本地导入单张图像", kind=wx.ITEM_NORMAL)
        item2 = wx.MenuItem(fileMenu, wx.NewId(), text="从本地导入视频", kind=wx.ITEM_NORMAL)
        item3 = wx.MenuItem(fileMenu, wx.NewId(), text= "从摄像头导入视频帧", kind=wx.ITEM_NORMAL)
        # 绑定事件
        self.Bind(wx.EVT_MENU, self.importFromLocal, item1)
        self.Bind(wx.EVT_MENU, self.importFromVideo, item2)
        self.Bind(wx.EVT_MENU, self.importFromCapture, item3)
        fileMenu.Append(item1)
        fileMenu.Append(item2)
        fileMenu.Append(item3)
        menuBar.Append(fileMenu, "文件")
        self.SetMenuBar(menuBar)

        # 二、初始化控制版块
        control = wx.Panel(self)
        controlSizer = wx.GridBagSizer(0, 0)
        # 按钮
        detect = wx.Button(control, wx.NewId(), "检测")
        controlSizer.Add(detect, pos=(3, 5), flag=wx.ALL, border=5)
        tip = wx.StaticText(control, label="人脸信息：")
        controlSizer.Add(tip, pos=(4, 5), flag=wx.ALL, border=5)
        self._input = wx.TextCtrl(control)
        controlSizer.Add(self._input, pos=(5, 5), flag=wx.ALL, border=5)
        identify = wx.Button(control, wx.NewId(), "识别")
        controlSizer.Add(identify, pos=(8, 5), flag=wx.ALL, border=5)
        # 事件绑定
        control.Bind(wx.EVT_BUTTON, self.startDetect, detect)
        control.Bind(wx.EVT_BUTTON, self.startIdentify, identify)
        # 控制版块-布局管理
        control.SetSizerAndFit(controlSizer)

        # 系统界面-布局管理
        sizer = wx.GridBagSizer(0, 0)
        sizer.Add(control, pos=(0,70),span=(35,30),flag=wx.EXPAND | wx.ALL ,border=5)
        self.SetSizerAndFit(sizer)

        # 缓冲图像
        self._image = "../../../resources/tem/1.jpg"

        # 控制
        # 0 - 不做任何处理
        # 1 - 检测
        # 2 - 识别
        self._control = 0

        # 是否在视频播放
        self._isVideo = False

        # 是否在进行视频线程
        self._thread = False

    """
        绑定函数
    """
    def importFromLocal(self, event):
        print("从本地导入单张图像")
        self._isVideo = False
        self._thread = False
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
                cv2.imwrite(self._image, img)
                self.OnPaint(self)
            except:
                wx.MessageBox("读取图片失败", "消息", wx.OK | wx.ICON_INFORMATION)
            finally:
                dlg.Destroy()

    def importFromVideo(self, event):
        print("从本地导入视频")
        self._thread = False
        sleep(0.05)
        self._thread = True
        self._isVideo = True
        dlg = wx.FileDialog(self, message="选择文件",
                            defaultDir=os.getcwd(),
                            wildcard="MP4 files (*.mp4)|*.mp4|RMVB files (*.rmvb)|*.rmvb|AVI files (*.avi)|*.avi|MKV files (*.mkv)|*.mkv",
                            style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()[0]
            print("视频路径: " + str(path))
            try:
               cap =  cv2.VideoCapture(path)
               if cap.isOpened() is False:
                   raise Exception
               self._thread = Thread(target=self.showVideo,args=(cap,), name="showVideo")
               self._thread.start()
            except:
                wx.MessageBox("读取视频失败", "消息", wx.OK | wx.ICON_INFORMATION)
            finally:
                dlg.Destroy()

    def importFromCapture(self, event):
        print("从摄像头导入视频帧")
        self._thread = False
        sleep(0.05)
        self._thread = True
        self._isVideo = True
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened() is False:
                raise Exception

            self._thread = Thread(target=self.showVideo, args=(cap,), name="showCap")
            self._thread.start()
        except:
            wx.MessageBox("无法获取摄像头", "消息", wx.OK | wx.ICON_INFORMATION)

    def startDetect(self, event):
        print("检测")
        input = self._input.GetValue()
        print("输入：" + str(input))
        if cv2.imread(self._image) is None:
            wx.MessageBox("当前没有图像输入", "消息", wx.OK | wx.ICON_INFORMATION)
            return
        if input == "":
            wx.MessageBox("请输入人脸信息", "消息", wx.OK | wx.ICON_INFORMATION)
            return

        # 开启检测
        self._control = 1

    def startIdentify(self, event):
        print("识别")

        if cv2.imread(self._image) is None:
            wx.MessageBox("当前没有图像输入", "消息", wx.OK | wx.ICON_INFORMATION)
            return

        # 开启识别
        self._control = 2

    """
        内部函数
    """
    def detect(self):

        try:
            img = cv2.imread(self._image)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # face = face_cascade.detectMultiScale(gray, 1.3, 5)
        except:
            pass
        return

    def showVideo(self, cap):
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if ret is False or self._thread is False:
                    break
                height, width = frame.shape[0:2]
                while height > 800 or width > 700:
                    frame = cv2.pyrDown(frame)
                    height, width = frame.shape[0:2]
                cv2.imwrite(self._image, frame)
                self.OnPaint(self)
                sleep(0.05)
            print("视频完毕")
        except:
            pass

    def OnPaint(self, event):
        try:
            dc = wx.ClientDC(self)
            if self._isVideo is False:
                dc.Clear()
            bitImage = wx.Bitmap(self._image)
            dc.DrawBitmap(bitImage, 0, 0)
        except:
            pass

if __name__=="__main__":
    app = wx.App()
    myWindow = MyWindows(parent=None, id =wx.NewId())
    myWindow.Show()
    app.MainLoop()
