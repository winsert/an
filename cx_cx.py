#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于获取可转债、可交换债的最新价，三线价格，回售价等数据

__author__ = 'winsert@163.com'

import sqlite3, urllib2
from datetime import datetime
from cx_ex import getEX

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
        return zg_price, zg_zdf
    except:
        zg_price = 0.0
        zg_zdf = 0.0
        return zg_price, zg_zdf

# 用于查询转债的价格
def getZZ(zzCode):
    key = zzCode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    resp = bsObjForm(url)
    tmp_list = resp.split(',')
    zz_price = float(tmp_list[3]) #获取正股实时价格
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

    l = mnlv.split(',') #转成列表
    for i in range (len(l)-y, len(l)-1):
        dqjz = dqjz +round(float(l[i])*0.8, 2)

    dqjz = dqjz + j
    return dqjz


# 主程序
def getCX(alias):
    
    cx = alias
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select name, Code, zgcode, Prefix, jian, jia, zhong, Note, zgj, hsqsr, hsj, dqr, position, shj, ll, ce, qs, qss, zgqsr from cb where Alias = '%s'" %cx
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

        if tmp[0][3] == 'QS':
            msg = tmp[0][0]+u' :已强赎'
            return msg

        if tmp[0][15] == 'e':
            msg = getEX(cx)
            return msg

        zgcode = tmp[0][3]+tmp[0][2] #正股代码
        zg, zg_zdf = getZG(zgcode) #查询正股价格, 涨跌幅
        if zg == 0.0:
            msg = tmp[0][0]+u' : 停牌'
            return msg

        zzcode = tmp[0][3]+tmp[0][1] #转债代码
        zz = float(getZZ(zzcode)) #查询转债价格
        zgj = float(tmp[0][8]) #转股价
        zgjz = (100/zgj)*zg #计算转股价值
        yjl = round((zz-zgjz)/zgjz*100, 2) #计算溢价率
        qsj = round((zgj * 1.3), 2) #计算强赎价
        qsl = round((zg/zgj -1)*100, 2) #计算强赎率

        position = tmp[0][12] #已购买的张数

        dqr = tmp[0][11] #到期日
        synx = getSYNX(dqr) #计算剩余年限
        
        shj = tmp[0][13] #赎回价
        ll = tmp[0][14] #每年的利率
        dqjz = getDQJZ(synx, shj, ll) #计算到期价值
        dqsyl = round((dqjz/zz - 1) * 100, 2)
        dqnh = round(dqsyl/synx, 2)
        
        qs = tmp[0][16]
        qss = tmp[0][17]
        zgqsr = str(tmp[0][18])

        if float(tmp[0][10]) == 0.0:
            msg = tmp[0][0]+' '+tmp[0][2]+u'\n可转债 '+tmp[0][1]+' : '+str(position)+u'张\n'+u'最新价:'+str(zz)+u'  溢价率:'+str(yjl)+u'%'+u'\n建:'+str(tmp[0][4])+u'  加:'+str(tmp[0][5])+u'  重:'+str(tmp[0][6])+u'\n'+tmp[0][7]+'\n'+u'\n转股价:'+str(zgj)+u'\n转股起始日:'+zgqsr+u'\n正股价:'+str(zg)+u' 涨跌幅:'+str(zg_zdf)+'%'+u'\n强赎价:'+str(qsj)+u'\n已强赎:'+str(qs)+u'天'+u'  剩余:'+str(qss)+u'天'+u'\n到期价值:'+str(dqjz)+u'\n到期收益率:'+str(dqsyl)+'%'+u'\n到期年化收益率:'+str(dqnh)+'%'+u'\n回售起始日:无'+u'\n回售价:无'+u'\n到期日:'+str(dqr)+u'\n剩余年限:'+str(synx)
            #print msg
            return msg
        else:
            msg = tmp[0][0]+' '+tmp[0][2]+u'\n可转债 '+tmp[0][1]+' : '+str(position)+u'张\n'+u'最新价:'+str(zz)+u'  溢价率:'+str(yjl)+u'%'+u'\n建:'+str(tmp[0][4])+u'  加:'+str(tmp[0][5])+u'  重:'+str(tmp[0][6])+u'\n'+tmp[0][7]+'\n'+u'\n转股价:'+str(zgj)+u'\n转股起始日:'+zgqsr+u'\n正股价:'+str(zg)+u' 涨跌幅:'+str(zg_zdf)+'%'+u'\n强赎价:'+str(qsj)+u'\n已强赎:'+str(qs)+u'天'+u'  剩余:'+str(qss)+u'天'+u'\n到期价值:'+str(dqjz)+u'\n到期收益率:'+str(dqsyl)+'%'+u'\n到期年化收益率:'+str(dqnh)+'%'+u'\n回售起始日:'+str(tmp[0][9])+u'\n回售价:'+str(tmp[0][10])+u'\n到期日:'+str(dqr)+u'\n剩余年限:'+str(synx)
            #print msg
            return msg

    #except Exception, e:
        #print e

    except :
        msg = u'查询可转债:%s不存在！' %cx
        print msg
        return msg

if __name__ == '__main__':
    
    while 1:
        alias = raw_input('输入可转债名称的缩写：')
        print getCX(alias)
        print
