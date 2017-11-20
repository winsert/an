#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于修改jian, jia, zhong, note, position, zgj数据

__author__ = 'winsert@163.com'

import sqlite3

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# 查询指定转债的数据
def CX(alias):
    
    cx = alias
    tmp = []
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select name, jian, jia, zhong, note, position, zgj from cb where Alias = '%s'" %cx
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

        name = tmp[0][0] #转债名称
        jian = tmp[0][1] #建仓价
        jia = tmp[0][2] #建仓价
        zhong = tmp[0][3] #建仓价
        note = tmp[0][4] #说明
        position = tmp[0][5] #持仓
        zgj = tmp[0][6] #转股价

        print
        print u'名  称：', name
        print u'建仓价：', jian
        print u'加仓价：', jia
        print u'重仓价：', zhong
        print u'说  明：', note
        print u'持  仓：', position
        print u'转股价：', zgj
        print

        tmp.append(jian)
        tmp.append(jia)
        tmp.append(zhong)
        tmp.append(note)
        tmp.append(position)
        tmp.append(zgj)
        return tmp 

    except Exception, e :
        print 'CX() Error:', e
        sys.exit()

#对指定转债的'建仓价'进行修改
def Jian(alias, jian):
    alias = alias
    jian = float(jian)

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "UPDATE cb SET jian = ? WHERE Alias = ?"
        curs.execute(sql, (jian, alias))
        conn.commit()
        curs.close()
        conn.close()

        print u'建仓价 已修改为：', str(jian)

    except Exception, e:
        print 'Jian() ERROR :', e
        sys.exit()

#对指定转债的'加仓价'进行修改
def Jia(alias, jia):
    alias = alias
    jia = float(jia)

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "UPDATE cb SET jia = ? WHERE Alias = ?"
        curs.execute(sql, (jia, alias))
        conn.commit()
        curs.close()
        conn.close()

        print u'加仓价 已修改为：', str(jia)

    except Exception, e:
        print 'Jia() ERROR :', e
        sys.exit()

#对指定转债的'重仓价'进行修改
def Zhong(alias, zhong):
    alias = alias
    zhong = float(zhong)

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "UPDATE cb SET zhong = ? WHERE Alias = ?"
        curs.execute(sql, (zhong, alias))
        conn.commit()
        curs.close()
        conn.close()

        print u'重仓价 已修改为：', str(zhong)

    except Exception, e:
        print 'Zhong() ERROR :', e
        sys.exit()

#对指定转债的‘说明’进行修改
def Note(alias, note):
    alias = alias
    note = note

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "UPDATE cb SET note = ? WHERE Alias = ?"
        curs.execute(sql, (note, alias))
        conn.commit()
        curs.close()
        conn.close()

        print u'说明 已修改为：', str(note)

    except Exception, e:
        print 'Note() ERROR :', e
        sys.exit()

#对指定转债的'持仓'进行修改
def Position(alias, position):
    alias = alias
    position = int(position)

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "UPDATE cb SET position = ? WHERE Alias = ?"
        curs.execute(sql, (position, alias))
        conn.commit()
        curs.close()
        conn.close()

        print u'持仓 已修改为：', str(position)

    except Exception, e:
        print 'Position() ERROR :', e
        sys.exit()

#对指定转债的'转股价'进行修改
def ZGJ(alias, zgj):
    alias = alias
    zgj = float(zgj)

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "UPDATE cb SET zgj = ? WHERE Alias = ?"
        curs.execute(sql, (zgj, alias))
        conn.commit()
        curs.close()
        conn.close()

        print u'转股价 已修改为：', str(zgj)

    except Exception, e:
        print 'ZGJ() ERROR :', e
        sys.exit()

if  __name__ == '__main__': 

    msg = u"""
    本程序用于修改：
    - 建仓价 jian
    - 加仓价 jia
    - 重仓价 zhong
    - 说  明 note
    - 持  仓 position
    - 转股价 zgj
    """
    print
    print msg
    alias = raw_input(u'输入可转债的简称缩写：')
    cx = CX(alias)
    yn = raw_input(u'是否要修改(y/n)？')
    if yn == 'n':
        sys.exit()

    print
    print u'原 建仓价：', str(cx[1])
    jian = raw_input(u"请输入新 建仓价：")
    if jian != '':
        Jian(alias, jian)
    else:
        print u'建仓价 没有修改！'

    print
    print u'原 加仓价：', str(cx[2])
    jia = raw_input(u"请输入新 加仓价：")
    if jia != '':
        Jia(alias, jia)
    else:
        print u'加仓价 没有修改！'

    print
    print u'原 重仓价：', str(cx[3])
    zhong = raw_input(u"请输入新 重仓价：")
    if zhong != '':
        Zhong(alias, zhong)
    else:
        print u'重仓价 没有修改！'

    print
    print u'原 说明：', str(cx[4])
    note = unicode(raw_input(u"请输入新 说明："))
    if note != '':
        Note(alias, note)
    else:
        print u'说明 没有修改！'

    print
    print u'原 持仓：', str(cx[5])
    position = raw_input(u"请输入新 持仓：")
    if position != '':
        Position(alias, position)
    else:
        print u'持仓 没有修改！'

    print
    print u'原 转股价：', str(cx[6])
    zgj = raw_input(u"请输入新 转股价：")
    if zgj != '':
        ZGJ(alias, zgj)
    else:
        print u'转股价 没有修改！'
