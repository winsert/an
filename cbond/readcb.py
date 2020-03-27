#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 读出 code = ?的可转债、可交换债的所有信息
# 0:已强赎
# 1:普通
# 2:关注
# 3:持仓

__author__ = 'winsert@163.com'

import sqlite3

# 读出指定 code 的所有可转债、可交换债的所有信息
def readCB(code):
    cblists = []
    if code >= 0 :
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select * from cb where code = %r" %code
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()
    else:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select * from cb where code > 0"
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

    for tlist in tmp:
        cblist = list(tlist) #将元组tuple转换成list
        cblists.append(cblist)
        
    return cblists

if __name__ == '__main__':

    print u"\n列表code =-1: 普通+关注+持仓"
    print u"列表code = 0: 已强赎"
    print u"列表code = 1: 普通"
    print u"列表code = 2: 关注"
    print u"列表code = 3: 持仓\n"
    
    code = int(raw_input("要查询的code?"))
    cblists = readCB(code)
    print "\ncode = " + str(code)+ u" 共有：" + str(len(cblists))
    for i in cblists:
        print i[3],
    print '\n'