#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 查询股票的模块

__author__ = 'winsert@163.com'

import urllib2

# 用于解析URL页面
def bsObjForm(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read().decode('gbk','ignore')
    return html

# 用于查询stock的价格
def getStock():

    st_dict = {'hk02680':1.4} #预警价
    #st_dict = {'sh505888':1.00, 'sz150016':1.00} #预警价
    st_list = []

    try:
        for key in st_dict:
            value = st_dict[key]
            #print key
            #print st_dict[key]
            url = "http://hq.sinajs.cn/list="+key #生成用于查询的URL
            resp = bsObjForm(url)
            tmp_list = resp.split(',')
            #print tmp_list
            st_msg = ''

            if len(tmp_list) > 3: #判断是否停牌
                kl = list(key)
                if kl[0] == 'h':
                    st_name = tmp_list[1][-4:] #stock名称
                    new_price = float(tmp_list[6]) #获取stock最新价格
                else:
                    st_name = tmp_list[0][-4:] #stock名称
                    new_price = float(tmp_list[3]) #获取stock最新价格
                #print st_name, new_price
                if new_price > value:
                #if new_price < value:
                    #st_msg = st_name+u' 最新价:'+str(new_price)+' < '+str(value)
                    st_msg = st_name+u' 最新价:'+str(new_price)+' > '+str(value)
                    #print st_msg
                    st_list.append(st_msg)

        #print st_list
        return st_list

    except Exception, e:
        print 'getStock ERROR :', e
        st_list.append(e)
        return st_list

if __name__ == '__main__':

    msg_list = getStock()
    if len(msg_list) == 0 :
        print 'Everthing is OK !'
    else:
        for msg in msg_list:
            print msg
