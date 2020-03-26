#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 自动获取可转债的最新价进行"三线"和"高价折扣法"分析，并用微信发送通知

__author__ = 'winsert@163.com'

#import itchat, time
import itchat, time
from sys import exit
from datetime import datetime

from cbond.readcb import readCB #读出 code!= 0 的可转债,可交换债的所有信息
from cbond.readcb import readCB3 #读出 code=3(持仓) 可转债,可交换债的所有信息
from cbond.cxcb import getCB #进行高价折扣和三线分析的模块
from cbond.cxqs import getQS #强赎模块
from cbond.cxindex import getIndex #指数模块

if __name__ == '__main__':
    
    # 持仓的转债列表
    list3 = readCB3()

    #要查询的指数代码
    index = {
        u'50ETF':'sh510050',
        u'300ETF':'sh510300',
        u'500ETF':'sh510500',
        u'创业板ETF':'sz159915',
        u'证券ETF':'sh512880',
        u'红利ETF':'sh510880',
        u'H股ETF':'sh510900',
        u'深证成指':'sz399001',
        } 
    
    itchat.login(enableCmdQR=2)

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

            # 查询指数
            for k in index.keys():
                value = index.get(k)
                index_zz = getIndex(value)
                index_msg = k+' : '+str(index_zz)
                print index_msg
                itchat.send(index_msg, toUserName = userName)

            time.sleep(5400)

            print time.asctime(time.localtime(time.time())) #显示查询时间
            print restEndMsg
            print 
            itchat.send(restEndMsg, toUserName = userName)

        #print datetime.now()
        print time.asctime(time.localtime(time.time())) #显示查询时间
        
        # 高价折扣和三线分析：
        i = 0
        for cblist in list3:
            #查询持仓转债是否有满足三线买入条件，return msg和转债最新价
            msg, newHPrice, newLPrice, zdf = getCB(cblist)
            if msg != 'ok': # msg='ok',无提醒信息
                print 'return msg is ok.'
                itchat.send(msg, toUserName = userName)
            if newHPrice > cblist[10]: #如果转债最新价>原最高价，则修改新高价
                list3[i][10] = newHPrice
            if newLPrice < cblist[11]: #如果转债最新价<原最低价，则修改新低价
                list3[i][11] = newLPrice
            if abs(zdf) > cblist[-1]: #如果转债最新价<原最低价，则修改新低价
                msg = cblist[3]+u' 涨跌幅='+str(zdf)+'%!'
                itchat.send(msg, toUserName = userName)
                list3[i][-1] = abs(zdf)
            i = i +1

        time.sleep(100)  # 延时查询的秒数,120即延时2分钟查询一次。

    # 查询指数收盘的涨跌情况
    for k in index.keys():
        value = index.get(k)
        index_zz = getIndex(value)
        index_msg = k+' : '+str(index_zz)
        print index_msg
        itchat.send(index_msg, toUserName = userName)
    
    # code!= 0 的转债列表(非强赎转债)
    listCB = readCB()
    #计算转债的强赎天数，更新最高价和最低价：
    qsMsgList = getQS(listCB)
    if len(qsMsgList) > 0:
        for qsMsg in qsMsgList:
            print qsMsg
            itchat.send(qsMsg, toUserName = userName)
    
    print time.asctime(time.localtime(time.time())) #显示查询时间
    itchat.send(endMsg, toUserName='filehelper')
    itchat.send(endMsg, toUserName = userName)
    itchat.logout()
    exit()
