#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于画出指定转债溢价率、年化收益率的折线图

__author__ = 'winsert@163.com'

import sqlite3, random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

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

# 改变日期格式
def Cdate(date):
    dd = list(date)
    
    if dd [4] == '0':
        ddd = dd[5] + dd[6] + dd[7]
    else:
        ddd = dd[4] + dd[5] + dd[6] + dd[7]
    #print ddd
    return ddd

# 查询转债的代码
def getCode(alias):
    
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select Code from cb where alias = %r;" %alias 
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()
        code = str(tmp[0][0])
        
        return code
        
    except Exception, e:
        print e

# 查询转债的代码
def getCBInfo(code):
    
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select name, zgj, dqr, shj, ll from cb where Code = %r;" %code 
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()
        name = tmp[0][0]
        zgj = tmp[0][1]
        dqr = tmp[0][2]
        shj = tmp[0][3]
        ll = tmp[0][4]
        
        print u"\n名  称：" + name + u"\n转股价：" + str(zgj) + u"\n到期日：" +  dqr + u"\n赎回价：" +  str(shj) + u"\n年利率：" + ll
        return name, zgj, dqr, shj, ll
        
    except Exception, e:
        print e


# 判断查询日期是否存在数据
def getDate(sdate, edate, ccode):
    
    tmp_list = []
    date_list = []
    
    try:
        conn = sqlite3.connect('dd.db')
        curs = conn.cursor()
        sql = "select today from %s" % (ccode)
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()
        #print tmp

        for day in tmp:
            tmp_list.append(day[0])
        #print tmp_list 

        for date in range(sdate, edate+1):
            if str(date) in tmp_list:
                date_list.append(str(date))
            else:
                print str(date) + u" 没有数据！"
        
        #print date_list
        return date_list
         
    except Exception, e:
        print e
    
# 查询转债的收盘价
def getSPJ(date, ccode):

    try:
        conn = sqlite3.connect('dd.db')
        curs = conn.cursor()
        sql = "select zg_e, zz_e from %s where today = %s" % (ccode, date) #按日期查询收盘价
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()
        zg_spj = float(tmp[0][0]) #正股收盘价
        zz_spj = float(tmp[0][1]) #转债收盘价
        #print zg_spj, zz_spj
        return zg_spj,  zz_spj
        
    except Exception, e:
        print e

def getYJL(zg_spj, zz_spj, zgj):
    '''计算溢价率'''
    zgjz = (100/zgj)*zg_spj #计算转股价值
    yjl = round((zz_spj-zgjz)/zgjz*100, 2) #计算溢价率
    #print yjl
    return yjl

def getSYNX(dqr):
    '''计算剩余年期'''
    y = dqr.split('-')
    d1 = datetime(int(y[0]), int(y[1]), int(y[2]), 0, 0)
    synx = round((d1 - datetime.now()).days / 365.00, 3)
    #print synx
    return synx

def getDQJZ(synx, shj, ll):
    '''计算到期价值'''
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

def getDQNH(dqr, shj, ll, zz_spj):
    '''计算到期年化收益率'''
    synx = getSYNX(dqr) #计算剩余年限
    dqjz = getDQJZ(synx, shj, ll) #计算到期价值
    dqsyl = round((dqjz/zz_spj - 1) * 100, 3)
    dqnh = round(dqsyl/synx, 2)
    #print dqnh
    return dqnh


#画折线图
def getPlot(days_list, date_txt, ax, ay):
    n = len(days_list) #用于设定X轴
    print u"\n将显示 " + str(n) + u" 天的查询结果......"
    x = [] #日期
    y = [] #成交金额
    for i in days_list:
        #x.append(round((float(i[0]) / 10), 2))
        x.append(float(i[0]))
        y.append(float(i[1]))
    
    plt.figure(figsize=(16, 8))
    plt.title(date_txt)
    plt.plot(x, y, label='AMO changes', linewidth=2, color='r', marker='o', markerfacecolor='blue', markersize=5)
    #plt.plot(x, y)
    plt.xlim(ax-15, ax+15) #溢价率
    #plt.xlabel('premium rate')
    plt.ylim(ay-1.5, ay+1.5) #到期年化收益率
    #plt.ylabel('annualized rate of return')

    plt.show()


if __name__ == '__main__':
    
    today = getDATE() #生成日期
    print u"\n今天是：" + today + "\n"

    cb = raw_input('请输入可转债"名称缩写"或"代码" > ')

    while cb == '' or len(cb) > 6:
        cb = raw_input('请输入可转债"名称缩写"或"代码" > ')
    
    if cb.isdigit(): #cb是转债代码
        while len(cb) < 6:
            cb = raw_input('请输入可转债"名称缩写"或"代码" > ')
        code = cb
        name, zgj, dqr, shj, ll = getCBInfo(code) #得到名称、转股价，到期日，赎回价，利率
    else: #cb是转债别名
        code = getCode(cb) #别名转为代码
        name, zgj, dqr, shj, ll = getCBInfo(code) #得到名称、转股价，到期日，赎回价，利率
    
    ccode = 'c' + code #用于在dd.db中查询表格

    # 开始查询日期
    start_date = raw_input("请输入开始日期，例：20180707 > ")
    if start_date == '':
        start_date = '20180707'
        print u"查询开始日期：" + start_date + '\n'
    else:
        while int(start_date) < 20180707 or int(start_date) > (int(today) - 1) :
            start_date = raw_input("请输入开始日期，例：20180707 > ")
    
    #结束查询日期
    end_date = raw_input("请输入结束日期，例：20180809 > ")
    if end_date == '':
        end_date = today
        print u"查询结束日期：" + today
    else:
        while int(end_date) > int(today) or int(end_date) < int(start_date):
            end_date = raw_input("请输入结束日期，例：20180809 > ")
    
    print u"\n即将开始查询 " + cb + u" 自 " + start_date + u" 至 " + end_date + u" 期间的数据......\n"
    
    start_date = int(start_date)
    end_date = int(end_date)
    date_list = getDate(start_date, end_date, ccode) #判断查询日期是否存在数据
    #date_list = getDate(20180707, 20180719, ccode) #判断查询日期是否存在数据
    
    days_list = [] #记录查询日期的成交金额

    for date in date_list:
        day_list = [] #记录每日的成交金额
        #print u"\n即将开始查询 " + date + u" 的数据...\n"
        zg_spj, zz_spj = getSPJ(date, ccode) #查询转债收盘价
        yjl = getYJL(zg_spj, zz_spj, zgj) #查询转债溢价率
        day_list.append(yjl) 
        dqnh = getDQNH(dqr, shj, ll, zz_spj) #查询转债到期年化收益率
        day_list.append(dqnh) 
        days_list.append(day_list)
    
    print u'\n将显示以下数据：'
    print days_list

    # 计算溢价率的平均值
    a = 0
    n = len(days_list)
    for h in days_list:
        a = a + h[0]
    ax = round(a / n, 2) #计算平均值，用于设定坐标轴的x值

    # 计算到期年化收益率的平均值
    b = 0
    n = len(days_list)
    for h in days_list:
        b = b + h[1]
    ay = round(b / n, 2) #计算平均值，用于设定坐标轴的y值

    date_txt = str(start_date) + " --- " + str(end_date)
    #date_txt = "20180707  ---  20180719"
    getPlot(days_list, date_txt, ax, ay) #画折线图，X轴日期，Y轴成交金额
    
    print u"结束查询！"