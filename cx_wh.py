#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询外汇的模块

__author__ = 'winsert@163.com'

import urllib2

# 用于解析URL页面
def bsObjForm(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read().decode('gbk','ignore')
    return html

# 用于查询外汇的价格
def getWH():

    wh_dict = {'usdcny':6.72, 'audcny':5.30, 'hkdcny':0.86, 'audusd':0.79, 'eurusd':1.16}
    wh_list = []
    wh_msg = ''

    try:
        for key in wh_dict:
            #print key
            #print wh_dict[key]
            url = "http://hq.sinajs.cn/list=fx_s"+key #生成用于查询的URL
            resp = bsObjForm(url)
            tmp_list = resp.split(',')
            #print tmp_list
            new_price = float(tmp_list[1]) #获取实时价格
            zr_price = float(tmp_list[3]) #获取昨日收盘价
            zdf = round((new_price/zr_price - 1)*100, 3)
            wh_msg = key+u'\n最新价:'+str(round(new_price, 4))+u'  涨跌:'+str(zdf)+' %'
            wh_list.append(wh_msg)

        return wh_list

    except Exception, e:
        print 'getWH ERROR :', e
        wh_list.append(e)
        return wh_list

'''
if __name__ == '__main__':

    msg_list =  getWH()
    for msg in msg_list:
        print msg
'''
