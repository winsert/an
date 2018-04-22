#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于记录转债的每笔成交记录

__author__ = 'winsert@163.com'

import sqlite3
from datetime import datetime

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# 查询指定转债的数据
def CX(code):
    cx = code
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select name, code, position, avg from cb where Code = '%s'" %cx
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

        name = tmp[0][0] #转债名称
        code = tmp[0][1] #代码
        position = tmp[0][2] #持仓
        avg = tmp[0][3] #平均成本

        print
        print u'    名  称：', name
        print u'    代  码：', code
        print u'    持  仓： ' + str(position) + u'张'
        print u'    平均价： ' + str(avg) + u'元'
        print

        return name, position

    except Exception, e :
        print 'CX() Error:', e
        sys.exit()

# 生成日期
def TD():
    now_time = str(datetime.now())
    date = now_time[0:10]
    return date

# 增加新交易记录
def EX(code, date, price, amount):
    code = code
    date = date
    price = float(price)
    amount = int(amount)

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "INSERT INTO exchange (code, date, price, amount) VALUES (?, ?, ?, ?)"
        curs.execute(sql, ( code, date, price, amount ))
        conn.commit()
        curs.close()
        conn.close()

        print
        print u'已增加新交易记录：'

    except Exception, e:
        print 'EX() ERROR :', e
        sys.exit()

# 修改cb表格中的position, avg数据
def Position(code, position, avg):
    code = code
    position = position
    avg = avg

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "UPDATE cb SET Position = %d, AVG = %r WHERE Code = %s" % (position, avg, code) 
        curs.execute(sql)
        conn.commit()
        curs.close()
        conn.close()

    except Exception, e:
        print 'Position() ERROR :', e
        sys.exit()

# 求持仓平均成本价
def AVG(code):
    code = code
    tmp = []

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "SELECT sum(price*amount)/sum(amount) from exchange WHERE Code = %s" % code
        curs.execute(sql)
        tmp = curs.fetchall()
        avg = tmp[0][0]
        conn.commit()
        curs.close()
        conn.close()

        return avg

    except Exception, e:
        print 'AVG() ERROR :', e
        sys.exit()

if  __name__ == '__main__': 
    
    msg = u"""
    本程序用于记录每笔交易数据：
    - 日  期 date
    - 成交价 price
    - 成交量 amount
    - 持  仓 position
    - 平均价 avg
    """
    print
    print msg
    code = raw_input(u'输入可转债的代码：')
    cx_name, cx_position = CX(code) #返回指定转债name, position

    yn1 = raw_input(u'是否要修改(y/n)？')
    if yn1 == 'n':
        sys.exit()

    print
    price = raw_input(u"请输入 成交价 ：")
    amount = raw_input(u"请输入 成交量 ：")

    print
    print u'将修改以下转债数据：'
    print
    print u'    名  称 ：' + cx_name
    print u'    代  码 ：' + code
    print u'    成交价 ：' + price
    print u'    成交量 ：' + amount
    print

    yn2 = raw_input(u'是否要修改(y/n)？')
    if yn2 == 'y':
        date = TD() #生成日期
        EX(code, date, price, amount) #生成新交易记录
        position = int(cx_position) + int(amount) #更新持仓数据
        avg = round(AVG(code),2) #计算平均持仓成本
        print u'    名  称 ：' + cx_name
        print u'    代  码 ：' + code
        print u'    日  期 ：' + date
        print u'    成交价 ：' + price
        print u'    成交量 ：' + amount
        print u'    持仓量 ：' + str(position)
        print u'    平均价 ：' + str(avg)
        print
        Position(code, position, avg) #更新cb表中的position和avg数据
    else:
        sys.exit()
