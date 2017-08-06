#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 获取可转债、可交换债的条款等信息

__author__ = 'winsert@163.com'

import sqlite3
from datetime import datetime

# 计算剩余年限
def getSYNX(dqr):
    ymd = dqr #到期日
    y = ymd.split('-')
    d1 = datetime(int(y[0]), int(y[1]), int(y[2]), 0, 0)
    synx = round((d1 - datetime.now()).days / 365.00, 2)
    return synx

# 主程序
def getTK(alias):
    
    cx = alias
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select name, Code, position, zgdm, zgqsr, zgj, hsqsr, hsj, dqr, shj, zgjxt, qzsh, hs from cb where Alias = '%s'" %cx
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

        if tmp[0][2] == 'QS':
            msg = tmp[0][0]+u' :已强赎'
            return msg

        name = tmp[0][0] #转债名称
        code = str(tmp[0][1]) #转债代码
        position = str(tmp[0][2]) #已购买的张数
        zgdm = str(tmp[0][3]) #转股代码
        zgqsr = str(tmp[0][4]) #转股起始日
        zgj = str(tmp[0][5]) #转股价
        hsqsr = str(tmp[0][6]) #回售起始日
        hsj = str(tmp[0][7]) #回售价
        dqr = str(tmp[0][8]) #到期日
        shj = str(tmp[0][9]) #赎回价
        zgjxt = tmp[0][10] #下调转股价条款
        qzsh = tmp[0][11] #强制赎回条款
        hs = tmp[0][12] #回售条款
        synx = str(getSYNX(dqr)) #计算剩余年限

        msg = name+':'+code+u'\n仓位:'+position+u'\n转股起始日:'+zgqsr+u'\n转股价:'+zgj+u'\n转股代码:'+zgdm+u'\n回售起始日:'+hsqsr+u'\n回售价:'+hsj+u'\n到期日:'+dqr+u'\n剩余年限:'+synx+u'\n赎回价:'+shj+'\n'+u'\n下调转股价条款:'+'\n'+zgjxt+'\n'+u'\n强制赎回条款:'+'\n'+qzsh+'\n'+u'\n回售条款:'+'\n'+hs

        #print msg
        return msg

    except Exception, e:
        print e
        msg = e
        return msg

if __name__ == '__main__':
    
    while 1:
        alias = raw_input('输入可转债名称的缩写：')
        print getTK(alias)
        print
