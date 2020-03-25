#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于计算转债的强赎天数

__author__ = 'winsert@163.com'

import sqlite3, urllib2
from datetime import datetime

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
        zg_zdf = 0.0
        return zg_price

# 用于查询转债的价格
def getZZ(zzCode):
    key = zzCode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    resp = bsObjForm(url)
    tmp_list = resp.split(',')
    zz_price = float(tmp_list[3]) #获取正股实时价格
    return zz_price

# 主程序
def getQS():
    msglist = []
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.execute("select Code, zgcode, Prefix, zgqsr, zgj, qs, qss, name, position from cb")
        for row in curs:
            code = row[0]
            zzcode = row[2]+row[0] #前缀+转债代友
            zgcode = row[2]+row[1] #前缀+正股代码
            prefix = row[2] #前缀
            zgqsr = row[3] #转股起始日
            zgj = float(row[4]) #转股价
            qs = row[5] #已强赎天数
            qss = row[6] #30天记数
            name = row[7]
            position = row[8]

            y = zgqsr.split('-') #转换为日期格式
            d = datetime(int(y[0]), int(y[1]), int(y[2]), 0, 0)

            if datetime.now() >= d and prefix != 'QS' and position > 0:
                zg = getZG(zgcode) #查询正股价格
                zz = getZZ(zzcode) #查询转债价格

                if zg > 0 and zz > 0:
                    qsl = round((zg/zgj), 2) #计算强赎率

                    if qsl > 1.3 and qs < 15 and qss >= 1:
                        nqs = qs + 1
                        nqss = qss -1
                        conn.execute("UPDATE cb SET qs = %r, qss = %r where Code = %s" % (nqs, nqss, code))
                        msg = name+u'\n已强赎'+str(nqs)+u'天,剩余天数:'+str(nqss)+u'天。'
                        msglist.append(msg)
                    elif qsl > 1.3 and qs >= 15 and qss >= 0:
                        #conn.execute("UPDATE cb SET prefix = 'QS' where Code = %s" % code)
                        msg = name+u' 已完成强赎!!!'
                        msglist.append(msg)
                    elif qsl < 1.3 and qs >= 1 and qss >= 1:
                        nqss = qss -1
                        conn.execute("UPDATE cb SET qss = %r where Code = %s" % (nqss, code))
                        msg = name+u'\n已强赎'+str(qs)+u'天,剩余天数:'+str(nqss)+u'天。'
                        msglist.append(msg)

                if qss == 0 :
                    nqs = 0
                    nqss = 30
                    conn.execute("UPDATE cb SET qs = %r, qss = %r where Code = %s" % (nqs, nqss, code))
                    msg = name+u' 强赎失败'
                    msglist.append(msg)

        conn.commit()
        curs.close()
        conn.close()
        return msglist

    except Exception, e:
        print e
        msg = e
        msglist.append(msg)
        return msglist

if __name__ == '__main__':
    
    msglist = getQS()
    for msg in msglist:
        print msg
