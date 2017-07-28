#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询PM2.5数据的模块。

__author__ = 'Andy'

import requests, lxml
from bs4 import BeautifulSoup

# 用于解析URL页面:
def getSoup(url):
    soup_url = url 
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    content = requests.get(soup_url, headers=headers) 
    soup = BeautifulSoup(content.text, 'lxml')
    return soup

# 获取PM2.5数据：
def getPM25():

    PM_url = 'http://www.pm25.com/jinan.html'
    soup = getSoup(PM_url)
    #city = soup.find(class_='bi_loaction_city')  # 城市名称
    aqi = soup.find("a", {"class", "bi_aqiarea_num"})  # AQI指数
    quality = soup.select(".bi_aqiarea_right span")  # 空气质量等级
    result = soup.find("div", class_='bi_aqiarea_bottom')  # 空气质量描述

    PM25_msg = u'AQI指数：' + aqi.text + u'\n空气质量：' + quality[0].text + result.text
    print PM25_msg

    return PM25_msg

if __name__ == '__main__':
    print getPM25()
