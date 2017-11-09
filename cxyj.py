#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询可转债、可交换债的溢价率的模块

__author__ = 'winsert@163.com'

import sqlite3, urllib2

# 用于解析URL页面
def bsObjForm(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read().decode('gbk','ignore')
    return html

# 用于查询指定证券的价格
def getZQ(zqCode):
    key = zqCode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp_list = resp.split(',')
        zq_price = float(tmp_list[3]) #获取证券实时价格
        if zq_price == 0:
            zq_price = float(tmp_list[2]) #获取证券昨日收盘价
        return zq_price
    except:
        zq_price = 0 
        return zq_price

# 从cb.db数据库中提取可转债数据进行实时三线分析
def getYJ():

    msg = []
    yj_msg = ''
    
    conn = sqlite3.connect('cb.db')
    curs = conn.cursor()
    sql = "select name, Code, zgcode, Prefix, zgj from cb" 
    curs.execute(sql)
    tmp = curs.fetchall()
    curs.close()
    conn.close()

    for cc in tmp:
        prefix = cc[3]

        if prefix != 'QS' :  #QS代表已强赎

            name = cc[0] #转债名称
            code = cc[1] #转债代码
            zzcode = cc[3]+cc[1] #前缀+转债代码
            zgcode = cc[3]+cc[2] #前缀+正股代码
            zgj = float(cc[4]) #转股价
            zz = float(getZQ(zzcode)) #查询转债价格
            zg = float(getZQ(zgcode)) #查询正股价格

            if zg != 0: #正股的价格不等于0
                zgjz = (100/zgj)*zg #计算转股价值
                yjl = round((zz-zgjz)/zgjz*100, 2) #计算溢价率

                if yjl < 0.0:
                    yj_msg = name+u" 的溢价率="+str(yjl)+u"%，小于0。"

                    msg.append(yj_msg)

    return msg               

if __name__ == '__main__':
    msg_list = getYJ()

    for msg in msg_list:
        print msg
