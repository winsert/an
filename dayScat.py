#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用可转债每日的溢价率，年化收益率画散点图

__author__ = 'winsert@163.com'

import sqlite3, random
import numpy as np
import matplotlib.pyplot as plt

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
def getDate(date, codes):
    code = 'c' + random.choice(codes)
    
    try:
        conn = sqlite3.connect('dd.db')
        curs = conn.cursor()
        sql = "select yjl from %s where today = %s" % (code, date)
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()
        #print tmp
        #print len(tmp)
        
        return len(tmp)
         
    except Exception, e:
        print e
    
# 查询转债的数据
def getCbData(date, codes):
    cb_list = []
    try:
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
                cb_list.append(cb)
            
        #print cb_list
        return cb_list
            
    except Exception, e:
        print e

#画散点图
def getScat(xy, date):
    x = [] #溢价率
    y = [] #到期年化收益率
    for i in xy:
        #x.append(round((float(i[0]) / 10), 2))
        x.append(float(i[0]))
        y.append(float(i[1]))
    
    X = np.array(x)
    Y = np.array(y)
    
    plt.scatter(X, Y, s=10, c='blue', alpha=1)

    plt.title(date)
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
    
    date = int(raw_input("请输入查询日期，例：20180707 > "))
    while date < 20180707:
        date = int(raw_input("请输入开始日期，例：20180709 > "))
    
    codes = getCode() #查询转债的代码
    d = getDate(date, codes) #判断查询日期是否存在数据
    if d != 0:
        print u"\n即将开始查询 " + str(date) + u" 的数据...\n"
        xy_list = getCbData(date, codes) #查询转债的数据
        getScat(xy_list, date) #画散点图
    else:
        print u'\n' + str(date) + u" 的数据不存在！\n"