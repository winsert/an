#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 获取证券指数涨跌幅度的模块

__author__ = 'winsert@163.com'

import sqlite3, urllib2

# 用于解析URL页面
def bsObjForm(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read().decode('gbk','ignore')
    return html

#获取证券指数涨跌幅
def getIndex(code):
    key = code
    url = "http://hq.sinajs.cn/list=s_"+key #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp_list = resp.split(',')
        index_price = str(tmp_list[3]) #获取指数的涨跌幅
        #print index_price
        return index_price
    except:
        index_price = '0'
        return index_price

'''
if __name__ == '__main__':
''' 
