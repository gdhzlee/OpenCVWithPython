import wx
import cv2
import os

class MyWindows(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title = "人脸识别系统", size=(1000, 800))

        # 菜单栏
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        item1 = wx.MenuItem(fileMenu, wx.NewId(), text= "从本地导入单张图像", kind=wx.ITEM_NORMAL)
        item2 = wx.MenuItem(fileMenu, wx.NewId(), text="从本地导入视频", kind=wx.ITEM_NORMAL)
        item3 = wx.MenuItem(fileMenu, wx.NewId(), text= "从摄像头导入视频帧", kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.importFromLocal, item1)
        self.Bind(wx.EVT_MENU, self.importFromVideo, item2)
        self.Bind(wx.EVT_MENU, self.importFromCapture, item3)
        fileMenu.Append(item1)
        fileMenu.Append(item2)
        fileMenu.Append(item3)
        menuBar.Append(fileMenu, "文件")
        self.SetMenuBar(menuBar)

        # 显示模块
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        # 控制模块
        control = wx.Panel(self)
        controlSizer = wx.GridBagSizer(0, 0)
        # 按钮
        detect = wx.Button(control, wx.NewId(), "检测")
        controlSizer.Add(detect, pos=(3, 5), flag=wx.ALL, border=5)
        tip = wx.StaticText(control, label="人脸信息：")
        controlSizer.Add(tip, pos=(4, 5), flag=wx.ALL, border=5)
        tc = wx.TextCtrl(control)
        controlSizer.Add(tc, pos=(5, 5), flag=wx.ALL, border=5)
        identify = wx.Button(control, wx.NewId(), "识别")
        controlSizer.Add(identify, pos=(8, 5), flag=wx.ALL, border=5)
        # 事件绑定
        control.Bind(wx.EVT_BUTTON, self.detect, detect)
        control.Bind(wx.EVT_BUTTON, self.identify, identify)
        # 控制模块布局器
        control.SetSizerAndFit(controlSizer)

        # 全局布局器
        sizer = wx.GridBagSizer(0, 0)
        sizer.Add(control, pos=(0,70),span=(35,30),flag=wx.EXPAND | wx.ALL ,border=5)
        self.SetSizerAndFit(sizer)

        #
        self._image = "../../../resources/image/6.jpg"

    def importFromLocal(self, event):
        print("从本地导入单张图像")
        dlg = wx.FileDialog(self, message=u"选择文件",
                            defaultDir=os.getcwd(),
                            defaultFile="",
                            wildcard="",
                            style=0)

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print(paths)
            for path in paths:
                print(path)
                self._image = path
        self.OnPaint(self)
        dlg.Destroy()

    def importFromVideo(self, event):
        # self.show(self, event)
        print("从本地导入视频")

    def importFromCapture(self, event):
        print("从摄像头导入视频帧")

    def detect(self, event):
        print("检测")

    def identify(self, event):
        print("识别")

    def OnPaint(self, event):
        dc = wx.ClientDC(self)
        # 按比例缩小
        try:
            img = cv2.imread(self._image)
            if img is None:
                print("打不开图像")
            height, width = img.shape[0:2]
            while(height > 800 or width > 700):
                img = cv2.pyrDown(img)
                height, width = img.shape[0:2]
            cv2.imwrite(self._image, img)
            print("保存图片成功")
            bitImage = wx.Bitmap(self._image)
            print("读取图片成功")
            dc.DrawBitmap(bitImage,0,0)

        except Exception as e:
            print(e)
            wx.MessageBox("打不开图片", "消息", wx.OK | wx.ICON_INFORMATION)

if __name__=="__main__":
    app = wx.App()
    myWindow = MyWindows(parent=None, id =wx.NewId())
    myWindow.Show()
    app.MainLoop()

