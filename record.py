#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于查询转债的每笔成交记录

__author__ = 'winsert@163.com'

import sqlite3

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# 查询指定转债的数据
def CX(code):
    code = code
    tmp = []
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select name, position, avg from cb where Code = '%s'" %code
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

        name = tmp[0][0] #转债名称
        position = tmp[0][1] #持仓
        avg = tmp[0][2] #平均成本

        print
        print '\t', u'查询结果：'
        print '\t', u'名  称：', name
        print '\t', u'代  码：', code
        print '\t', u'持  仓： ' + str(position) + u'张'
        print '\t', u'平均价： ' + str(avg) + u'元'
        print

    except Exception, e :
        print 'CX() Error:', e
        sys.exit()

# 查询交易记录
def RC(code):
    code = code
    tmp = []

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select date, price, amount from exchange where Code = '%s' ORDER BY price" %code
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

        print '\t', u"日期", '\t', '\t',  u"成交价", '\t', u"成交量"
        for x in tmp:
            print '\t', x[0], '\t', x[1], '\t',  x[2]

        print
        print u'已完成交易记录查询。'

    except Exception, e:
        print 'RC() ERROR :', e
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
    本程序用于查询每笔交易数据：
    - 名  称 name
    - 代  码 code
    - 日  期 date
    - 成交价 price
    - 成交量 amount
    - 持  仓 position
    - 平均价 avg
    """
    print
    print msg
    code = raw_input(u'输入可转债的代码：')
    CX(code) #查询指定转债的name, position, avg
    RC(code) #返回指定转债的交易记录
