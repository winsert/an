#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 通过微信查询可转债、指数、外汇等价格信息。

__author__ = 'Andy'

import os, sys
import time
from datetime import datetime
import itchat

from cx_wh import getWH
from cx_tk import getTK
from cx_sp import getSP
from cx_cb import getCB
from cx_cx import getCX
from cx_zg import getZG
from cx_pm import getPM
from cx_tqsk import getWeather
from cx_jrtq import getToday
from cx_index import getIndex
from cx_raspi import getCpuTemp
from cx_raspi import getDiskSpace

# 获得帮助
def getHelp():
    print help_msg
    return help_msg

# 发送单条信息
def sendMsg(result):
    msg = result
    print msg
    print time.ctime()
    print
    itchat.send(msg, 'filehelper')

#发送多条信息
def sendMsgList(result):
    msgList = result
    print time.ctime()
    for msg in msgList:
        print msg
        itchat.send(msg, 'filehelper')
    print

@itchat.msg_register(itchat.content.TEXT)
def main(msg):

    #if msg['ToUserName'] != 'filehelper': return

    try:
        print msg['Text']
        tmp = msg['Text']
        cc = tmp[0:2]
        #print 'cc = ',cc
        xx = tmp[2:]
        #print 'xx = ', xx
    except:
        cc = ''

    if cc == 'cx':
        result = getCX(xx)
        sendMsg(result)

    elif cc == 'tk':
        result = getTK(xx)
        sendMsg(result)

    elif cc == 'zg':
        zg_name, zg_new, zg_zdf = getZG(xx) #查询股票价名称,价格和涨跌幅
        #print zg_name, zg_new, zg_zdf
        result = zg_name+u'\n最新价:'+zg_new+u'\n涨跌幅:'+zg_zdf 
        sendMsg(result)

    elif msg['Text'] == 'h':
        result = getHelp()
        sendMsg(result)

    elif msg['Text'] == 'tq':
        result = getToday()
        sendMsg(result)

    elif msg['Text'] == 'cpu':
        result = getCpuTemp()
        sendMsg(result)

    elif msg['Text'] == 'disk':
        result = getDiskSpace()
        sendMsg(result)

    elif msg['Text'] == 'sk':
        result = getWeather()
        sendMsg(result)

    elif msg['Text'] == 'pm':
        result = getPM()
        sendMsg(result)

    elif msg['Text'] == 'cb':
        result = getCB()
        sendMsgList(result)

    elif msg['Text'] == 'wh':
        result = getWH()
        sendMsgList(result)

    elif msg['Text'] == 'in':
        result = getIndex()
        sendMsgList(result)

    elif msg['Text'] == 'sp':
        result = getSP()
        sendMsgList(result)

    elif msg['Text'] == 'off':
        print time.ctime()
        print u"网页微信Logout"
        itchat.send(u"网页微信Logout", 'filehelper')
        itchat.logout()

    else:
        print time.ctime()
        print 'What is it ?'
        itchat.send('What is it ?', 'filehelper')

help_msg = u"""
使用说明：
输入'h'：查询帮助
输入'tq'：查询今日天气
输入'sk'：查询天气实况
输入'pm'：查询PM2.5数据
输入'cb'：查询入线可转债
输入'wh'：查询外汇信息
输入'sp'：查询商品信息
输入'in'：查询指数涨跌幅
输入'cx+缩写'：查转债信息
输入'tk+缩写'：查转债条款
输入'zg+代码'：查股票价格
输入'disk'：DISK使用情况
输入'cpu'：查询CPU温度
输入'off'：网页微信Logout
"""

if __name__ == '__main__':

    itchat.auto_login(enableCmdQR=2) # 通过二维码登录微信
    #itchat.auto_login(hotReload=True)

    itchat.send(help_msg, 'filehelper')

    itchat.run()
