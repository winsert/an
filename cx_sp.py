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
def getSP():

    sp_dict = {u'COMEX Gold':'GC', 'COMEX Silver':'SI', 'NYMEX Oil':'CL'}
    sp_list = []
    sp_msg = ''

    try:
        for key in sp_dict:
            value = sp_dict[key]
            url = "http://hq.sinajs.cn/list=hf_"+value #生成用于查询的URL
            resp = bsObjForm(url)
            tmp_list = resp.split(',')
            sp_price = str(tmp_list[2]) #获取外汇实时价格
            sp_zdf = str(round(float(tmp_list[1]), 2)) #获取外汇涨跌幅
            sp_msg = key+u'\n 现价:'+sp_price+u' 涨跌:'+sp_zdf+'%'
            sp_list.append(sp_msg)

        return sp_list

    except Exception, e:
        print 'getSP ERROR :', e
        sp_list.append(e)
        return sp_list
'''

if __name__ == '__main__':

    msg_list =  getSP()
    for msg in msg_list:
        print msg
'''
