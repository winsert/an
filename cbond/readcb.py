#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 读出 code = ?的可转债、可交换债的所有信息
# 0:已强赎
# 1:普通
# 2:关注
# 3:持仓

__author__ = 'winsert@163.com'

import sqlite3

# 读出所有可转债、可交换债的所有信息
def readCB():
    conn = sqlite3.connect('cb.db')
    curs = conn.cursor()
    sql = "select * from cb" 
    curs.execute(sql)
    tmp = curs.fetchall()
    curs.close()
    conn.close()
    return tmp

# 读出 code=0 的可转债、可交换债的所有信息
def readCB0():
    conn = sqlite3.connect('cb.db')
    curs = conn.cursor()
    sql = "select * from cb where code=0" 
    curs.execute(sql)
    tmp = curs.fetchall()
    curs.close()
    conn.close()
    return tmp

# 读出 code=1 的可转债、可交换债的所有信息
def readCB1():
    conn = sqlite3.connect('cb.db')
    curs = conn.cursor()
    sql = "select * from cb where code=1" 
    curs.execute(sql)
    tmp = curs.fetchall()
    curs.close()
    conn.close()
    return tmp

# 读出 code=2 的可转债、可交换债的所有信息
def readCB2():
    conn = sqlite3.connect('cb.db')
    curs = conn.cursor()
    sql = "select * from cb where code=2" 
    curs.execute(sql)
    tmp = curs.fetchall()
    curs.close()
    conn.close()
    return tmp

# 读出 code=3 的可转债、可交换债的所有信息
def readCB3():
    conn = sqlite3.connect('cb.db')
    curs = conn.cursor()
    sql = "select * from cb where code=3" 
    curs.execute(sql)
    tmp = curs.fetchall()
    curs.close()
    conn.close()
    return tmp

if __name__ == '__main__':

    list0 = readCB0()
    print "\ncode = 0 共有：" + str(len(list0))
    for i in list0:
        print i[3],

    list1 = readCB1()
    print "\n\ncode = 1 共有：" + str(len(list1))
    for i in list1:
        print i[3],

    list2 = readCB2()
    print "\n\ncode = 2 共有：" + str(len(list2))
    for i in list2:
        print i[3],
    
    list3 = readCB3()
    print "\n\ncode = 3 共有：" + str(len(list3))
    for i in list3:
        print i[3],
    print "\n"