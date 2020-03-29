#! /usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于由到期年化收益率计算转债的价格

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
        zg_name = tmp_list[0][-4:]
        zg_price = float(tmp_list[3]) #获取正股最新价格
        if zg_price != 0:
            return zg_price
        else:
            print zg_name + u" 停牌！"
            
    except Exception, e:
        print u'查询正股价的模块报错：'+str(e)

# 用于查询转债的价格
def getZZ(zzCode):
    key = zzCode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    resp = bsObjForm(url)
    tmp_list = resp.split(',')
    if len(tmp_list) < 3:
        zz_price = 100
    else:
        zz_price = float(tmp_list[3]) #获取转债实时价格
    
    if zz_price == 0:
        zz_price = float(tmp_list[2]) #获取转债昨日收盘价
        return zz_price
    else:
        return zz_price

# 计算剩余年限
def getSYNX(dqr):
    ymd = dqr #到期日
    y = ymd.split('-')
    d1 = datetime(int(y[0]), int(y[1]), int(y[2]), 0, 0)
    synx = round((d1 - datetime.now()).days / 365.00, 2)
    return synx

# 计算到期价值
def getDQJZ(synx, shj,  ll):
    y = synx #剩余年限
    j = float(shj) #赎回价
    mnlv = ll #每年的利率
    dqjz = 0.0

    inty = int(y)
    if y > inty: 
        y = inty + 1
    else:
        y = inty

    l = mnlv.split(',') #转成列表
    for i in range (len(l)-y, len(l)-1):
        dqjz = dqjz +round(float(l[i])*0.8, 2)

    dqjz = dqjz + j
    return dqjz

# 主程序
def getCX(alias):    
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select name, zzcode, zgcode, Prefix, pj, zgj, dqr, shj, ll, hs, yjd, aqd from cb where Alias = '%s'" %alias
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()
        #print tmp
         
        name = tmp[0][0] #名称
        zzcode = tmp[0][1] #转债代码
        zgcode = tmp[0][2] #正股代码
        prefix = tmp[0][3] #前缀
        zz_code = prefix+zzcode #前缀+转债代码
        zz = float(getZZ(zz_code)) #查询转债价格
        zg_code = prefix+zgcode #前缀+正股代码
        #zg_price = getZG(zg_code) #查询正股价格
        pj = tmp[0][4] #评价
        zgj = float(tmp[0][5]) #转股价
        #zgjz = round((100/zgj)*zg_price, 2) #计算转股价值
        #yjl = round((zz-zgjz)/zgjz*100, 2) #计算溢价率
        dqr = tmp[0][6] #到期日
        synx = getSYNX(dqr) #计算剩余年限
        shj = tmp[0][7] #赎回价
        ll = tmp[0][8] #每年的利率
        hstk = tmp[0][9] #回售条款
        dqjz = getDQJZ(synx, shj, ll) #计算到期价值
        dqsyl = round((dqjz/zz - 1) * 100, 2) #计算到期收益率
        dqnh = round(dqsyl/synx, 2) #计算到期年化收益率

        yjd = tmp[0][10] #研究度
        aqd = tmp[0][11] #安全度

        print u"转债名称：" + name
        print u"转债评级：" + pj
        print u"研 究 度：" + yjd
        print u"安 全 度：" + aqd

        print u"\n最新价格：" + str(zz) + u"元"
        print u"到期价值：" + str(dqjz) + u"元"
        print u"剩余年限：" + str(synx) + u"年"
        print u"到期收益率：" + str(dqsyl) + u"％"
        print u"到期年化收益率：" + str(dqnh) + u"％"
        print
        print u"利率：" + ll
        #print hstk
        print

        for i in range(1,7): #由到期收益率计算转债的价格
            syl = 1 + (i * synx)/100
            dhj = round((dqjz/syl), 3)
            print u"到期年化收益率为" + str(i) +u"%时,转债价格：" + str(dhj) + u"元"
        print

    except Exception, e :
        print u'主程序报错：'+str(e)

if __name__ == '__main__':
    alias = raw_input('输入可转债的简称缩写：')
    print
    dqjz = getCX(alias)