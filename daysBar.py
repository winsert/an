#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于画出每日可交易转债成交金额的折线图

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

# 判断查询日期是否存在数据
def getDate(sdate, edate, codes):
    code = 'c' + random.choice(codes)
    tmp_list = []
    date_list = []
    
    try:
        conn = sqlite3.connect('dd.db')
        curs = conn.cursor()
        sql = "select today from %s" % (code)
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
            #else:
                #print str(date) + u" 没有数据！"
        
        #print date_list
        return date_list
         
    except Exception, e:
        print e
    
# 查询转债的数据
def getCbData(date, codes):
    cjje = 0

    try:
        for code in codes:
            code_tab ='c' + code
            conn = sqlite3.connect('dd.db')
            curs = conn.cursor()
            sql = "select zz_j from %s where today = %s" % (code_tab, date) #按日期查询成交金额
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

#画折线图
def getBar(cjje_lists, date_txt):
    n = len(cjje_lists) #用于设定X轴
    print u"\n将显示 " + str(n) + u" 天的查询结果......"
    x = [] #日期
    y = [] #成交金额
    for i in range(n):
        #x.append(round((float(i[0]) / 10), 2))
        x.append(i+1)
        y.append(float(cjje_lists[i][1]))
        #y.append(float(i[1]))
    
    plt.figure(figsize=(20, 8))
    plt.bar(x, y)

    plt.xlim(0, 32)
    plt.title(date_txt)
    plt.xlabel('DATE')
    plt.xticks(())  # ignore xticks
    plt.ylabel('AMO')
    plt.ylim(0, 35)
    #plt.yticks(())  # ignore yticks

    # 设置数字标签
    for a, b in zip(x, y):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=20)

    plt.show()


if __name__ == '__main__':
    
    today = getDATE() #生成日期
    print u"\n今天是：" + today + "\n"

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
    
    print u"\n即将开始查询自 " + start_date + u" 至 " + end_date + u" 期间的数据......\n"
    
    codes = getCode() #查询转债的代码
    
    start_date = int(start_date)
    end_date = int(end_date)
    date_list = getDate(start_date, end_date, codes) #判断查询日期是否存在数据
    #date_list = getDate(20180707, 20180719, codes) #判断查询日期是否存在数据
    
    cjje_lists = [] #记录查询日期的成交金额
    
    for date in date_list:
        cjje_list = [] #记录每日的成交金额
        #print u"\n即将开始查询 " + date + u" 的数据...\n"
        cjje = getCbData(date, codes) #查询转债的数据
        cjje_list.append(Cdate(date))
        cjje_list.append(cjje)
        cjje_lists.append(cjje_list)
        
    print u'\n将显示以下 ' + str(len(cjje_lists))+ u' 天数据：'
    print cjje_lists
    date_txt = str(start_date) + " --- " + str(end_date)
    #date_txt = "20180707  ---  20180719"
    getBar(cjje_lists, date_txt) #画折线图，X轴日期，Y轴成交金额
    
    print u"结束查询！"