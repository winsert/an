#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询CB正股价格的模块

__author__ = 'winsert@163.com'

import sqlite3, urllib2

# 用于解析URL页面
def bsObjForm(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read().decode('gbk','ignore')
    return html

# 用于查询正股的价格
def getZG(zgCode):
    key = zgCode
    try:
        url1 = "http://hq.sinajs.cn/list=sz"+key #生成用于查询沪市的URL
        resp1 = bsObjForm(url1)
        tmp1 = resp1.split(',')
        url2 = "http://hq.sinajs.cn/list=sh"+key #生成用于查询深市的URL
        resp2 = bsObjForm(url2)
        tmp2 = resp2.split(',')

        if len(tmp1) == 1 and len(tmp2) == 1:
            zg_name = u'股票不存在' #获取股票名称
            zg_price = '0.0'
            zg_zdf = '0.0'
            return zg_name, zg_price, zg_zdf
        elif len(tmp1) == 1:
            tmp = tmp2
        else:
            tmp = tmp1

        if float(tmp[3]) == 0.0:
            zg_name = tmp[0] #获取股票名称
            zg_price = u'停牌'
            zg_zdf = '0.0'
        else:
            zg_name = tmp[0] #获取股票名称
            zgzr_price = float(tmp[2]) #获取正股昨日收盘价
            zg_new = float(tmp[3]) #获取正股最新价格
            zg_zdf = str(round((zg_new/zgzr_price)*100, 2) -100)
            zg_price = str(zg_new)
        return zg_name[-4:], zg_price, zg_zdf

    except Exception, e:
        print e
        zg_name = e
        zg_price = '0.0'
        zg_zdf = '0.0'
        return zg_name, zg_price, zg_zdf

'''
if __name__ == '__main__':

    stock = raw_input('请输入股票代码:')
    zg_name, zg_new, zg_zdf =  getZG(stock)
    print zg_name, zg_new, zg_zdf
'''
