#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 自动获取可转债、可交换债的最新价进行"三线"和"高价折扣法"分析

__author__ = 'winsert@163.com'

import itchat, time
from sys import exit
from datetime import datetime

from cxcb import getCB #查询可转债,可交换债是否满足三线的模块
from cxhp import getHP #高价折扣模块
from cxqs import getQS #强赎模块
from cxindex import getIndex #指数模块

startMsg = u'不挑戏，不逃戏，不入戏，不调戏'
restStartMsg = 'Have a good Lunch !'
restEndMsg = 'Good Afternoon !'
endMsg =  "I will come back !"
OKMsg = 'Everything is OK.'

itchat.login(enableCmdQR=2) #登录微信
# 选定微信接收人
account = itchat.get_friends()
for user in account:
    if user['NickName'] == 'Andy':
        userName = user['UserName']

#启动程序后发送开始信息
print time.asctime(time.localtime(time.time())) #显示启动程序的时间
print startMsg
print
itchat.send(startMsg, 'filehelper')
itchat.send(startMsg, toUserName = userName)

#主程序
while 1:

    #时间设定
    now_time = datetime.now()
    today_year = now_time.year
    today_month = now_time.month
    today_day = now_time.day
    #print today_year, today_month, today_day

    time0 = datetime(today_year, today_month, today_day, 0, 0, 0) ##
    time1 = datetime(today_year, today_month, today_day, 9, 30, 0) # 设定交易开始时间:09:30:0。
    time2 = datetime(today_year, today_month, today_day, 15, 0, 0) # 设定交易结束时间:15:0:0。
    time3 = datetime(today_year, today_month, today_day, 11, 30, 0) # 设定午间休息开始时间11:30:0。
    time4 = datetime(today_year, today_month, today_day, 13, 0, 0) # 设定午间休息结束时间13:0:0。
    time5 = datetime(today_year, today_month, today_day, 15, 4, 59) ##
    time6 = datetime(today_year, today_month, today_day, 23, 59, 59) ##
    time7 = datetime(today_year, today_month, today_day, 9, 0, 0) ##
    time8 = datetime(today_year, today_month, today_day, 9, 25, 0) ##

    # 运行时间>= 09:25:59 and <= 14:59:59
    if datetime.now() >= time1 and datetime.now() <= time2 :

        # 判断午体时间 >= 11:29:59 and <= 12:59:59
        if datetime.now() >= time3 and datetime.now() <= time4 :
            print time.asctime(time.localtime(time.time())) #显示查询时间
            print restStartMsg
            print 
            itchat.send(restStartMsg, toUserName = userName) #发送开始午休信息

            time.sleep(5400) #午休时长5400秒

            print time.asctime(time.localtime(time.time())) #显示查询时间
            print restEndMsg
            print 
            itchat.send(restEndMsg, toUserName = userName) #发送结束午休信息

        #print datetime.now()
        print time.asctime(time.localtime(time.time())) #显示查询时间

        # 三线分析：
        msglist = getCB() #查询是否有CB,EB满足三线买入条件
        if len(msglist) > 0: #有满足条件的CB,EB
            for msg in msglist: 
                print msg
                print
                #itchat.send(msg, 'filehelper')
                itchat.send(msg, toUserName = userName)

        # 高价折扣法分析
        HPlist = getHP() #查询是否CB满足高价折扣法
        if len(HPlist) > 0: #有满足高价折扣法的CB
            for hpMsg in HPlist:
                print hpMsg
                #itchat.send(hpMsg, 'filehelper')
                itchat.send(hpMsg, toUserName = userName)

        print OKMsg
        print
        time.sleep(180)  # 延时查询的秒数,180即延时3分钟查询一次。

    elif datetime.now() >= time2 and datetime.now() <= time5 :
            
        # 查询指数收盘的涨跌情况
        index = {u'上证50':'sh000016', u'深圳成指':'sz399001', u'上证指数':'sh000001', u'沪深300':'sz399300', u'中证500':'sh000905', u'创业板':'sz399006', u'B股':'sh000003', u'深次新股':'sz399678', u'国债':'sh000012'} #要查询的指数代码
        for k in index.keys():
            value = index.get(k)
            index_zz = getIndex(value)
            if index_zz >=1.5 or index_zz <= -1.5 : #指数涨跌幅超过1.5%时
                index_msg = k+' : '+ str(index_zz)
                print index_msg
                itchat.send(index_msg, 'filehelper')
                itchat.send(index_msg, toUserName = userName)

        #计算转债的强赎天数：
        qsMsgList = getQS()
        if len(qsMsgList) > 0:
            for qsMsg in qsMsgList:
                print qsMsg
                itchat.send(qsMsg, toUserName = userName)

        print time.asctime(time.localtime(time.time())) #显示查询时间
        print endMsg
        print
        itchat.send(endMsg, toUserName='filehelper') #发送交易时间结束信息
        itchat.send(endMsg, toUserName = userName) #发送交易时间结束信息
        time.sleep(300)  # 延时查询的秒数,300即延时5分钟查询一次。

    elif datetime.now() >= time5 and datetime.now() <= time6 :
        
        print time.asctime(time.localtime(time.time())) #显示查询时间
        print
        time.sleep(3700)  # 延时3600秒(60分钟)后再继续运行
        itchat.send(OKMsg, 'filehelper')

    elif datetime.now() >= time0 and datetime.now() <= time7 :
        print time.asctime(time.localtime(time.time())) #显示查询时间
        print
        time.sleep(1800)  # 延时1800秒(30分钟)后再继续运行
        itchat.send(OKMsg, 'filehelper')

    elif datetime.now() >= time7 and datetime.now() <= time1 : #校时
        print time.asctime(time.localtime(time.time())) #显示查询时间
        print
        if datetime.now() >= time8 and datetime.now() <= time1 : #开盘前5分钟
            itchat.send(startMsg, 'filehelper')
            itchat.send(startMsg, toUserName = userName)

        time.sleep(300)  # 延时300秒(5分钟)后再继续运行
