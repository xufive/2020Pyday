# -*- coding: utf-8 -*-

import wx
import numpy as np
from PIL import Image

from wxgl.scene import *
from wxgl.colormap import *

class mainFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''
    
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '地球模型上的2019-nCoV疫情地图', style=wx.DEFAULT_FRAME_STYLE)
        self.Maximize()
        
        # 从等经纬地图上读取经纬度网格上的每一个格点的颜色
        c = np.array(Image.open('fb/CoV10_etopo.png'))/255
        
        # 生成和等经纬地图分辨率一致的经纬度网格，计算经纬度网格上的每一个格点的空间坐标(x,y,z)
        lats, lons = np.mgrid[np.pi/2:-np.pi/2:complex(0,c.shape[0]), 0:2*np.pi:complex(0,c.shape[1])]
        x = np.cos(lats)*np.cos(lons)
        y = np.cos(lats)*np.sin(lons)
        z = np.sin(lats)
        
        self.scene = WxGLScene(self, r"C:\Windows\Fonts\simfang.ttf", bg=[0,0,0,0])
        self.scene.setPosture(elevation=0, azimuth=120, save=True)
        self.master = self.scene.addRegion((0,0,1,1))
        self.master.drawMesh('earth', x, y, z, c)
        self.master.update()
        
class mainApp(wx.App):
    def OnInit(self):
        self.Frame = mainFrame()
        self.Frame.Show()
        return True

if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
