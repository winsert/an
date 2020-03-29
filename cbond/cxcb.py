#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询可转债、可交换债的最新价是否满足高从折扣和三线条件的模块
__author__ = 'winsert@163.com'

import urllib2
from readcb import readCB #读出 code=3(持仓) 可转债,可交换债的所有信息

# 用于解析URL页面
def bsObjForm(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read().decode('gbk','ignore')
    return html

# 用于查询转债的价格和涨跌幅
def getZZ(zzcode):
    url = "http://hq.sinajs.cn/list="+zzcode #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp_list = resp.split(',')
        zz_name = tmp_list[0]
        zs_price = float(tmp_list[2]) #获取转债昨收价格
        zz_price = float(tmp_list[3]) #获取转债实时价格
        zz_hprice = float(tmp_list[4]) #获取转债当日最高价
        zz_lprice = float(tmp_list[5]) #获取转债当日最低价
        if abs(zz_hprice - zs_price) > abs(zz_lprice - zs_price):
            zz_zdf = round((zz_hprice/zs_price - 1) * 100, 2) #最大涨幅
        else:
            zz_zdf = round((zz_lprice/zs_price - 1) * 100, 2) #最大跌幅
        #print zz_name, zs_price, zz_hprice, zz_hprice-zs_price, zz_lprice, zz_lprice-zs_price, zz_zdf
        return zz_price, zz_zdf
    except:
        zz_price = 0
        zz_zdf = 0.0
        return zz_price, zz_zdf

# 用于计算正股涨跌幅和溢价率
def getZG(zgcode, zz, zgj):
    key = zgcode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp_list = resp.split(',')
        zs_price = float(tmp_list[2]) #获取正股昨收价格
        zg_price = float(tmp_list[3]) #获取正股实时价格
        zg_zdf = round((zg_price/zs_price - 1) * 100, 2) #涨跌幅
        yjl = round((zz/(100/zgj*zg_price) - 1) * 100, 2) #溢价率
        return zg_zdf, yjl
    except:
        zg_zdf = 1.0
        yjl = 1.0
        print "getZG() is error !"
        return zg_zdf, yjl

# 对可转债数据进行高价折扣和三线分析
def getCB(cblist):
    name = cblist[3] #转债名称
    zzcode = cblist[7]+cblist[5] #前缀+转债代码
    zgcode = cblist[7]+cblist[6] #前缀+正股代码
    HPrice = float(cblist[10]) #原最高价
    LPrice = float(cblist[11]) #最低价
    jian = float(cblist[12]) #建仓价
    jia = float(cblist[13])  #加仓价
    zhong = float(cblist[14]) #重仓价
    zgj = float(cblist[17]) #转股价
        
    zz, zz_zdf = getZZ(zzcode) #查询转债价格和涨跌幅
    newHPrice = HPrice #新最高价初始化
    newLPrice = LPrice #新最低价初始化

    if zz >= 130.00: #进行高价折扣分析
        #if zz > HPrice + 1.0: #比原最高价高1.0元
        if zz > HPrice * 1.01: #比原最高价高1%    
            zg_zdf, yjl = getZG(zgcode, zz, zgj)
            msg = name+u':'+str(zz)+u'>前高价'+str(HPrice)+u'\n正股:'+str(zg_zdf)+'%'+u'，溢价率'+str(yjl)+'%'
            newHPrice = zz #新最高价
        elif HPrice >= 130.0 and zz <= (HPrice-9):
            msg = name+u':'+str(zz)+u'，自最高价下跌超过9元。'
            newHPrice = zz #新最高价
        else:
            msg = 'ok'
            #print name+u" 最新价:"+str(zz)+u"元，原最高价:"+str(HPrice)+u"元不变!\n"
    elif zz > 0 and zz < 130.00: #进行三线分析
        if HPrice > 130.0: #转债价格跌破130.00
            msg = name+u':'+str(zz)+u' < 130元！'
            newHPrice = 130.00 #将最高价重置为130.00
        if zz <= jian and zz < (LPrice - 0.5) and zz > jia : #满足建仓条件
            msg = name+u':新低价'+str(zz)+u',建仓价:'+str(jian)
            newLPrice = zz #新最低价
        elif zz <= jia and zz < (LPrice - 1.0) and zz > zhong : #满足加仓条件
            msg = name+u':新低价'+str(zz)+u',加仓价:'+str(jia)
            newLPrice = zz #新最低价
        elif zz <= zhong and zz< (LPrice * 0.9) and zz > 0: #满足重仓条件
            msg = name+u':新低价'+str(zz)+u',重仓价:'+str(zhong)
            newLPrice = zz #新最低价
        else:
            msg = 'ok'
            #print name+u" 最新价:"+str(zz)+u"元，原最低价:"+str(HPrice)+u"元不变!\n"
    else:
        msg = 'ok'
        print name + u" 停牌！\n"
    
    if msg != 'ok':
        print msg
        print
    
    return msg, newHPrice, newLPrice, zz_zdf

if __name__ == '__main__':

    list3 = readCB(3)
    for cblist in list3:
        msg, newHPrice, newLPrice, zdf = getCB(cblist)
        #print 'newHPrice = ', newHPrice
        #print 'newLPrice = ', newLPrice
        #print 'zz_zdf = ', zdf
        #print