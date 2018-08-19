#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于画出每日可交易转债成交金额的折线图

__author__ = 'winsert@163.com'

import sqlite3, random, datetime
import numpy as np
import matplotlib.pyplot as plt
#from datetime import datetime

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

# 生成开始日期
def getDate(N):
    n = N * -1
    now_time = datetime.datetime.now()
    start_time = now_time + datetime.timedelta(days=n)
    year = str(start_time.year)
    month = start_time.month
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)

    day = start_time.day
    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)

    start_date = year+month+day
    #print start_date
    return start_date


# 查询转债的代码
def getCode():
    
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select Code, Prefix, ce from cb"
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

        code_list = []
        
        for code in tmp:
            if code[1] != 'QS' and code[2] != 'e': #过滤已强赎的转债和交换债
                code_list.append(code[0])
        
        #print code_list
        code_list.remove('123004')
        #print code_list
        return code_list
               
    except Exception, e:
        print e
    
# 查询转债的数据
def getCbData(n, codes):
    cjje = 0
    #print 'n = ', n

    try:
        for code in codes:
            code_tab ='c' + code
            conn = sqlite3.connect('dd.db')
            curs = conn.cursor()
            sql = "select zz_j from %s ORDER BY today desc limit %r, 1" % (code_tab, n) #按倒序查询成交金额
            curs.execute(sql)
            tmp = curs.fetchall()
            curs.close()
            conn.close()
            #print tmp
            
            
            for cb in tmp:
                #print round(float(cb[0]), 3)
                cjje = cjje + (round((float(cb[0])/10000))) #成交金额多少万元
                #print cjje
            
        #print round(cjje / 10000, 2) #成交金额多少亿元
        return round(cjje / 10000, 2)
        
    except Exception, e:
        print e

def getAVG(avg_days, cjje_lists):
    '''计算N天成交金额平均数'''
    a = 0
    avg_lists = []
    while (a + avg_days) <= len(cjje_lists):
        #print 'a = ', a
        cj = 0
        avg_list = []
        for i in range(a, a + avg_days):
            cj = cj + cjje_lists[i][1]
            b = cjje_lists[i][0]
            #print b
        avg = round((cj / avg_days), 2)
        avg_list.append(b)
        avg_list.append(avg)
        avg_lists.append(avg_list)
        a = a + 1

    print u'\n日成交金额的 ' + str(avg_days) + u' 日平均数：'
    print avg_lists
    return avg_lists

#画折线图
def getBP(cjje_lists, avg_lists, date_txt):
    n = len(cjje_lists) #用于设定X轴
    #print u"\n将显示 " + str(n) + u" 天的查询结果......"
    x = [] #日期
    y1 = [] #日成交金额
    y2 = [] #平均成交金额

    for i in range(n):
        #x.append(round((float(i[0]) / 10), 2))
        x.append(i+1)
        y1.append(float(cjje_lists[i][1]))
        #y.append(float(i[1]))
    
    for i in range(n):
        y2.append(float(avg_lists[i][1]))
    
    plt.figure(figsize=(16, 8))
    plt.title(date_txt)
    plt.bar(x, y1)
    plt.plot(x, y2, linewidth=3, color='r')
    #plt.plot(x, y2, linewidth=5, color='r', marker='o', markerfacecolor='blue', markersize=5)
    
    plt.xlim(0, 32)
    plt.xlabel('DATE')
    plt.xticks(())  # ignore xticks
    plt.ylabel('AMO')
    plt.ylim(0, 35)
    #plt.yticks(())  # ignore yticks

    # 设置数字标签
    for a, b in zip(x, y1):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=20)

    plt.show()
    

if __name__ == '__main__':
    
    avg_days = 5 #计算avg_days天的平均数据
    N = 25 #查询Ｎ天前的数据
    days = avg_days + N #查询倒数N+avg_days天的数据

    today = getToday() #生成今天日期
    print u"\n今天是：" + today + "\n"
    print u"即将开始查询自 " + today + u" 起倒数 " + str(days) + u" 天的数据......\n"
    
    start_date = getDate(N)

    codes = getCode() #查询转债的代码
    
    cjje_lists = [] #记录查询日期的成交金额
    
    for n in range((days - 1), -1, -1):
        cjje_list = [] #记录每日的成交金额
        cjje = getCbData(n, codes) #查询转债的数据
        cjje_list.append(n)
        cjje_list.append(cjje)
        cjje_lists.append(cjje_list)
    #print cjje_lists

    avg_lists = getAVG(avg_days, cjje_lists)
    
    cjje_lists = cjje_lists[(avg_days - 1):]
    print u'\n将显示以下 ' + str(len(cjje_lists))+ u' 天数据：'
    print cjje_lists
    
    date_txt = start_date + " --- " + today
    #print date_txt

    getBP(cjje_lists, avg_lists, date_txt) #画折线图，X轴日期，Y轴成交金额
 
    print u"\n结束查询！"