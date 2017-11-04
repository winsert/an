#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 通过微信查询可转债、指数、外汇等价格信息。

__author__ = 'Andy'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os, time
from datetime import datetime

from qqbot import QQBotSlot as qqbotslot, RunBot

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
    bot.SendTo(contact, msg)

#发送多条信息
def sendMsgList(result):
    msgList = result
    print time.ctime()
    for msg in msgList:
        print msg
        bot.SendTo(contact, msg)
    print

@qqbotslot
def onQQMessage(bot, contact, member, content):

    try:
        print "接收到的content：", content
        cc = content[0:2]
        print 'cc = ', cc
        xx = content[2:]
        print 'xx = ', xx
    except:
        cc = ''

    if cc == 'cx':
        result = getCX(xx)
        print result
        bot.SendTo(contact, result)

    elif cc == 'tk':
        result = getTK(xx)
        bot.SendTo(contact, result)

    elif cc == 'zg':
        result = getZG(xx) #查询股票价名称,价格和涨跌幅
        bot.SendTo(contact, result)

    elif content == 'h':
        result = getHelp()
        bot.SendTo(contact, result)

    elif content == 'tq':
        result = getToday()
        bot.SendTo(contact, result)

    elif content == 'cpu':
        result = getCpuTemp()
        bot.SendTo(contact, result)

    elif content == 'disk':
        result = getDiskSpace()
        bot.SendTo(contact, result)

    elif content == 'sk':
        result = getWeather()
        bot.SendTo(contact, result)

    elif content == 'pm':
        result = getPM()
        bot.SendTo(contact, result)

    elif content == 'cb':
        result = getCB()
        bot.SendTo(contact, result)

    elif content == 'wh':
        result = getWH()
        bot.SendTo(contact, result)

    elif content == 'in':
        result = getIndex()
        bot.SendTo(contact, result)

    elif content == 'sp':
        result = getSP()
        bot.SendTo(contact, result)

    elif content == 'off':
        print time.ctime()
        print 'STOP QQBot'
        bot.SendTo(contact, 'STOP QQBot')
        bot.Stop()

    else:
        print time.ctime()
        print 'What is it ?'
        bot.SendTo(contact, 'What is it ?')

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
输入'off'：STOP QQBot
"""

if __name__ == '__main__':

    RunBot()
