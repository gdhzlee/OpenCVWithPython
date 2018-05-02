import wx
import cv2

class MyWindows(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title = "人脸识别系统")

        # panel = wx.Panel(self)

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
        detect = wx.Button(self, wx.NewId(), "检测", pos=(450, 100))
        identify = wx.Button(self, wx.NewId(), "识别", pos=(450, 200))
        self.Bind(wx.EVT_BUTTON, self.detect, detect)
        self.Bind(wx.EVT_BUTTON, self.identify, identify)

        # 视图
        # self._image = cv2.imread("../../../resources/image/1.jpg")
        self.image = wx.Image("../../../resources/image/4.jpg")
        print(self.image)
        # win = window1(self, self.image)

        self.bitImage = self.image.ConvertToBitmap()
        print(self.bitImage)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

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

    # def show(self, event):
    #     dc = wx.ClientDC(self)
    #     dc.DrawBitmap(self._image, 400, 400, True)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitImage, 30, 30, True)

class window1(wx.Window):

    def __init__(self, parent, image):
        wx.Window.__init__(self, parent)
        self.image = image.ConvertToBitmap()

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.image, 0, 0, True)

if __name__=="__main__":
    app = wx.App()
    myWindow = MyWindows(parent=None, id =wx.NewId())
    myWindow.Show()
    app.MainLoop()

    image = cv2.imread("../../../resources/image/4.jpg")
    print(image)