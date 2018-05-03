import wx
import cv2

# class MyPanel(wx.Panel):
#
#     def __init__(self):
#         wx.Panel.__init__(self)
#         # # 视图
#         self.image = wx.Image("../../../resources/image/4.jpg")
#         self.bitImage = self.image.ConvertToBitmap()
#         self.Bind(wx.EVT_PAINT, self.OnPaint)
#
#         dc = wx.ClientDC(self)
#         dc.DrawBitmap(self.bitImage, 30, 30, True)
#
#     def OnPaint(self, event):
#         dc = wx.PaintDC(self)
#         dc.DrawBitmap(self.bitImage, 30, 30, True)

class MyWindows(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title = "人脸识别系统", size=(1000, 800))

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0,0)

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


        # 按钮
        # tc4 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        panel1 = wx.Panel(self)
        sizer.Add(panel1, pos=(0, 0), span=(35,70), flag=wx.EXPAND | wx.ALL, border=5)
        panel2 = wx.Panel(self)
        sizer.Add(panel2, pos=(0,78),span=(1,12),flag=wx.EXPAND | wx.ALL ,border=5)
        panel3 = wx.Panel(self)
        sizer.Add(panel3, pos=(35, 0), span=(2, 0), flag=wx.EXPAND | wx.ALL, border=5)

        # identify1 = wx.Button(panel1, wx.NewId(), "识别1")
        # sizer.Add(identify1, pos=(0, 20), flag=wx.ALL, border=5)

        detect = wx.Button(panel1, wx.NewId(), "检测")
        sizer.Add(detect, pos=(2, 78), flag=wx.ALL, border=5)

        tip = wx.StaticText(panel1, label="人脸信息：")
        sizer.Add(tip, pos=(3, 78), flag=wx.ALL, border=5)
        tc = wx.TextCtrl(panel1)
        sizer.Add(tc, pos=(4, 78), flag=wx.ALL, border=5)

        identify = wx.Button(panel1, wx.NewId(), "识别")
        sizer.Add(identify, pos=(8, 78), flag=wx.ALL, border=5)

        panel.Bind(wx.EVT_BUTTON, self.detect, detect)
        panel.Bind(wx.EVT_BUTTON, self.identify, identify)

        panel.SetSizerAndFit(sizer)

        # # # 视图
        # panel1.Bind(wx.EVT_ERASE_BACKGROUND, self.OnPaint)


    def importFromLocal(self, event):
        print("从本地导入单张图像")

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
        bitImage = wx.Bitmap("../../../resources/image/4.jpg")
        dc = wx.ClientDC(self)
        dc.DrawBitmap(bitImage, 30, 30, True)

if __name__=="__main__":
    app = wx.App()
    # # 视图
    # image = wx.Image("../../../resources/image/4.jpg")
    # bitImage = image.ConvertToBitmap()
    myWindow = MyWindows(parent=None, id =wx.NewId())
    myWindow.Show()
    app.MainLoop()

