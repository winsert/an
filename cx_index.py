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
def cxIndex(code):
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

def getIndex():

    msg_list =[]
    index_msg = ''

    index = {u'上证50':'sh000016', u'沪深300':'sz399300', u'中证500':'sh000905', u'创业板':'sz399006', u'B股':'sh000003', u'国债':'sh000012'} #要查询的指数代码
    
    for k in index.keys():
        value = index.get(k)
        index_zz = cxIndex(value)
        index_msg = k+' : '+index_zz
        #print index_msg
        msg_list.append(index_msg)

    #print msg_list
    return msg_list
'''
if __name__ == '__main__':

    for msg in getIndex():
        print msg
'''
