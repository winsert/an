#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于查询今日和历史上今日的天气信息

__author__ = 'winsert@163.com'

import urllib2
import datetime
from bs4 import BeautifulSoup


# 用于解析URL页面
def bsObjForm(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read()
    #print html
    return html

def bsObjFormHistory(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read().decode('UTF-8','ignore')
    return html

# 获取历史上的天气信息
def getHistoryWeather(url, month_day):
    resp = bsObjFormHistory(url)
    soup = BeautifulSoup(resp, "html.parser")
    all = soup.find('div', class_="blk_02").find_all('tr')
    for tr in all:
        #print tr.get_text()
        day_list = tr.get_text().splitlines()
        #print day_list
        if month_day in day_list:
            av_high = day_list[2]
            av_low = day_list[3]
            his_high = day_list[5]
            his_low = day_list[6]
            history_weather = u'历史上今日：'+u'\n平均最高温度：'+str(av_high)+u'度'+u'\n平均最低温度：'+str(av_low)+u'度'+u'\n极端最高温度：'+str(his_high)+u'度'+u'\n极端最低温度：'+str(his_low)+u'度'
    return history_weather

# 获取今日天气信息
def getTodayWeather(url):
    resp = bsObjForm(url)
    soup = BeautifulSoup(resp, 'html.parser')
    temp = soup.find('div', class_="tqshow").find('span').get_text()
    status = soup.find('li',class_="cDRed").get_text()
    #wind = soup.find('li', style="height:18px;overflow:hidden").get_text()
    today_weather = u'今日：'+status+u'，气温：'+temp
    #print today_weather
    return today_weather

def getToday():
    today_url = "http://jinan.tianqi.com"
    today_weather_msg = getTodayWeather(today_url)
    #print today_weather_msg

    today = datetime.date.today()
    month_day = str(today.month)+str(today.day)
    history_url = "http://php.weather.sina.com.cn/whd.php?c=1&city=%BC%C3%C4%CF&dpc=1"
    history_weather_msg = getHistoryWeather(history_url, month_day)
    #print history_weather_msg
        
    #print today_weather_msg+u'\n'+history_weather_msg
    return today_weather_msg+u'\n'+history_weather_msg

if __name__ == '__main__':
    getToday()
