#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#用于从jisilu.cn上提取cb、eb的相关基础数据

__author__ = 'winsert@163.com'

import requests, random, lxml, urllib2, sqlite3

from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


def get(url): 
    url = url

    agent_list = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

    UA = random.choice(agent_list) #随机选出一个user_agent
    headers = {'User-Agent': UA} #构造一个完整的user-agent

    try:
        request = urllib2.Request(url=url, headers=headers)
        print "request is done !"
        result = urllib2.urlopen(request).read()
        print "result is done !"
        #sf = open('./soup.txt', 'w')
        #print >> sf, result
        #sf.close()
        #result = open('./soup.txt', 'r')
        soup = BeautifulSoup(result, 'lxml').find('div', id="tc_data").find('table', class_='jisilu_tcdata').find_all('td')
        print "soup is done !"
        #result.close()
        return soup
    except Exception, e:
        print u'get(url)时发生错误：'
        print e
        sys.exit()

def record(url):

    url = url
    soup = get(url)

    record = []
    zgjxt = ''
    qzsh = ''
    hs = ''
    ll = ''

    tmp_list = []
    for i in soup: #整理原始数据
        tmp = i.get_text()
        tmp_list.append(filter(None, tmp.split()))
    #print tmp_list

    if tmp_list[0][2][0] == '1': #判断是cb还是eb?
        ce = 'e'
        print u"将要加入数据库的交换债是：", tmp_list[0][2]
    else:
        ce = 'c'
        print u"将要加入数据库的可转债是：", tmp_list[0][2]
    record.append(ce)
    record.append(unicode(tmp_list[0][2])) #转债名称

    alias = raw_input("请设定简称Alias：")
    record.append(alias) #转债简称Alias

    record.append(tmp_list[0][4]) #转债代码
    #record.append(tmp_list[0][5][4:8]) #正股名称
    record.append(tmp_list[0][7][0:6]) #正股代码

    if tmp_list[0][7][0] == '6': #判断是sh,还是sz
        prefix = 'sh'
    else:
        prefix = 'sz'
    record.append(prefix)

    position = 0 #仓位默认为0
    record.append(position)
    HPrice = 130.00 #最高价默认为130.00
    record.append(HPrice)
    LPrice = 111.00 #最低价默认为100.00
    record.append(LPrice)

    jian = float(raw_input("请设定'建仓价'："))
    record.append(jian)
    jia = float(raw_input("请设定'加仓价'："))
    record.append(jia)
    zhong = float(raw_input("请设定'重仓价'："))
    record.append(zhong)
    note = raw_input("请设定'说明Note'：")
    record.append(unicode(note))

    zgdm = '' #转股代码
    record.append(zgdm)
    
    record.append(tmp_list[10][0]) #转股起始日
    record.append(tmp_list[18][0]) #转股价
    record.append(tmp_list[12][0]) #回售起始日

    if tmp_list[20][0] != '-': #判断是否有回售价
        record.append(tmp_list[20][0]) #有回售价
    else:
        record.append(0.0) #无回售价

    record.append(tmp_list[14][0]) #到期日
    record.append(tmp_list[22][0]) #赎回价

    tmp_list[36] #转股价下调
    for i in tmp_list[36]:
        zgjxt = zgjxt + i
    record.append(unicode(zgjxt))
        
    tmp_list[38] #强制赎回
    for i in tmp_list[38]:
        qzsh = qzsh + i
    record.append(unicode(qzsh))

    tmp_list[40] #回售
    for i in tmp_list[40]:
        hs = hs + i
    record.append(unicode(hs))

    tmp_list[42] #利率
    print tmp_list[42]
    if len(tmp_list[42]) == 1:
        ll = '1.0,1.0,1.0,1.0,1.0'
    else:
        for i in range(1,len(tmp_list[42])):
            try:
                #f  = float(tmp_list[42][i][:3])
                ll = ll + tmp_list[42][i][:3] + ','
            except Exception, e:
                continue
        ll = ll[:-1]
    record.append(ll)

    qs = 0 #已强赎天数,默认为0
    record.append(qs)
    qss = 30 #剩余强赎天数,默认为30天
    record.append(qss)

    #print record
    return record

def sql(record): #向数据库insert新记录

    rec = record

    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "insert into cb (ce, Name, Alias, Code, zgcode, Prefix, position, HPrice, LPrice, jian, jia, zhong, Note, zgdm, zgqsr, zgj, hsqsr, hsj, dqr, shj, zgjxt, qzsh, hs, ll, qs, qss) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        curs.execute(sql, rec)
        conn.commit()
        curs.close()
        conn.close()
        print
        print rec[1], u"已加入cb.db数据库。"
    except Exception,e:
        print "SQL_Error is:", e

if __name__ == '__main__':

    url = raw_input('请输入URL地址：')

    rec = record(url)
    print
    print "="*80
    print u"查询结果如下："
    print
    for i in rec:
        print i
    print "="*80

    print
    yn = raw_input('以上查询结果是否要加入cb.db数据库中（y/n）？')
    if yn == 'y':
        sql(rec)
    else:
        sys.exit()
