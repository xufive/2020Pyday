# -*- coding: utf-8 -*-

import time, json, requests
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

plt.rcParams['font.sans-serif'] = ['FangSong']  # 设置默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时'-'显示为方块的问题

def get_day_list():
    """获取每日数据"""
    
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
    data = json.loads(requests.get(url=url).json()['data'])['chinaDayList']
    return [(item['date'], item['confirm']) for item in data]

def fit_exp():
    """拟合"""
    
    def func(x, a, b):
        return np.power(a, (x+b)) # 指数函数y = a^(x+b)
        
    _date, _y = zip(*get_day_list())
    _x = np.arange(len(_y))
    x = np.arange(len(_y)+1)
    
    fita, fitb = optimize.curve_fit(func, _x, _y, (2,0))
    y = func(x, fita[0], fita[1]) # fita即为最优拟合参数
    
    plt.plot(_date, _y, label='原始数据')
    plt.plot(x, y, label='$%0.3f^{x+%0.3f}$'%(fita[0], fita[1]))
    plt.legend(loc='upper left')
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    plt.grid(linestyle=':') # 显示网格
    plt.show()

if __name__ == '__main__':
    fit_exp()
    
    