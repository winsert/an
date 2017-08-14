#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询CPU温度、空间使用情况的模块

__author__ = 'Andy'

import os

# 查询CPU温度
def getCpuTemp():
    cputemp=os.popen('vcgencmd measure_temp').readline()
    sumcputemp=float(cputemp.replace("temp=","").replace("'C\n",""))
    cpu_msg = u'CPU温度：'+str(sumcputemp)+u' ℃'
    return cpu_msg

# 查询存储空间使用情况
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            dlist = line.split()[1:5]
            disk_msg ="DISK Total Space = "+dlist[0]+"\nDISK Used Space = "+dlist[1]+"\nDISK Used Percent = "+dlist[3]+"\nDISK Avail Space = "+dlist[2]
            return disk_msg

def getIP():
    iplist = []
    p = os.popen("hostname -I")
    line = p.readline().split()
    ip_msg = "LAN IP : "+line[0]+"\nWLAN IP : "+line[1]
    return ip_msg

if __name__ == '__main__':
    print getCpuTemp()
    print getDiskSpace()
    print getIP()
