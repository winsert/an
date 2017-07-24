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

# 用于查询正股的价格
def getWH():

    wh_dict = {'usdcny':6.73, 'audcny':5.30}
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
            wh_price = float(tmp_list[1]) #获取外汇实时价格
            print key+' new price is %r.' % wh_price
            if wh_price < wh_dict[key]:
                wh_msg = key+' new price is %r, < %r !' %(wh_price, wh_dict[key])
                #print wh_msg
                wh_list.append(wh_msg)

        return wh_list

    except Exception, e:
        print 'getWH ERROR :', e
        wh_list.append(e)
        return wh_list

'''
if __name__ == '__main__':

    msg_list =  getWH()
    if len(msg_list) == 0 :
        print 'Everthing is OK !'
    else:
        for msg in msg_list:
            print msg
'''
