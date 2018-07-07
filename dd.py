#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于记录可转债每日的开盘价，收盘价，溢价率，年化收益率等数据

__author__ = 'winsert@163.com'

import sqlite3, urllib2
from datetime import datetime
from cx_ex import getEX

# 生成日期
def getDATE():
    now_time = datetime.now()
    year = str(now_time.year)
    month = now_time.month
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)

    day = now_time.day
    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)

    today = year+month+day
    #print today
    return today

# 用于解析URL页面
def bsObjForm(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read().decode('gbk','ignore')
    return html

# 用于查询正股的数据
def getZG(zgCode):
    key = zgCode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp_list = resp.split(',')
        zg_s = tmp_list[1] #获取开盘价
        zg_e = tmp_list[3] #获取收盘价
        zg_h = tmp_list[4] #获取最高价
        zg_l = tmp_list[5] #获取最低价
        return zg_s, zg_e, zg_h, zg_l
    except:
        zg_s, zg_e, zg_h, zg_l = '0.000'
        return zg_s, zg_e, zg_h, zg_l

# 用于查询转债的数据
def getZZ(zzCode):
    key = zzCode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp_list = resp.split(',')
        zz_s = tmp_list[1] #获取开盘价
        zz_e = tmp_list[3] #获取收盘价
        zz_h = tmp_list[4] #获取最高价
        zz_l = tmp_list[5] #获取最低价
        zz_z = tmp_list[8] #获取成交张数
        zz_j = tmp_list[9] #获取成交金额
        return zz_s, zz_e, zz_h, zz_l, zz_z, zz_j
    except:
        zz_s, zz_e, zz_h, zz_l, zz_z, zz_j = '0.000'
        return zz_s, zz_e, zz_h, zz_l, zz_z, zz_j

# 计算剩余年限
def getSYNX(dqr):
    ymd = dqr #到期日
    y = ymd.split('-')
    d1 = datetime(int(y[0]), int(y[1]), int(y[2]), 0, 0)
    synx = round((d1 - datetime.now()).days / 365.00, 3)
    return synx

# 计算到期价值
def getDQJZ(synx, shj,  ll):
    synx = synx #剩余年限
    shj = float(shj) #赎回价
    mnlv = ll #每年的利率
    dqjz = 0.0

    int_synx = int(synx)
    if synx > int_synx: 
        synx = int_synx + 1
    else:
        synx = int_synx
    #print synx

    l = mnlv.split(',') #转成列表
    
    for i in range (len(l)-synx, len(l)-1):
        dqjz = dqjz +round(float(l[i])*0.8, 2)

    dqjz = dqjz + shj
    return dqjz

#将查询结果写入数据库dd.db
def getRECORD(today, code, zg_s, zg_e, zg_h, zg_l, zz_s, zz_e, zz_h, zz_l, zz_z, zz_j, yjl, dqnh):
    today = today #日期
    code = 'c'+code #转债代码
    zg_s = zg_s #正股开盘价
    zg_e = zg_e #正股收盘价
    zg_h = zg_h #正股最高价
    zg_l = zg_l #正股最低价
    zz_s = zz_s #转债开盘价
    zz_e = zz_e #转债收盘价
    zz_h = zz_h #转债最高价
    zz_l = zz_l #转债zuid价
    zz_z = zz_z #转债成交张数
    zz_j = zz_j #转债成交金额
    yjl = yjl   #溢价率
    dqnh = dqnh #年化收益率

    conn = sqlite3.connect('dd.db')
    create_tb_cmd = "CREATE TABLE IF NOT EXISTS %s (today text, zg_s text, zg_e text, zg_h text, zg_l text, zz_s text, zz_e text, zz_h text, zz_l text, zz_z text, zz_j text, yjl text, dqnh text);" %code
    conn.execute(create_tb_cmd)
    insert_dt_cmd = "INSERT INTO %s (today, zg_s, zg_e, zg_h, zg_l, zz_s, zz_e, zz_h, zz_l, zz_z, zz_j, yjl, dqnh) VAlUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" %code
    conn.execute(insert_dt_cmd, (today, zg_s, zg_e, zg_h, zg_l, zz_s, zz_e, zz_h, zz_l, zz_z, zz_j, yjl, dqnh))
    conn.commit()
    conn.close()

# 主程序
def getCX(today):
    today = today
    
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select name, Code, zgcode, Prefix, zgj, dqr, shj, ll, ce from cb"
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

        for cb in tmp:
            name = cb[0] #转债名称
            code = cb[1] #转债代码
            zgcode = cb[2] #正股代码
            prefix = cb[3] #前缀
            zgj = float(cb[4]) #转股价
            dqr = cb[5] #到期日
            shj = cb[6] #赎回价
            ll = cb[7] #每年的利率
            ce = cb[8] #区别转债和交换债

            #if prefix != 'QS' and ce != 'e':
            if cb[1] == '123005':

                zgcode = cb[3]+cb[2] #正股代码
                zg_s, zg_e, zg_h, zg_l = getZG(zgcode) #查询正股开盘，收盘，最高，最低价数据
                #print name, zg_s, zg_e, zg_h, zg_l

                if zg_h != '0.000' and zg_l != '0.000': #判断正股是否停牌

                    zzcode = cb[3]+cb[1] #转债代码
                    zz_s, zz_e, zz_h, zz_l, zz_z, zz_j = getZZ(zzcode) #查询转债开盘，收盘，最高,最低价，成交张数，成交金额等数据
                    #print name, zz_s, zz_e, zz_h, zz_l, zz_z, zz_j
                    
                    zgjz = (100/float(zgj))*float(zg_e) #计算转股价值
                    yjl = str(round((float(zz_e) - zgjz)/zgjz*100, 2)) #计算溢价率
                    #print name, zgjz, yjl

                    synx = getSYNX(dqr) #计算剩余年限
                    dqjz = getDQJZ(synx, shj, ll) #计算到期价值
                    #print name, dqjz

                    dqsyl = round((dqjz/float(zz_e) - 1) * 100, 3) #计算到期收益率
                    dqnh = str(round(dqsyl/synx, 2)) #计算到期年化收益率
                    print today, name, zz_s, zz_e, zz_h, zz_l, zz_z, zz_j, yjl, dqnh

                    getRECORD(today, code, zg_s, zg_e, zg_h, zg_l, zz_s, zz_e, zz_h, zz_l, zz_z, zz_j, yjl, dqnh)
        
    except Exception, e:
        print e
        
if __name__ == '__main__':
    today = getDATE() #生成日期
    getCX(today)