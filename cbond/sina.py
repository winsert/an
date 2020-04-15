#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询可转债、可交换债、股票的价格信息
__author__ = 'winsert@163.com'

import urllib2

# 用于解析URL页面
def bsObjForm(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read().decode('gbk','ignore')
    return html

# 用于查询转债的价格信息
def getZZ(zz_code):
    msgs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] #[今开,昨收,当前,最高,最低,涨跌幅]
    url = "http://hq.sinajs.cn/list="+zz_code #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp = resp.split(',')
        name = tmp[0]
        msgs[0] = float(tmp[1]) #获取转债今开价格
        msgs[1] = float(tmp[2]) #获取转债昨收价格
        msgs[2] = float(tmp[3]) #获取转债当前价格
        msgs[3] = float(tmp[4]) #获取转债当日最高价
        msgs[4] = float(tmp[5]) #获取转债当日最低价
        msgs[5] = round((msgs[2]/msgs[1] - 1) * 100, 2) #涨跌幅
        #print name, msgs
        return msgs
    except:
        name = "getZZ is error."
        print name, msgs
        return msgs

# 用于计算正股涨跌幅和溢价率
def getZG(zg_code):
    msgs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] #[今开,昨收,当前,最高,最低,涨跌幅]
    url = "http://hq.sinajs.cn/list="+zg_code #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp = resp.split(',')
        name = tmp[0]
        msgs[0] = float(tmp[1]) #获取股票今开价格
        msgs[1] = float(tmp[2]) #获取股票昨收价格
        msgs[2] = float(tmp[3]) #获取股票当前价格
        msgs[3] = float(tmp[4]) #获取股票当日最高价
        msgs[4] = float(tmp[5]) #获取股票当日最低价
        msgs[5] = round((msgs[2]/msgs[1] - 1) * 100, 2) #涨跌幅
        #print name, msgs
        return msgs
    except:
        name = "getZG is error."
        print name, msgs
        return msgs

if __name__ == '__main__':

    #zzcode = raw_input("请输入可转债代码：")
    zgcode = raw_input("请输入股票代码：")
    #msgs = getZZ(zzcode)
    msgs = getZG(zgcode)
    for msg in msgs:
        print msg