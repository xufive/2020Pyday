# -*- coding: utf-8 -*-

# 本代码中的用户名和密码不可用
# 如需测试，请先在https://urs.earthdata.nasa.gov/home注册账号

import re
from requests import request
from requests.cookies import RequestsCookieJar

def get_modis_by_requests():
    # 获取token
    resp = request('GET', 'https://urs.earthdata.nasa.gov/home')
    pt = re.compile(r'.*<input type="hidden" name="authenticity_token" value="(.*)" />.*')
    print(len(resp.text))
    token = pt.findall(resp.text)[0]
    print('token: ', token)
    
    # 登录并保存cookie
    jar = RequestsCookieJar()
    jar.update(resp.cookies)
    url = 'https://urs.earthdata.nasa.gov/login'
    forms = {
        'username': 'xufive',
        'password': '*********',
        'redirect_uri': '', 
        'commit': 'Log+in', 
        'client_id': '', 
        'authenticity_token': token
    }
    resp = request('POST', url, data=forms, cookies=jar)
    jar.update(resp.cookies)
    print('cookie: ', resp.cookies.items())
    
    # 请求下载页面，解析文件下载的url
    url = 'https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/6/MOD13Q1/2019/321/MOD13Q1.A2019321.h00v08.006.2019337235356.hdf'
    resp = request('GET', url, cookies=jar)
    pu = re.compile(r'href="(https://ladsweb.modaps.eosdis.nasa.gov.*hdf)"')
    furl = pu.findall(resp.text)[0]
    furl= furl.replace('&amp;', '&')
    print('furl: ', furl)
    
    # 下载文件并保存
    resp = request('GET', furl, cookies=jar)
    with open('fb/modis_requests.hdf', 'wb') as fp:
        fp.write(resp.content)
    print('OK')

if __name__ == '__main__':
    get_modis_by_requests()
 
