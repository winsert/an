#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 通过微信查询可转债、指数、外汇等价格信息。

__author__ = 'Andy'

import os, sys
import time
from datetime import datetime
import itchat

from cx_wh import getWH
from cx_cb import getCB
from cx_cx import getCX
from cx_ex import getEX
#from cx_pm import getPM25
from cx_cpu import getCpuTemp
from cx_tqsk import getWeather
from cx_jrtq import getToday
from cx_index import getIndex

# 获得帮助
def getHelp():
    print help_msg
    return help_msg

@itchat.msg_register(itchat.content.TEXT)
def main(msg):

    #if msg['ToUserName'] != 'filehelper': return

    try:
        print msg['Text']
        tmp_list = list(msg['Text'])
        cc = tmp_list[0]+tmp_list[1]
        xx = tmp_list[2]+tmp_list[3]
    except:
        cc = ''

    if cc == 'cx':
        result = getCX(xx)
        print time.ctime()
        print result
        print
        itchat.send(result, 'filehelper')

    elif cc == 'ex':
        result = getEX(xx)
        print time.ctime()
        print result
        print
        itchat.send(result, 'filehelper')

    elif msg['Text'] == 'help':
        result = getHelp()
        print time.ctime()
        itchat.send(result, 'filehelper')

    elif msg['Text'] == 'tq':
        result = getToday()
        print time.ctime()
        print
        itchat.send(time.ctime(), 'filehelper')
        itchat.send(result, 'filehelper')

    elif msg['Text'] == 'cpu':
        result = u'CPU温度：'+str(getCpuTemp())+u' ℃'
        print time.ctime()
        print
        itchat.send(result, 'filehelper')

    elif msg['Text'] == 'sk':
        result = getWeather()
        print time.ctime()
        print
        itchat.send(result, 'filehelper')

    elif msg['Text'] == 'pm':
        #result = getPM25()
        result = getHelp()
        print time.ctime()
        print
        itchat.send(result, 'filehelper')

    elif msg['Text'] == 'cb':
        print time.ctime()
        result = getCB()
        for cbMsg in result:
            print cbMsg
            itchat.send(cbMsg, 'filehelper')
        print

    elif msg['Text'] == 'wh':
        print time.ctime()
        result = getWH()
        for whMsg in result:
            print whMsg
            itchat.send(whMsg, 'filehelper')
        print

    elif msg['Text'] == 'in':
        print time.ctime()
        result = getIndex()
        for indexMsg in result:
            print indexMsg
            itchat.send(indexMsg, 'filehelper')
        print

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
输入'help'：查询帮助
输入'cpu'：查询CPU温度
输入'tq'：查询今日天气
输入'sk'：查询天气实况
输入'pm'：查询PM2.5数据
输入'cb'：查询入线可转债
输入'wh'：查询外汇信息
输入'in'：查询指数涨跌幅
输入'cx+缩写'：查CB信息
输入'ex+缩写'：查EB信息
输入'off'：网页微信Logout
"""

if __name__ == '__main__':

    itchat.auto_login(enableCmdQR=2) # 通过二维码登录微信
    #itchat.auto_login(hotReload=True)

    itchat.send(help_msg, 'filehelper')

    itchat.run()
