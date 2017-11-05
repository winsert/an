#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 通过微信查询可转债、指数、外汇等价格信息。

__author__ = 'Andy'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os, time

from qqbot import QQBotSlot as qqbotslot, RunBot

from cx_wh import getWH #查询外汇
from cx_tk import getTK #查询转债，交换债条款
from cx_sp import getSP #查询商品
from cx_cb import getCB #查询全部入线的转债，交换债
from cx_cx import getCX #查询指定转债，交换债 例：蓝标转债,cxlb
from cx_zg import getZG #查询指定股票 例：平安银行 zg000001
from cx_pm import getPM #查询PM
from cx_tqsk import getWeather #查询天气实况
from cx_jrtq import getToday #查询今日天气
from cx_index import getIndex #查询证券指数
from cx_raspi import getCpuTemp #查询CPU温度
from cx_raspi import getDiskSpace #查询磁盘空间

@qqbotslot
def onQQMessage(bot, contact, member, content):

    #print "接收到的content：", content

    try:
        if content[0:2] == 'cx':
            result = getCX(content[2:])
            bot.SendTo(contact, result)

        elif content[0:2] == 'tk':
            result = getTK(content[2:])
            bot.SendTo(contact, result)

        elif content[0:2] == 'zg':
            result = getZG(content[2:]) #查询股票价名称,价格和涨跌幅
            bot.SendTo(contact, result)

        elif content == 'h':
            result = help_msg #显示帮助信息
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
            for msg in result:
                bot.SendTo(contact, msg)

        elif content == 'wh':
            result = getWH()
            for msg in result:
                bot.SendTo(contact, msg)

        elif content == 'in':
            result = getIndex()
            for msg in result:
                bot.SendTo(contact, msg)

        elif content == 'sp':
            result = getSP()
            for msg in result:
                bot.SendTo(contact, msg)

        elif content == 'off':
            bot.SendTo(contact, 'STOP QQBot')
            bot.Stop()

        else:
            print '============== What is it ? ==================='
            bot.SendTo(contact, 'What is it ?')

    except Exception, e:
        print 'QQBot ERROR :', e
        bot.SendTo(contact, e)

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
