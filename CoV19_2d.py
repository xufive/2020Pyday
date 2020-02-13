# -*- coding: utf-8 -*-

import time
import json
import requests
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.figure
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams['font.sans-serif'] = ['FangSong']  # 设置默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时'-'显示为方块的问题

def catch_daily():
    """抓取每日确诊和死亡数据"""
    
    date_list = list() # 日期
    confirm_list = list() # 确诊
    suspect_list = list() # 疑似
    dead_list = list() # 死亡
    heal_list = list() # 治愈
    
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
    for item in json.loads(requests.get(url=url).json()['data'])['chinaDayList']:
        month, day = item['date'].split('.')
        date_list.append(datetime.strptime('2020-%s-%s'%(month, day), '%Y-%m-%d'))
        confirm_list.append(int(item['confirm']))
        suspect_list.append(int(item['suspect']))
        dead_list.append(int(item['dead']))
        heal_list.append(int(item['heal']))
    
    return date_list, confirm_list, suspect_list, dead_list, heal_list

def catch_distribution():
    """抓取行政区域确诊分布数据"""
    
    data = {}
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
    for item in json.loads(requests.get(url=url).json()['data'])['areaTree'][0]['children']:
        if item['name'] not in data:
            data.update({item['name']:0})
        for city_data in item['children']:
            data[item['name']] += int(city_data['total']['confirm'])
    
    return data

def plot_daily():
    """绘制每日确诊和死亡数据"""
    
    date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily() # 获取数据
    
    plt.figure('2019-nCoV疫情统计图表', facecolor='#f4f4f4', figsize=(10, 8))
    plt.title('2019-nCoV疫情曲线', fontsize=20)
    
    plt.plot(date_list, confirm_list, label='确诊')
    plt.plot(date_list, suspect_list, label='疑似')
    plt.plot(date_list, dead_list, label='死亡')
    plt.plot(date_list, heal_list, label='治愈')
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d')) # 格式化时间轴标注
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    plt.grid(linestyle=':') # 显示网格
    plt.legend(loc='best') # 显示图例
    plt.savefig('fb/2019-nCoV疫情曲线.png') # 保存为文件
    plt.show()

