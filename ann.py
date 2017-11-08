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

if __name__ == '__main__':
    
    itchat.login(enableCmdQR=2)
    #itchat.auto_login(enableCmdQR=2) # 通过二维码登录微信

    startMsg = u'不挑戏，不逃戏，不入戏，不调戏'
    restStartMsg = 'Have a good Lunch !'
    restEndMsg = 'Good Afternoon !'
    endMsg =  "I will come back !"
    newPriceMsg =  u"没有可转债满足 买入条件。"
    HPriceMsg =  u"没有可转债满足 高价折扣法 。"

    # 选定微信接收人
    account = itchat.get_friends()
    for user in account:
        if user['NickName'] == 'Andy':
            userName = user['UserName']

    now_time = datetime.now()
    today_year = now_time.year
    today_month = now_time.month
    today_day = now_time.day
    #print today_year, today_month, today_day

    rest_starttime = datetime(today_year, today_month, today_day, 11, 29, 59) # 设定午间休息开始时间11:29:59。
    rest_endtime = datetime(today_year, today_month, today_day, 12, 59, 59) # 设定午间休息结束时间12:59:59。
    pause_time = datetime(today_year, today_month, today_day, 14, 59, 59) # 设定程序每天暂停运行的时间:14:59:59。
    start_time = datetime(today_year, today_month, today_day, 9, 25, 59) # 设定程序每天重新运行的时间:09:25:59。
    #print end_time

    print startMsg
    print
    itchat.send(startMsg, 'filehelper')
    itchat.send(startMsg, toUserName = userName)

    while 1:

        # 运行时间>= 09:25:59 and <= 14:59:59
        if datetime.now() >= start_time and datetime.now() <= pause_time :

            # 判断午体时间
            if datetime.now() >= rest_starttime and datetime.now() <= rest_endtime :
                print time.asctime(time.localtime(time.time())) #显示查询时间
                print restStartMsg
                print 
                itchat.send(restStartMsg, toUserName = userName)

                time.sleep(5500) #午休时长5500秒

                print time.asctime(time.localtime(time.time())) #显示查询时间
                print restEndMsg
                print 
                itchat.send(restEndMsg, toUserName = userName)


            #print datetime.now()
            print time.asctime(time.localtime(time.time())) #显示查询时间

            # 三线分析：
            msglist = getCB() #查询是否有CB满足三线买入条件
            if len(msglist) == 0: #没有满足条件的CB
                print newPriceMsg
                #itchat.send(newPriceMsg, 'filehelper')
            else:    
                for msg in msglist: #有满足条件的CB
                    print msg
                    print
                    #itchat.send(time.ctime(), 'filehelper')
                    #itchat.send(msg, 'filehelper')
                    itchat.send(msg, toUserName = userName)

            # 高价折扣法分析
            HPlist = getHP() #查询是否CB满足高价折扣法
            if len(HPlist) == 0: #没有满足高价折扣法的CB
                print HPriceMsg
                print
                #itchat.send(HPriceMsg, 'filehelper')
            else:
                for hpMsg in HPlist: #有满足高价折扣法的CB
                    print hpMsg
                    #print
                    #itchat.send(hpMsg, 'filehelper')
                    itchat.send(hpMsg, toUserName = userName)

            time.sleep(180)  # 延时查询的秒数,180即延时3分钟查询一次。

        else:
            
            #计算转债的强赎天数：
            qsMsgList = getQS()
            if len(qsMsgList) > 0:
                for qsMsg in qsMsgList:
                    print qsMsg
                    itchat.send(qsMsg, toUserName = userName)

            print time.asctime(time.localtime(time.time())) #显示查询时间
            print endMsg
            print
            itchat.send(endMsg, toUserName='filehelper')
            itchat.send(endMsg, toUserName = userName)

            time.sleep(64200)  # 延时64800秒(18小时)后再继续运行
