#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询CPU温度的模块。

__author__ = 'Andy'

import os

# 查询CPU温度
def getCpuTemp():
    cputemp=os.popen('vcgencmd measure_temp').readline()
    sumcputemp=float(cputemp.replace("temp=","").replace("'C\n",""))
    print u'CPU温度：'+str(sumcputemp)+u' ℃'
    return sumcputemp
'''
if __name__ == '__main__':
    print u'CPU温度：'+str(getCpuTemp())+u' ℃'
'''
