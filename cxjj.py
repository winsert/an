#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询基金的模块

__author__ = 'winsert@163.com'

import urllib2

# 用于解析URL页面
def bsObjForm(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read().decode('gbk','ignore')
    return html

# 用于查询基金的价格
def getJJ():

    jj_dict = {'sh505888':1.00,} #预警价
    #jj_dict = {'sh505888':1.00, 'sz150016':1.00} #预警价
    jj_list = []
    jj_msg = ''

    try:
        for key in jj_dict:
            value = jj_dict[key]
            #print key
            #print jj_dict[key]
            url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
            resp = bsObjForm(url)
            tmp_list = resp.split(',')
            #print tmp_list
            jj_name = tmp_list[0][-4:] #基金名称
            new_price = float(tmp_list[1]) #获取基金最新价格
            zr_price = float(tmp_list[3]) #获取基金昨日价格
            #zdf = round((new_price/zr_price - 1)*100, 3) #计算涨跌
            if new_price < value:
                jj_msg = jj_name+u' 最新价:'+str(new_price)+' < '+str(value)
                #print jj_msg
                jj_list.append(jj_msg)

        return jj_list

    except Exception, e:
        print 'getWH ERROR :', e
        jj_list.append(e)
        return jj_list

if __name__ == '__main__':

    msg_list = getJJ()
    if len(msg_list) == 0 :
        print 'Everthing is OK !'
    else:
        for msg in msg_list:
            print msg
