# -*- coding: utf-8 -*-

# 本代码中的用户名和密码不可用
# 如需测试，请先在https://urs.earthdata.nasa.gov/home注册账号

import os, re
import pycurl
import urllib.parse
from io import BytesIO

def get_modis_by_pycurl():
    # 实例化pycurl，生成对象
    c = pycurl.Curl()
    c.unsetopt(pycurl.CUSTOMREQUEST)
    c.setopt(pycurl.NOSIGNAL, 1)
    
    # 设置访问HTTPS
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    
    # 是否允许重定向
    c.setopt(pycurl.FOLLOWLOCATION, True)
    
    # 使用cookie文件记录登录信息
    cookieFile = 'cookieFile.cookie'
    if os.path.isfile(cookieFile):
        os.remove(cookieFile)
    
    c.setopt(pycurl.COOKIEFILE, cookieFile)
    c.setopt(pycurl.COOKIEJAR, cookieFile)
    
    # 设置服务端应答回调函数
    c.resp_header_buf = BytesIO()
    c.resp_body_buf = BytesIO()
    c.setopt(pycurl.HEADERFUNCTION, c.resp_header_buf.write) # 设置服务端应答head时的回调函数
    c.setopt(pycurl.WRITEFUNCTION, c.resp_body_buf.write) # 设置服务端应答body时的回调函数 
    
    # 取得登录页面
    url = 'https://urs.earthdata.nasa.gov/home'
    c.setopt(pycurl.HTTPGET, True)
    c.setopt(pycurl.URL, url) 
    c.perform()
    body = c.resp_body_buf.getvalue()
    
    # 解析取得token
    pt = re.compile(r'.*<input type="hidden" name="authenticity_token" value="(.*)" />.*')    
    print(len(body))
    token = pt.findall(body.decode('gbk'))[0]
    print('token: ', token)
    
    url = 'https://urs.earthdata.nasa.gov/login'
    forms = {
        "username": "xufive",
        "password": "********",
        "redirect_uri": "",
        "commit": "Log+in",
        "client_id": "",
        "authenticity_token": token
    }
    c.setopt(pycurl.POSTFIELDS, urllib.parse.urlencode(forms))
    c.setopt(pycurl.POST, True)
    c.setopt(pycurl.URL, url)
    c.perform()
    print('login: ', 'OK')
    
    # 设置服务端应答回调函数
    c.resp_header_buf = BytesIO() # 设置访问HTTPS
    c.resp_body_buf = BytesIO() # 设置访问HTTPS
    c.setopt(pycurl.HEADERFUNCTION, c.resp_header_buf.write) # 设置服务端应答head时的回调函数
    c.setopt(pycurl.WRITEFUNCTION, c.resp_body_buf.write) # 设置服务端应答body时的回调函数
    
    # 数据文件下载地址
    url = 'https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/6/MOD13Q1/2019/321/MOD13Q1.A2019321.h00v08.006.2019337235356.hdf'
    
    # 第一次访问下载地址，返回页面中有验证链接
    c.setopt(pycurl.HTTPGET, True)
    c.setopt(pycurl.URL, url)
    c.perform()
    body = c.resp_body_buf.getvalue()
    
    # 解析内容，取得验证用户的链接
    pu = re.compile(r'href="(https://ladsweb.modaps.eosdis.nasa.gov.*hdf)"')        
    urls = pu.findall(body.decode('gbk'))
    temp_url = urls[0].replace('&amp;', '&')
    print ('furl: ', temp_url)
    
    c.setopt(pycurl.FOLLOWLOCATION, False) # 不允许重定向
    c.setopt(pycurl.HTTPGET, True)
    c.setopt(pycurl.URL, temp_url)
    c.perform()
    print (c.getinfo(pycurl.HTTP_CODE))
    
    # 设置服务端应答回调函数
    c.resp_header_buf = BytesIO()# 设置访问HTTPS
    c.resp_body_buf = BytesIO()# 设置访问HTTPS
    c.setopt(pycurl.HEADERFUNCTION, c.resp_header_buf.write) # 设置服务端应答head时的回调函数
    c.setopt(pycurl.WRITEFUNCTION, c.resp_body_buf.write) # 设置服务端应答body时的回调函数
    
    # 下载
    c.setopt(pycurl.HTTPGET, True)
    c.setopt(pycurl.URL, url)
    f = open('fb/modis_pycurl.hdf', 'wb')
    c.setopt(pycurl.WRITEDATA, f) # 应答为文件时，指定流资源
    c.perform()
    c.close()
    print('OK')

if __name__ == '__main__':
    get_modis_by_pycurl()
 
