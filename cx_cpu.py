#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询CPU温度的模块。

__author__ = 'Andy'

import os

# 查询CPU温度
def getCpuTemp():
    cputemp=os.popen('vcgencmd measure_temp').readline()
    sumcputemp=float(cputemp.replace("temp=","").replace("'C\n",""))
    #print u'CPU温度：'+str(sumcputemp)+u' ℃'
    return sumcputemp

def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

if __name__ == '__main__':
    print u'CPU温度：'+str(getCpuTemp())+u' ℃'
