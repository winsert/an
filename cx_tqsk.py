#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询天气实况信息的模块。

__author__ = 'Andy'

import requests, lxml, os, sys
from bs4 import BeautifulSoup

# 用于解析URL页面:
def getSoup(url):
    soup_url = url 
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    content = requests.get(soup_url, headers=headers) 
    soup = BeautifulSoup(content.text, 'lxml')
    return soup

# 获取天气实况:
def getWeather():
    weather_url = "http://jnqx.jinan.gov.cn/jnszfqxj/front/zdz/list.do?type=1"
    soup = getSoup(weather_url)
    result = soup.find('div', align="center").find_all('td')

    wlist = []
    for w in result:
        wlist.append(w.get_text())

    #print wlist[18]

    weather_msg = u'地点：'+wlist[16].strip().strip('\n').strip('\t').strip('\r')+u'\n时间：'+wlist[17]+u'\n温度：'+wlist[18].strip().strip('.')+u'℃'+u'\n湿度：'+wlist[19].strip()+u'％'+u'\n风向：'+wlist[20]+u'\n风速：'+wlist[21].strip()+u'm/s'+u'\n雨量：'+wlist[22].strip()+u'mm/h'+u'\n气压：'+wlist[23].strip()+u'hPa'+'\n'
    print weather_msg

    return weather_msg
'''
if __name__ == '__main__':
    print getWeather()
'''
