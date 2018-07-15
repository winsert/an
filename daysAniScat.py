#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用可转债每日的溢价率，年化收益率画动态散点图

__author__ = 'winsert@163.com'

import sqlite3, random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
        code_list.remove('113008')
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
            else:
                print str(date) + u" 没有数据！"
        
        #print date_list
        return date_list
         
    except Exception, e:
        print e
    
# 查询转债的数据
def getCbData(dates, codes):
    
    cb_lists = []
    try:
        for date in dates:
            cb_list = []
            for code in codes:
                code_tab ='c' + code
                conn = sqlite3.connect('dd.db')
                curs = conn.cursor()
                sql = "select yjl, dqnh from %s where today = %s" % (code_tab, date)
                curs.execute(sql)
                tmp = curs.fetchall()
                curs.close()
                conn.close()
                #print tmp
            
                for cb in tmp:
                    #print cb
                    c = []
                    c0 = float(cb[0])
                    c.append(c0)
                    c1 = float(cb[1])
                    c.append(c1)
                    
                    cb_list.append(c)
                #print cb_list
                #raw_input()
                
            cb_lists.append(cb_list)
            #print cb_lists
            #raw_input()
            
        #print cb_lists
        return cb_lists
            
    except Exception, e:
        print e

#生成x, y数列
def getXYList(xy_list):
    x_lists = []
    y_lists = []
    for i in xy_list: #取出某日的数列
        #print i
        #raw_input()
        x_list = []
        y_list = []
        for j in i: #取出某日某转债的数列
            x_list.append(j[0])
            y_list.append(j[1])

        x_lists.append(x_list)
        y_lists.append(y_list)
        #print type(x_lists)
        #print y_lists
        #print
        #raw_input()
    
    return x_lists, y_lists


#画散点图
def getScat(x_lists, y_lists, date_list):
        
    X = np.array(x_lists)
    Y = np.array(y_lists)
    #print type(X); raw_input()
        
    fig = plt.figure()
    plt.scatter(X, Y, s=3, c='b', alpha=1)

    #plt.title(date)
    plt.xlim(-20, 175)
    plt.xlabel('premium rate')
    #plt.xticks(())  # ignore xticks
    plt.ylim(-10, 10)
    plt.ylabel('annualized rate of return')
    #plt.yticks(())  # ignore yticks

    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))

    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))

    plt.show()
    

if __name__ == '__main__':
    '''
    today = getDATE() #生成日期
    print u"\n今天是：" + today + "\n"

    start_date = int(raw_input("请输入开始日期，例：20180707 > "))
    while start_date < 20180707:
        start_date = int(raw_input("请输入开始日期，例：20180709 > "))

    end_date = int(raw_input("请输入结束日期，例：20180809 > "))
    while end_date > int(today) or end_date < start_date:
        end_date = int(raw_input("请输入结束日期，例：20180809 > "))
    
    print u"\n即将开始查询自 " + str(start_date) + u" 至 " + str(end_date) + u" 期间的数据...\n"
    '''
    codes = getCode() #查询转债的代码
    
    #date_list = getDate(start_date, end_date, codes) #判断查询日期是否存在数据
    date_list = getDate(20180707, 20180709, codes) #判断查询日期是否存在数据

    xy_list = getCbData(date_list, codes) #查询转债的数据
    x_lists, y_lists = getXYList(xy_list) #生成x, y数列

    getScat(x_lists, y_lists, date_list) #画散点图
    
    print u"结束查询！"