#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 自动获取可转债、可交换债的最新价是否满足高价折扣法的模块
__author__ = 'winsert@163.com'

import urllib2
from readcb import readCB3 #读出 code=3(持仓) 可转债,可交换债的所有信息

# 用于解析URL页面
def bsObjForm(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read().decode('gbk','ignore')
    return html

# 用于查询指定证券的价格
def getZZ(zzCode):
    key = zzCode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp_list = resp.split(',')
        zz_price = float(tmp_list[3]) #获取证券实时价格
        #print zzCode+u' 当前价：'+str(zz_price)+'\n'
        return zz_price
    except:
        zz_price = 0
        print "getZZ() is error !"
        return zz_price

# 用于计算正股涨跌幅和溢价率
def getZG(zgcode, zz, zgj):
    key = zgcode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp_list = resp.split(',')
        zs_price = float(tmp_list[2]) #获取正股昨收价格
        zg_price = float(tmp_list[3]) #获取正股实时价格
        zdf = round((zg_price/zs_price - 1) * 100, 2) #涨跌幅
        yjl = round((zz/(100/zgj*zg_price) - 1) * 100, 2) #溢价率
        return zdf, yjl
    except:
        zdf = 1.0
        yjl = 1.0
        print "getZG() is error !"
        return zdf, yjl

#从cb.db数据库中提取可转债数据进行"高价折扣法"分析
def getHP(cblist):
    
    try:
        name = cblist[3] #转债名称
        code = cblist[5] #转债代码
        zzcode = cblist[7]+cblist[5] #前缀+转债代码
        zgcode = cblist[7]+cblist[6] #前缀+正股代码
        HPrice = float(cblist[10]) #原最高价
        zgj = float(cblist[17]) #转股价
        zz = float(getZZ(zzcode)) #查询转债价格

        #if zz > HPrice + 1.0: #比原最高价高1.0元
        if zz > HPrice * 1.01: #比原最高价高1%    
            zdf, yjl = getZG(zgcode, zz, zgj)
            msg = name+u':'+str(zz)+u'>前高价'+str(HPrice)+u'\n正股:'+str(zdf)+'%'+u'，溢价率'+str(yjl)+'%'
            newHPrice = zz #新最高价
        elif HPrice > 130.0 and zz < 130.0: #转债价格跌破130.00
            msg = name+u':'+str(zz)+u' < 130元！'
            newHPrice = 130.00 #将最高价重置为130.00
        elif HPrice >= 130.0 and zz <= (HPrice-9) and zz > 130.0:
            msg = name+u':'+str(zz)+u'，自最高价下跌超过9元。'
            newHPrice = zz #新最高价
        else:
            msg = 'ok'
            newHPrice = HPrice

    except Exception,e2:
        print 'getHP ERROR :',e2

    if msg != 'ok':
        print msg
        print
    else:
        print name+u'最高价'+str(newHPrice)+u',不变。\n'

    return msg, newHPrice

if __name__ == '__main__':
    
    list3 = readCB3()
    for cblist in list3:
        msg, newHPrice = getHP(cblist)