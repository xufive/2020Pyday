# -*- coding: utf-8 -*-

import os, time, json, requests
import multiprocessing as mp
from apscheduler.schedulers.blocking import BlockingScheduler

def data_obtain():
    """获取数据"""
    
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
    with open('fb/ncp.txt', 'w') as fp:
        fp.write(requests.get(url=url).json()['data'])
    
    print('Obtain OK')

def data_process():
    """处理数据"""
    
    while True:
        if os.path.isfile('fb/ncp.txt'):
            with open('fb/ncp.txt', 'r') as fp:
                data = json.loads(fp.read())
            
            with open('fb/ncp.csv', 'w') as fp:
                for p in data['areaTree'][0]['children']:
                    fp.write('%s,%d,%d,%d,%d\n'%(p['name'], p['total']['confirm'], p['total']['suspect'], p['total']['dead'], p['total']['heal']))
            
            os.remove('fb/ncp.txt')
            print('Process OK')
        else:
            print('No data file')
        
        time.sleep(10)

if __name__ == '__main__':
    # 创建并启动数据处理子进程
    p_process = mp.Process(target=data_process) # 创建数据处理子进程
    p_process.daemon = True  # 设置子进程为守护进程
    p_process.start() # 启动数据处理子进程
    
    # 创建调度器
    scheduler = BlockingScheduler() 
    
    # 添加任务
    scheduler.add_job(
        data_obtain,            # 获取数据的任务
        trigger = 'cron',       # 设置触发器为cron     
        minute = '*/1',         # 设置每分钟执行一次
        misfire_grace_time = 30 # 30秒内没有执行此job，则放弃执行
    )
    
    # 启动调度服务
    scheduler.start() 