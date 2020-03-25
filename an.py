#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 自动获取可转债的最新价进行"三线"和"高价折扣法"分析，并用微信发送通知

__author__ = 'winsert@163.com'

import itchat, time
from sys import exit
from datetime import datetime

from cbond.cxcb import getCB #查询可转债,可交换债是否满足三线的模块
from cbond.readcb import readCB2 #读出 code=2(关注) 可转债,可交换债的所有信息
from cbond.readcb import readCB3 #读出 code=3(持仓) 可转债,可交换债的所有信息
from cbond.cxhp import getHP #高价折扣模块
#from cxwh import getWH #查询外汇模块
#from cxjj import getJJ #查询基金模块
#from cx_stock import getStock #查询股票模块
from cbond.cxqs import getQS #强赎模块
from cbond.cxindex import getIndex #指数模块

if __name__ == '__main__':
    
    list2 = readCB2()
    print list2
    list3 = readCB3()
    '''
    itchat.login(enableCmdQR=2)
    #itchat.auto_login(enableCmdQR=2) # 通过二维码登录微信

    startMsg = u'不挑戏，不逃戏，不入戏，不调戏'
    restStartMsg = 'Have a good Lunch !'
    restEndMsg = 'Good Afternoon !'
    endMsg =  "I will come back !"
    newPriceMsg =  u"没有可转债满足 买入条件。"
    HPriceMsg =  u"没有可转债满足 高价折扣法 。"
    WHmsg = u"外汇一切正常 !"
    STmsg = u"Stock一切正常 !"
    JJmsg = u"基金一切正常 !"

    account = itchat.get_friends()
    for user in account:
        #if user['NickName'] == 'ken':
        #if user['NickName'] == 'Andy':
        if user['NickName'] == 'andy130':
            userName = user['UserName']

    now_time = datetime.now()
    today_year = now_time.year
    today_month = now_time.month
    today_day = now_time.day
    #print today_year, today_month, today_day

    rest_starttime = datetime(today_year, today_month, today_day, 11, 29, 59) # 设定午间休息开始时间11:29:59。
    rest_endtime = datetime(today_year, today_month, today_day, 12, 59, 59) # 设定午间休息结束时间12:59:59。
    end_time = datetime(today_year, today_month, today_day, 14, 59, 59) # 设定程序每天运行的结束时间到当天的14:59:59。
    #print end_time

    print startMsg
    print
    itchat.send(startMsg, 'filehelper')
    itchat.send(startMsg, toUserName = userName)

    while datetime.now() < end_time:

        # 判断午体时间
        if datetime.now() >= rest_starttime and datetime.now() <= rest_endtime :
            print time.asctime(time.localtime(time.time())) #显示查询时间
            print restStartMsg
            print 
            itchat.send(restStartMsg, toUserName = userName)

            index = {
                u'50ETF':'sh510050',
                u'300ETF':'sh510300',
                u'500ETF':'sh510500',
                u'创业板ETF':'sz159915',
                u'证券ETF':'sh512880',
                u'红利ETF':'sh510880',
                u'H股ETF':'sh510900',
                u'深证成指':'sz399001',
                } #要查询的指数代码
    
            for k in index.keys():
                value = index.get(k)
                index_zz = getIndex(value)
                index_msg = k+' : '+str(index_zz)
                print index_msg
                #itchat.send(index_msg, 'filehelper')
                itchat.send(index_msg, toUserName = userName)

            time.sleep(5500)

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

        # 查询stock价格是否低(高)于预设值
        #STlist = getStock()
        #if len(STlist) == 0: #没有满足条件stock
            #print STmsg
            #print
        #else:
            #for stMsg in STlist: #有满足条件的Stock
                #print stMsg
                #itchat.send(stMsg, toUserName = userName)

        # 查询外汇价格是否低于预设值
        #WHlist = getWH()
        #if len(WHlist) == 0: #没有满足条件的外汇
            #print WHmsg
            #print
        #else:
            #for whMsg in WHlist: #有满足条件的外汇
                #print whMsg
                #itchat.send(whMsg, toUserName = userName)

        # 查询基金价格是否低于预设值
        #JJlist = getJJ()
        #if len(JJlist) == 0: #没有满足条件的基金
            #print JJmsg
            #print
        #else:
            #for jjMsg in JJlist: #有满足条件的基金
                #print jjMsg
                #itchat.send(jjMsg, toUserName = userName)

        time.sleep(120)  # 延时查询的秒数,300即延时5分钟查询一次。

    # 查询指数收盘的涨跌情况
    index = {u'50ETF':'sh510050', u'300ETF':'sh510300', u'500ETF':'sh510500', u'创业板':'sz159915', u'B股':'sh000003', u'证券ETF':'sh512880', u'科技ETF':'sh515000', u'红利ETF':'sh510880'} #要查询的指数代码
    
    for k in index.keys():
        value = index.get(k)
        index_zz = getIndex(value)
        index_msg = k+' : '+str(index_zz)
        print index_msg
        #itchat.send(index_msg, 'filehelper')
        itchat.send(index_msg, toUserName = userName)

    #计算转债的强赎天数：
    qsMsgList = getQS()
    if len(qsMsgList) > 0:
        for qsMsg in qsMsgList:
            print qsMsg
            itchat.send(qsMsg, toUserName = userName)

    print time.asctime(time.localtime(time.time())) #显示查询时间
    itchat.send(endMsg, toUserName='filehelper')
    itchat.send(endMsg, toUserName = userName)
    itchat.logout()
    exit()
    '''