#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询正股价格的模块

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
            msg = u'股票不存在'
            return msg
        elif len(tmp1) == 1:
            tmp = tmp2
        else:
            tmp = tmp1

        if float(tmp[3]) == 0.0:
            zg_name = tmp[0] #获取股票名称
	    msg =zg_name[-4:]+u" 停牌了"
	    return msg
        else:
            zg_name = tmp[0][-4:] #获取股票名称
	    zg_kpj = str(tmp[1]) #今日开盘价
            zg_zsp = str(tmp[2]) #昨日收盘价
            zg_new = str(tmp[3]) #今日最新价格
            zg_zdf = str(round((float(tmp[3])/float(tmp[2]))*100, 2) -100) #涨跌幅
	    zg_zgj = str(tmp[4]) #今日最高价
	    zg_zdj = str(tmp[5]) #今日最低价
	    zg_cjl = str(round(float(tmp[8])/1000000.00, 2)) #成交量 百万手
	    zg_cje = str(round((float(tmp[9])/100000000.00), 2)) #成交金额 亿元

	    msg = zg_name+u'\n今日开盘价:'+zg_kpj+u'\n昨日收盘价:'+zg_zsp+u'\n今日最新价:'+zg_new+u'\n今日最高价:'+zg_zgj+u'\n今日最低价:'+zg_zdj+u'\n涨  跌  幅:'+zg_zdf+' %'+u'\n成  交  量:'+zg_cjl+u' 万手'+u'\n成交金额:'+zg_cje+u' 亿元'
        return msg

    except Exception, e:
        print e
        msg = u"查询 "+str(key)+u" 出错了"
	return msg

if __name__ == '__main__':

    stock = raw_input('请输入股票代码:')
    print getZG(stock)
