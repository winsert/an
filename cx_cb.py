#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于获取可转债、可交换债的最新价，三线价格，回售价等数据

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
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    resp = bsObjForm(url)
    tmp_list = resp.split(',')
    zg_price = float(tmp_list[3]) #获取正股实时价格
    return zg_price

# 用于查询转债的价格
def getZZ(zzCode):
    key = zzCode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp_list = resp.split(',')
        zz_price = float(tmp_list[3]) #获取正股实时价格
        return zz_price
    except:
        zz_price = 0 
        return zz_price

# 主程序
def getCB():

    msg = []
    zz_msg = ''
    
    conn = sqlite3.connect('cb.db')
    curs = conn.cursor()
    sql = "select name, Code, zgcode, Prefix, position, jian, jia, zhong, zgj from cb" 
    curs.execute(sql)
    tmp = curs.fetchall()
    curs.close()
    conn.close()

    for cc in tmp:
        #print cc
        #zgcode = cc[3]+cc[2] #前缀+正股代码
        #zg = float(getZG(zgcode)) #查询正股价格
        zzcode = cc[3]+cc[1] #前缀+转债代码
        position = cc[4]
        jian = float(cc[5])
        jia = float(cc[6])
        zhong = float(cc[7])
        zz = float(getZZ(zzcode)) #查询转债价格
        #zgj = float(cc[8]) #转股价
        #zgjz = (100/zgj)*zg #计算转股价值
        #yjl = round((zz-zgjz)/zgjz*100, 2) #计算溢价率

        if zz == 0.0:
            zz_msg = cc[0]+u': '+str(position)+u'张'+u'\n最新价:'+u'停牌'
        elif zz > jian:
            zz_msg = cc[0]+u': '+str(position)+u'张'+u'\n最新价:'+str(zz)
        elif zz <= jian and zz > jia:
            zz_msg = cc[0]+u': '+str(position)+u'张'+u'\n最新价:'+str(zz)+u'  建仓价:'+str(jian)
            msg.append(zz_msg)
        elif zz <= jia and zz > zhong:
            zz_msg = cc[0]+u': '+str(position)+u'张'+u'\n最新价:'+str(zz)+u'  加仓价:'+str(jia)
            msg.append(zz_msg)
        elif zz <= zhong:
            zz_msg = cc[0]+u':\n'+u'最新价:'+str(zz)+u'  重仓价:'+str(zhong)
            msg.append(zz_msg)

        #print zz_msg

    #print msg
    return msg
'''
if __name__ == '__main__':
    
    getCB()
'''
