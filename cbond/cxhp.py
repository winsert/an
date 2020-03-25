#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 自动获取可转债、可交换债的最新价是否满足高价折扣法的模块

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
        zz_price = float(tmp_list[3]) #获取证券实时价格
        #print zzCode+u' 当前价：'+str(zz_price)+'\n'
        return zz_price
    except:
        zz_price = 0
        print "getZZ() is error !"
        return zz_price

# 用于计算正股涨跌幅和溢价率
def getZG(zgcode, zz, zgj):
    key = zgcode
    url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
    try:
        resp = bsObjForm(url)
        tmp_list = resp.split(',')
        zs_price = float(tmp_list[2]) #获取正股昨收价格
        zg_price = float(tmp_list[3]) #获取正股实时价格
        zdf = round((zg_price/zs_price - 1) * 100, 2) #涨跌幅
        yjl = round((zz/(100/zgj*zg_price) - 1) * 100, 2) #溢价率
        return zdf, yjl
    except:
        zdf = 1.0
        yjl = 1.0
        print "getZG() is error !"
        return zdf, yjl

#对cb.db中HPrice的值进行修改
def getSQLite(code, newHP):
    cc = code
    hp = float(newHP)

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "UPDATE cb SET HPrice = %r WHERE Code = %s" % (hp, cc) 
        curs.execute(sql)
        conn.commit()
        curs.close()
        conn.close()

    except Exception, e1:
        print 'getSQLite ERROR :',e1

#从cb.db数据库中提取可转债数据进行"高价折扣法"分析
def getHP():
    hpMsg = []
    hpmsg = ''
    
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "select name, Code, Prefix, position, HPrice, zgcode, zgj from cb" 
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

        for cc in tmp:
            name = cc[0] #转债名称
            code = cc[1] #转债代码
            zzcode = cc[2]+cc[1] #前缀+转债代码
            position = float(cc[3]) #仓位
            hp = float(cc[4]) #原最高价
            zgcode = cc[2]+cc[5] #前缀+正股代码
            zgj = cc[6] #转股价

            if position > 0:
                zz = float(getZZ(zzcode)) #查询转债价格
                #print name+u' 原最高价：'+str(hp)+u'  当前价：'+str(zz)+'\n'

                #if zz > hp + 1.0: #比原最高价高1.0元
                if zz > hp * 1.01: #比原最高价高1%
                    getSQLite(code, zz)
                    zdf, yjl = getZG(zgcode, zz, zgj)
                    #hpmsg = cc[0]+u': '+str(position)+u'张'+u'\n最新价:'+str(zz)+u' >前高价:'+str(hp)
                    #hpmsg = cc[0]+u': '+str(zz)+u' >前高价:'+str(hp)
                    hpmsg = cc[0]+u':'+str(zz)+u'>前高价'+str(hp)+u'\n正股:'+str(zdf)+'%'+u'，溢价率'+str(yjl)+'%'
                    hpMsg.append(hpmsg)

                elif hp > 130.0 and zz < 130.0:
                    getSQLite(code, 130.00)
                    #hpmsg = cc[0]+u': '+str(position)+u'张'+u'\n最新价:'+str(zz)+u',< 130元。'
                    hpmsg = cc[0]+u':'+str(zz)+u' < 130元！'
                    hpMsg.append(hpmsg)

                elif hp >= 130.0 and zz <= (hp-9) and zz > 130.0:
                    getSQLite(code, zz)
                    #hpmsg = cc[0]+u': '+str(position)+u'张'+u'\n最新价:'+str(zz)+u'\n自最高价下跌超过9元。'
                    hpmsg = cc[0]+u':'+str(zz)+u'，自最高价下跌超过9元。'
                    hpMsg.append(hpmsg)

    except Exception,e2:
        print 'getHP ERROR :',e2

    #print hpMsg
    return hpMsg

if __name__ == '__main__':
    
    HPlist = getHP()
    if len(HPlist) == 0:
        print u'一切正常！'
        print
    else:
        for hpMsg in HPlist:
            print hpMsg
            print