def plot_distribution(mode='lcc', plot_name=True):
    """绘制行政区域确诊分布数据
    
    mode        - 投影模式，可选项：
                -- 'lcc'            兰博托投影
                -- 'ortho'          正射投影
                -- 'etopo'          全球等经纬投影模式，etopo风格
                -- 'shadedrelief'   全球等经纬投影模式，shadedrelief风格
                -- 'bluemarble'     全球等经纬投影模式，bluemarble风格
    plot_name   - 是否打印行政区域名
    """
    
    data = catch_distribution()
    
    font_14 = FontProperties(fname='res/simsun.ttf', size=14)
    font_11 = FontProperties(fname='res/simsun.ttf', size=11)
    
    if mode in ['etopo', 'shadedrelief', 'bluemarble']:
        width = 3000
        height = 1600
        rect = [0, 0, 1, 1]
        lat_min = -90
        lat_max = 90
        lon_min = 0
        lon_max = 360
    else:
        width = 3000
        height = 1500
        rect = [0.1, 0.12, 0.8, 0.8]
        lat_min = 0
        lat_max = 60
        lon_min = 77
        lon_max = 140
    
    handles = [
            matplotlib.patches.Patch(color='#ffaa85', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#ff7b69', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#bf2121', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#7f1818', alpha=1, linewidth=0),
]
    labels = [ '1-9人', '10-99人', '100-999人', '>1000人']
    
    provincePos = {
        "辽宁省":[121.7,40.9],
        "吉林省":[124.5,43.5],
        "黑龙江省":[125.6,46.5],
        "北京市":[116.0,39.9],
        "天津市":[117.0,38.7],
        "内蒙古自治区":[110.0,41.5],
        "宁夏回族自治区":[105.2,37.0],
        "山西省":[111.0,37.0],
        "河北省":[114.0,37.8],
        "山东省":[116.5,36.0],
        "河南省":[111.8,33.5],
        "陕西省":[107.5,33.5],
        "湖北省":[111.0,30.5],
        "江苏省":[119.2,32.5],
        "安徽省":[115.5,31.8],
        "上海市":[121.0,31.0],
        "湖南省":[110.3,27.0],
        "江西省":[114.0,27.0],
        "浙江省":[118.8,28.5],
        "福建省":[116.2,25.5],
        "广东省":[113.2,23.1],
        "台湾省":[120.5,23.5],
        "海南省":[108.0,19.0],
        "广西壮族自治区":[107.3,23.0],
        "重庆市":[106.5,29.5],
        "云南省":[101.0,24.0],
        "贵州省":[106.0,26.5],
        "四川省":[102.0,30.5],
        "甘肃省":[103.0,35.0],
        "青海省":[95.0,35.0],
        "新疆维吾尔自治区":[85.5,42.5],
        "西藏自治区":[85.0,31.5],
        "香港特别行政区":[115.1,21.2],
        "澳门特别行政区":[112.5,21.2]
    }
    
    fig = matplotlib.figure.Figure()
    fig.set_size_inches(width/100, height/100) # 设置绘图板尺寸
    axes = fig.add_axes(rect)
    
    if mode == 'lcc': # 兰博托投影模式
        m = Basemap(projection='lcc', llcrnrlon=77, llcrnrlat=14, urcrnrlon=140, urcrnrlat=51, lat_1=33, lat_2=45, lon_0=100, ax=axes)
        
        # 兰博托投影模式，全图
        #m = Basemap(projection='lcc', llcrnrlon=80, llcrnrlat=0, urcrnrlon=140, urcrnrlat=51, lat_1=33, lat_2=45, lon_0=100, ax=axes)
    elif mode == 'ortho': # 正射投影模式
        m = Basemap(projection='ortho', lat_0=36, lon_0=102, resolution='l', ax=axes)
    else: # 全球等经纬投影模式，
        m = Basemap(llcrnrlon=lon_min, urcrnrlon=lon_max, llcrnrlat=lat_min, urcrnrlat=lat_max, resolution='l', ax=axes)
        if mode == 'etopo':
            m.etopo()
        elif mode == 'shadedrelief':
            m.shadedrelief()
        else:
            m.bluemarble()
    
    
    m.readshapefile('res/china-shapefiles-master/china', 'province', drawbounds=True)
    m.readshapefile('res/china-shapefiles-master/china_nine_dotted_line', 'section', drawbounds=True)
    m.drawcoastlines(color='black') # 洲际线
    m.drawcountries(color='black')  # 国界线
    
    if mode in ['etopo', 'shadedrelief', 'bluemarble']:
        m.drawparallels(np.arange(lat_min,lat_max,30), labels=[1,0,0,0]) #画经度线
        m.drawmeridians(np.arange(lon_min,lon_max,30), labels=[0,0,0,1]) #画纬度线
    else:
        m.drawparallels(np.arange(lat_min,lat_max,10), labels=[1,0,0,0]) #画经度线
        m.drawmeridians(np.arange(lon_min,lon_max,10), labels=[0,0,0,1]) #画纬度线
    
    pset = set()
    for info, shape in zip(m.province_info, m.province):
        pname = info['OWNER'].strip('\x00')
        fcname = info['FCNAME'].strip('\x00')
        if pname != fcname: # 不绘制海岛
            continue
        
        for key in data.keys():
            if key in pname:
                if data[key] == 0:
                    color = '#f0f0f0'
                elif data[key] < 10:
                    color = '#ffaa85'
                elif data[key] <100:
                    color = '#ff7b69'
                elif  data[key] < 1000:
                    color = '#bf2121'
                else:
                    color = '#7f1818'
                break
        
        poly = Polygon(shape, facecolor=color, edgecolor=color)
        axes.add_patch(poly)
        
        if plot_name:
            pos = provincePos[pname]
            text = pname.replace("自治区", "").replace("特别行政区", "").replace("壮族", "").replace("维吾尔", "").replace("回族", "").replace("省", "").replace("市", "")
            if text not in pset:
                x,  y = m(pos[0], pos[1])
                axes.text(x,  y, text, fontproperties=font_11, color='#00FFFF')
                pset.add(text)
    
    axes.legend(handles, labels, bbox_to_anchor=(0.5, -0.11), loc='lower center', ncol=4, prop=font_14)
    axes.set_title("2019-nCoV疫情地图", fontproperties=font_14)
    FigureCanvasAgg(fig)
    fig.savefig('fb/2019-nCoV疫情地图_%s.png'%mode)

if __name__ == '__main__':
    #plot_daily()
    #plot_distribution()
    #plot_distribution(mode='ortho', plot_name=False)
    plot_distribution(mode='etopo', plot_name=False)
    #plot_distribution(mode='shadedrelief', plot_name=False)
    #plot_distribution(mode='bluemarble', plot_name=False)
    
 