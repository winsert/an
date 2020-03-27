#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于计算转债的强赎天数
__author__ = 'winsert@163.com'

import sqlite3, urllib2
from datetime import datetime

from readcb import readCB #读出 code!= 0 的可转债,可交换债的所有信息

# 用于解析URL页面
def bsObjForm(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read().decode('gbk','ignore')
    return html

# 用于查询正股的价格
def getZG(zgCode):
    key = zgCode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp_list = resp.split(',')
        zgzr_price = float(tmp_list[2]) #获取正股昨日收盘价
        zg_price = float(tmp_list[3]) #获取正股最新价格
        zg_zdf = round((zg_price/zgzr_price)*100, 2) -100 
        return zg_price
    except:
        zg_price = 0.0
        return zg_price

# 用于查询转债的价格
def getZZ(zzCode):
    key = zzCode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    resp = bsObjForm(url)
    tmp_list = resp.split(',')
    zz_price = float(tmp_list[3]) #获取转债收盘价
    zz_hprice = float(tmp_list[4]) #获取转债当日最高价
    zz_lprice = float(tmp_list[5]) #获取转债当日最低价
    return zz_price, zz_hprice, zz_lprice

#对cb.db中HPrice(最高价)的值进行修改
def modiHPrice(zzcode, HPrice):
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "UPDATE cb SET HPrice = %r WHERE zzcode = %s" % (HPrice, zzcode) 
        curs.execute(sql)
        conn.commit()
        curs.close()
        conn.close()
    except Exception, e:
        print 'modiHPrice ERROR :', e

#对cb.db中LPrice(最低价)的值进行修改
def modiLPrice(zzcode, LPrice):
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "UPDATE cb SET LPrice = %r WHERE zzcode = %s" % (LPrice, zzcode) 
        curs.execute(sql)
        conn.commit()
        curs.close()
        conn.close()
    except Exception, e:
        print 'modiLPrice ERROR :', e

#对cb.db中qs, qss的值进行修改
def qsDay(nqs, nqss, code):
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "UPDATE cb SET qs = %r, qss = %r where zzcode = %s" % (nqs, nqss, code)
        curs.execute(sql)
        conn.commit()
        curs.close()
        conn.close()
    except Exception, e:
        print 'qsDay ERROR :', e

#对cb.db中qss的值进行修改
def qssDay(nqss, code):
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "UPDATE cb SET qss = %r where zzcode = %s" % (nqss, code)
        curs.execute(sql)
        conn.commit()
        curs.close()
        conn.close()
    except Exception, e:
        print 'qssDay ERROR :', e

# 强赎分析,更新最高价，最低价
def getQS(listCB):
    msglist = []
    try:
        for cblist in listCB:
            name = cblist[3] #转债名称
            code = cblist[5] #转债代码
            zzcode = cblist[7]+cblist[5] #前缀+转债代码
            zgcode = cblist[7]+cblist[6] #前缀+正股代码
            hprice = float(cblist[10]) #原最高价
            lprice = float(cblist[11]) #原最低价
            zgqsr = cblist[16] #转股起始日
            zgj = float(cblist[17]) #转股价
            qs = cblist[25] #已强赎天数
            qss = cblist[26] #30天记数

            zz, zz_hprice, zz_lprice = getZZ(zzcode) #查询转债收盘价,当日最高价,当日最低价

            if zz_hprice > hprice: #更新最高价
                #print name, 'zz_hprice' , zz_hprice, hprice
                modiHPrice(code, zz_hprice)
                msg = name+u' 最高价更新为:'+str(zz_hprice)+u'元。'
                msglist.append(msg)
                
            if zz_lprice < lprice: #更新最低价
                #print name, 'zz_lprice', zz_lprice, lprice
                modiLPrice(code, zz_lprice)
                msg = name+u' 最低价更新为:'+str(zz_lprice)+u'元。'
                msglist.append(msg)

            y = zgqsr.split('-') #转换为日期格式
            d = datetime(int(y[0]), int(y[1]), int(y[2]), 0, 0)

            if datetime.now() >= d:
                zg = getZG(zgcode) #查询正股价格
                
                if zg > 0 and zz > 0:
                    qsl = round((zg/zgj), 2) #计算强赎率

                    if qsl > 1.3 and qs < 15 and qss >= 1:
                        nqs = qs + 1
                        nqss = qss -1
                        qsDay(nqs, nqss, code)
                        msg = name+u' 强赎'+str(nqs)+u'天,剩:'+str(nqss)+u'天。'
                        msglist.append(msg)
                    elif qsl > 1.3 and qs >= 15 and qss >= 0:
                        msg = name+u' 已完成强赎!!!'
                        msglist.append(msg)
                    elif qsl < 1.3 and qs >= 1 and qss >= 1:
                        nqss = qss -1
                        qssDay(nqss, code)
                        msg = name+u' 强赎'+str(qs)+u'天,剩:'+str(nqss)+u'天。'
                        msglist.append(msg)

        return msglist

    except Exception, e:
        print e
        msg = e
        msglist.append(msg)
        return msglist

if __name__ == '__main__':
    
    # code!= 0 的转债列表(非强赎转债)
    listCB = readCB(-1)

    msglist = getQS(listCB)
    for msg in msglist:
        print msg