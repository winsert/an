#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询可转债、可交换债的最新价是否满足三线条件的模块

__author__ = 'winsert@163.com'

import sqlite3, urllib2

# 用于解析URL页面
def bsObjForm(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read().decode('gbk','ignore')
    return html

# 用于查询指定证券的价格
def getZZ(zzCode):
    key = zzCode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp_list = resp.split(',')
        zz_price = float(tmp_list[3]) #获取正股实时价格
        return zz_price
    except:
        zz_price = 0 
        return zz_price

# 从cb.db数据库中提取可转债数据进行实时三线分析
def getCB():

    msg = []
    zz_msg = ''
    
    conn = sqlite3.connect('cb.db')
    curs = conn.cursor()
    sql = "select name, Code, zgcode, Prefix, position, jian, jia, zhong, zgj from cb" 
    curs.execute(sql)
    tmp = curs.fetchall()
    curs.close()
    conn.close()

    for cc in tmp:
        prefix = cc[3]

        if prefix != 'QS' :  #QS代表已强赎

            zzcode = cc[3]+cc[1] #前缀+转债代码
            position = cc[4] #仓位
            jian = float(cc[5]) #建仓价
            jia = float(cc[6])  #加仓价
            zhong = float(cc[7]) #重仓价
            zz = float(getZZ(zzcode)) #查询转债价格

            if zz <= jian and zz > jia and position < 600: #满足建仓条件
                zz_msg = cc[0]+u': '+str(position)+u'张'+u'\n最新价:'+str(zz)+u'  建仓价:'+str(jian)
                msg.append(zz_msg)
            elif zz <= jia and zz > zhong and position < 900: #满足加仓条件
                zz_msg = cc[0]+u': '+str(position)+u'张'+u'\n最新价:'+str(zz)+u'  加仓价:'+str(jia)
                msg.append(zz_msg)
            elif zz <= zhong and zz > 0: #满足重仓条件
                zz_msg = cc[0]+u': '+str(position)+u'张'+u'\n最新价:'+str(zz)+u'  重仓价:'+str(zhong)
                msg.append(zz_msg)

            #print zz_msg

    #print msg
    return msg

'''
if __name__ == '__main__':

    msglist = getCB()
    if len(msglist) == 0:
        print u"没有满足条件的CB"
    else:    
        for msg in msglist:
        print msg
        print
'''
