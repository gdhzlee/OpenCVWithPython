
import cv2
import wx

class MyFrame(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, '人脸识别系统', size=(500,400))

        # 按键
        panel = wx.Panel(self)
        button1  = wx.Button(panel, label="检测", pos=(370, 100))
        button2 = wx.Button(panel, label="识别", pos=(370, 200))
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button1)

        # 菜单
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()

        item1 = wx.MenuItem(fileMenu, wx.NewId(), text="导入单张图像",kind=wx.ITEM_NORMAL)
        item2 = wx.MenuItem(fileMenu, wx.NewId(), text="导入视频图像",kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.OnCloseMe, item1)
        # self.Bind(wx.EVT_MENU, self.OnCloseMe. item2)
        fileMenu.AppendItem(item1)
        fileMenu.AppendItem(item2)
        menuBar.Append(fileMenu, "&文件")
        self.SetMenuBar(menuBar)

    def OnCloseMe(self, event):
        self.Close(True)

if __name__=='__main__':
    app = wx.App()
    frame = MyFrame(parent=None, id=1)
    frame.Show()
    app.MainLoop()