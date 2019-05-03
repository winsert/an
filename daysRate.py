#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于查询每日收盘价超过到期价值的转债占比,并画出折线图

__author__ = 'winsert@163.com'

import sqlite3, urllib2, datetime
import matplotlib.pyplot as plt

# 生成今天日期
def getToday():
    now_time = datetime.datetime.now()
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

# 生成查询日期
def getDate(ndays):
    tmp_list = []

    for d in range(-1*ndays, 1):
        #print d
        now_time = datetime.datetime.now()
        cx_time = now_time + datetime.timedelta(days=d)
        year = str(cx_time.year)
        month = cx_time.month
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)

        day = cx_time.day
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)

        cx_date = year+month+day
        #print cx_date
        tmp_list.append(cx_date)
    #print tmp_list
    return tmp_list

# 计算剩余年限
def getSYNX(dqr):
    ymd = dqr #到期日
    y = ymd.split('-')
    d1 = datetime.datetime(int(y[0]), int(y[1]), int(y[2]), 0, 0)
    synx = round((d1 - datetime.datetime.now()).days / 365.00, 3)
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
        #dqjz = dqjz +round(float(l[i])*0.8, 2)
        dqjz = dqjz + float(l[i])

    dqjz = dqjz + shj
    return dqjz

#查询转债的代码和到期价值
def getCB():
    tmp_lists = []

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select name, Code, zgcode, Prefix, zgj, dqr, shj, ll, ce, zgqsr from cb"
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

        for cb in tmp:
            #name = cb[0] #转债名称
            code = cb[1] #转债代码
            prefix = cb[3]
            dqr = cb[5] #到期日
            shj = cb[6] #赎回价
            ll = cb[7] #每年的利率
            ce = cb[8] #区别转债和交换债

            if prefix != 'QS' and ce != 'e':
            #if cb[1] == '123015':
                #print name
                synx = getSYNX(dqr) #计算剩余年限
                dqjz = getDQJZ(synx, shj, ll) #计算到期价值
                #print dqjz
                tmp_list = []
                tmp_list.append(code)
                tmp_list.append(dqjz)
                tmp_lists.append(tmp_list)
        return tmp_lists

    except Exception, e:
        print 'getCB(): ', e

def getRate(date_list, cb_lists):
    zb = 0.0 #收盘价>到期价值的转债占所有转债的比例
    zb_lists = []
    try:
        for dl in date_list:
            #print dl
            zb_list = []
            cSum = 0 #记录转债的总数
            vSum = 0 #记录收盘价>到期价值的转债数量
            for cb in cb_lists:
                cl = 'c' + cb[0] #生成表名
                dqjz = float(cb[1]) #到期价值

                conn = sqlite3.connect('dd.db')
                curs = conn.cursor()
                sql = "select today, zz_e from %s" %cl #取日期、转债当日收盘价
                curs.execute(sql)
                dd_tmp = curs.fetchall()
                curs.close()
                conn.close()

                for zz in dd_tmp:
                    zz_date = zz[0] #日期
                    zz_e = float(zz[1]) #转债收盘价
                    if zz_date == dl:
                        #print cb[0], cb[1], zz_e
                        cSum = cSum + 1
                        if zz_e > dqjz:
                            #print cb[0], zz_e, dqjz
                            vSum = vSum + 1
            if cSum > 0:
                zb = round(float(vSum)/float(cSum)*100, 2)
                #print dl, cSum, vSum, zb
                zb_list.append(dl)
                zb_list.append(zb)
                zb_lists.append(zb_list)
                print dl+u'：共有 '+str(cSum)+u' 只转债，其中 '+str(vSum)+u' 只转债的收盘价 > 到期价值，占比：'+str(zb)+'%'

        #print zb_lists
        return zb_lists

    except Exception, e:
        print 'getRate()', e

#画折线图
def getLine(zb_lists):
    n = len(zb_lists) #用于设定X,Y轴
    x = [] #日期
    y = [] #占比
    
    for i in range(n):
        x.append(i+1)

    for i in range(n):
        y.append(float(zb_lists[i][1]))
    
    #plt.figure(figsize=(0, 2))
    plt.title(u"牛熊转换指标")
    plt.plot(x, y, linewidth=3, color='b')
    #plt.plot(x, y2, linewidth=5, color='r', marker='o', markerfacecolor='blue', markersize=5)
    
    plt.xlim(0, 120)
    plt.xlabel('DATE')
    plt.xticks(())  # ignore xticks
    plt.ylabel('RATE')
    plt.ylim(0, 90)
    #plt.yticks(())  # ignore yticks

    plt.show()


if __name__ == '__main__':
    
    ndays = 180 #查询Ｎ天前的数据

    today = getToday() #生成今天日期
    print u"\n今天是：" + today + "\n"
    print u"即将开始查询自 " + today + u" 起倒数 " + str(ndays) + u" 天的数据......\n"
    
    date_list = getDate(ndays) #生成开始日期
    #print date_list

    cb_lists = getCB() #查询转债的代码和到期价值
    #cb_list = [['127009', 115.3], [u'113527', 120.7]]
    #print cb_lists

    zb_lists = getRate(date_list, cb_lists) #计算收盘价>到期价值的转债占所有转债的比例
    #print zb_lists

    getLine(zb_lists) #画折线图
