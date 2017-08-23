#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询PM2.5数据的模块。

__author__ = 'Andy'

import requests
from bs4 import BeautifulSoup

# 用于解析URL页面:
def getSoup(url):
    soup_url = url 
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    content = requests.get(soup_url, headers=headers) 
    soup = BeautifulSoup(content.text, 'html.parser')
    return soup

# 获取PM2.5数据：
def getPM():

    try:
        tmp = []
        url = 'http://www.pm25.in/rank'
        soup = getSoup(url)
        #print soup
        result = soup.find('tbody').find_all('tr')
        #print result[2].contents

        for x in result:
            #print x.contents[3].string
            if x.contents[3].string == u'济南':
                for y in x.contents:
                    if y.string != '\n':
                        tmp.append(y.string)
        #print tmp
        msg = u'全国排名: '+tmp[0]+u'\n空气质量: '+tmp[3]+'\nAQI         : '+tmp[2]+'\nPM2.5    : '+tmp[5]+'\nPM10     : '+tmp[6]+u'\n一氧化碳: '+tmp[7]+u'\n二氧化氮: '+tmp[8]+u'\n二氧化硫: '+tmp[11]+u'\n臭氧1小时平均:'+tmp[9]+u'\n臭氧8小时平均: '+tmp[10]
        return msg

    except Exception, e:
        print e
        return e

if __name__ == '__main__':
    print getPM()
