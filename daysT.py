#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于画出每日可交易转债成交金额的折线图
__author__ = 'winsert@163.com'

import sqlite3, datetime

# 查询转债的代码
def getCode():
    
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select ce, code, zzcode, Prefix from cb"
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

        code_list = []

        for code in tmp:
            if code[0] != 'e' and code[1] != 0: #过滤已强赎的转债和交换债
            #if code[2] != 'e': #过滤交换债
                code_list.append(code[2])
        
        #print len(code_list)
        #print code_list
        return code_list
               
    except Exception, e:
        print e
    
# 查询转债的成交金额
def getCbData(n, codes):
    #codes = ['110030', '123031']
    td = '' #记录日期
    cjje = 0 #成交金额
    #print 'n = ', n #倒退天数

    try:
        for code in codes:
            #print code
            code_tab ='c' + code
            #print code_tab
            conn = sqlite3.connect('dd.db')
            curs = conn.cursor()
            sql = "select today, zz_j from %s ORDER BY today desc limit %r, 1" % (code_tab, n) #按倒序查询成交金额
            curs.execute(sql)
            tmp = curs.fetchall()
            curs.close()
            conn.close()
            #print tmp
            
            for cb in tmp:
                td = cb[0]
                #print td
                #print cb[1]
                cjje = cjje + (round((float(cb[1])/10000))) #成交金额多少万元
                #print cjje
        
        #print round(cjje / 10000, 2) #成交金额多少亿元
        return td, round(cjje / 10000, 2)
        
    except Exception, e:
        print e

# 计算剩余年限
def getSYNX(dqr):
    ymd = dqr #到期日
    y = ymd.split('-')
    d1 = datetime.datetime(int(y[0]), int(y[1]), int(y[2]), 0, 0)
    synx = round((d1 - datetime.datetime.now()).days / 365.00, 3)
    return synx

# 计算到期价值
def getDQJZ(synx, shj,  ll):
    synx = synx #剩余年限
    shj = float(shj) #赎回价
    mnlv = ll #每年的利率
    dqjz = 0.0

    int_synx = int(synx)
    if synx > int_synx: 
        synx = int_synx + 1
    else:
        synx = int_synx
    #print synx

    l = mnlv.split(',') #转成列表
    
    for i in range (len(l)-synx, len(l)-1):
        #dqjz = dqjz +round(float(l[i])*0.8, 2)
        dqjz = dqjz + float(l[i])

    dqjz = dqjz + shj
    return dqjz

#查询转债的代码和到期价值
def getCB():
    tmp_lists = []

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select ce, code, name, zzcode, Prefix, dqr, shj, ll from cb"
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

        for cb in tmp:
            ce = cb[0] #区别转债和交换债
            code = cb[1] #特征代码
            name = cb[2] #转债名称
            zzcode = cb[3] #转债代码
            prefix = cb[4]
            dqr = cb[5] #到期日
            shj = cb[6] #赎回价
            ll = cb[7] #每年的利率

            if code != 0 and ce != 'e': #过滤已强赎的转债和交换债
            #if zzcode == '123015':
                #print name
                synx = getSYNX(dqr) #计算剩余年限
                dqjz = getDQJZ(synx, shj, ll) #计算到期价值
                #print dqjz
                tmp_list = []
                tmp_list.append(zzcode)
                tmp_list.append(dqjz)
                tmp_lists.append(tmp_list)
        return tmp_lists

    except Exception, e:
        print 'getCB(): ', e

def getRate(date, cb_lists): #查询日期，转债代码
    zb = 0.0 #收盘价>到期价值的转债占所有转债的比例
    zb_lists = []
    try:    
        zb_list = []
        cSum = 0 #记录转债的总数
        vSum = 0 #记录收盘价>到期价值的转债数量
        
        for cb in cb_lists:
            cl = 'c' + cb[0] #生成表名
            dqjz = float(cb[1]) #到期价值

            conn = sqlite3.connect('dd.db')
            curs = conn.cursor()
            sql = "select today, zz_e from %s" %cl #取日期、转债当日收盘价
            curs.execute(sql)
            dd_tmp = curs.fetchall()
            curs.close()
            conn.close()

            for zz in dd_tmp:
                zz_date = zz[0] #日期
                zz_e = float(zz[1]) #转债收盘价
                if zz_date == date:
                    #print cb[0], cb[1], zz_e
                    cSum = cSum + 1
                    if zz_e > dqjz:
                        #print cb[0], zz_e, dqjz
                        vSum = vSum + 1

        #print date+u'：共有 '+str(cSum)+u' 只转债，其中 '+str(vSum)+u' 只转债的收盘价 > 到期价值。'

        return cSum, vSum

    except Exception, e:
        print 'getRate()', e

def SQL(record): #向数据库insert新记录

    rec = record

    try:
        conn = sqlite3.connect('dd.db')
        curs = conn.cursor()
        sql = "insert into cbt (date, cjje, csum, vsum) VALUES (?, ?, ?, ?)"
        curs.execute(sql, rec)
        conn.commit()
        curs.close()
        conn.close()
        print u"已加入dd.db数据库的cbt表。"
        print
    except Exception,e:
        print "SQL_Error is:", e

if __name__ == '__main__':
    
    days = 1 #查询倒数days天的数据

    codes = getCode() #查询转债的代码
    #print codes
    
    for n in range((days - 1), -1, -1):
        cjje_list = [] #记录每日的成交金额

        cjje = getCbData(n, codes) #查询转债的数据
        #cjje_list.append(n)
        
        print 'date =', cjje[0] #查询日期
        cjje_list.append(cjje[0]) #查询日期
        cjje_list.append(cjje[1]) #成交金额

        cb_lists = getCB() #查询转债的代码和到期价值
        #print cb_lists

        rates = getRate(cjje[0], cb_lists) #查询日期,转债代码
        #print rates

        cjje_list.append(rates[0]) #当日转债总数
        cjje_list.append(rates[1]) #收盘价>到期价值的转债数量
        print cjje_list

        print u"是否增加 " + cjje[0] + u" 的数据？",
        yn = raw_input("(y/n) ?")

        if yn == 'y':
            print u"\n正在增加 " + cjje[0] + u" 的数据......"
            SQL(cjje_list)    
            print u"\n操作已完成。"
        elif yn == 'n':
            print u"\n没有增加新数据。"