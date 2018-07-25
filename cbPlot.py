#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于画出指定转债成交金额的折线图

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
        sql = "select Code, name from cb where alias = %r;" %alias 
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()
        code = tmp[0][0]
        name = tmp[0][1]
        
        #print u"开始查询 " + name + u"转债 的数据......\n"
        return code, name
        
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
    
# 查询转债的数据
def getCbData(date, ccode):
    cjje = 0

    try:
        conn = sqlite3.connect('dd.db')
        curs = conn.cursor()
        sql = "select zz_j from %s where today = %s" % (ccode, date) #按日期查询成交金额
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()
        #print tmp
                
        for cb in tmp:
            #print round(float(cb[0]), 3)
            cjje = cjje + (round((float(cb[0])/10000))) #成交金额多少万元
            #print cjje
            
        #print round(cjje / 10000, 3) #成交金额多少千万元
        return round(cjje / 10000, 3)
        
    except Exception, e:
        print e

#画折线图
def getPlot(cjje_lists, date_txt, je):
    n = len(cjje_lists) #用于设定X轴
    print u"\n将显示 " + str(n) + u" 天的查询结果......"
    x = [] #日期
    y = [] #成交金额
    for i in cjje_lists:
        #x.append(round((float(i[0]) / 10), 2))
        x.append(float(i[0]))
        y.append(float(i[1]))
    
    plt.figure(figsize=(16, 8))
    plt.title(date_txt)
    plt.plot(x, y, label='AMO changes', linewidth=2, color='r', marker='o', markerfacecolor='blue', markersize=5)
    plt.xlabel('DATE')
    plt.ylabel('AMO')
    plt.ylim(0, je * 4) #根据成交金额的平均值设定Y轴

    # 设置数字标签
    for a, b in zip(x, y):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=20)

    plt.show()


if __name__ == '__main__':
    
    today = getDATE() #生成日期
    print u"\n今天是：" + today + "\n"

    cb = raw_input('请输入可转债"名称缩写"或"代码" > ')

    while cb == '' or len(cb) > 6:
        cb = raw_input('请输入可转债"名称缩写"或"代码" > ')
    
    if cb.isdigit():
        while len(cb) < 6:
            cb = raw_input('请输入可转债"名称缩写"或"代码" > ')
        ccode = 'c' + cb
    else:
        code, cb = getCode(cb)
        ccode = 'c' + code
    #print code

    start_date = raw_input("请输入开始日期，例：20180707 > ")
    if start_date == '':
        start_date = '20180707'
        print u"查询开始日期：" + start_date + '\n'
    else:
        while int(start_date) < 20180707 or int(start_date) > (int(today) - 1) :
            start_date = raw_input("请输入开始日期，例：20180707 > ")
            
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
    
    cjje_lists = [] #记录查询日期的成交金额
    
    for date in date_list:
        cjje_list = [] #记录每日的成交金额
        #print u"\n即将开始查询 " + date + u" 的数据...\n"
        cjje = getCbData(date, ccode) #查询转债每日的成交金额的数据
        cjje_list.append(Cdate(date)) #改变日期格式
        cjje_list.append(cjje)
        cjje_lists.append(cjje_list)
    
    # 计算每日成交金额的平均值
    cjje = 0
    n = len(cjje_lists)
    for cj in cjje_lists:
        print cj
        cjje = cjje + cj[1]
    je = round(cjje / n, 2) #计算平均值，用于设定坐标轴的y值
    
    print u'\n将显示以下数据：'
    print cjje_lists
    date_txt = str(start_date) + " --- " + str(end_date)
    #date_txt = "20180707  ---  20180719"
    getPlot(cjje_lists, date_txt, je) #画折线图，X轴日期，Y轴成交金额
    
    print u"结束查询！"