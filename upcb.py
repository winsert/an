#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 本程序用于修改转债数据
__author__ = 'winsert@163.com'

import sqlite3
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# 查询指定转债的数据
def getcb(alias):
    cbdict = {}
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        #sql = "select name, code, zzcode, jian, jia, zhong, note, position, AVG, zgj, ll, HPrice, LPrice, aqd, pj, tmp from cb where Alias = '%s'" %alias
        sql = "select * from cb where Alias = '%s'" %alias
        curs.execute(sql)
        tmp = curs.fetchall()
        curs.close()
        conn.close()

        print
        name = tmp[0][3] #转债名称
        print u'名  称：', name
        #cbdict['名  称：'] = ['name', name]

        code = tmp[0][2] #特征码
        print u'特征码：', code
        cbdict['特征码：'] = ['code', code]

        position = tmp[0][8] #持仓
        print u'持  仓：', position
        cbdict['持  仓：'] = ['position', position]

        avg = tmp[0][9] #平均成本价
        print u'平均价：', avg
        cbdict['平均价：'] = ['avg', avg]

        hprice = tmp[0][10] #新高价
        print u'新高价：', hprice
        cbdict['新高价：'] = ['hprice', hprice]

        lprice = tmp[0][11] #新低价
        print u'新低价：', lprice
        cbdict['新低价：'] = ['lprice', lprice]

        jian = tmp[0][12] #建仓价
        print u'建仓价：', jian
        cbdict['建仓价：'] = ['jian', jian]

        jia = tmp[0][13] #加仓价
        print u'加仓价：', jia
        cbdict['加仓价：'] = ['jia', jia]

        zhong = tmp[0][14] #重仓价
        print u'重仓价：', zhong
        cbdict['重仓价：'] = ['zhong', zhong]

        note = tmp[0][15] #说明
        print u'说  明：', note
        cbdict['说  明：'] = ['note', note]
        
        zgj = tmp[0][17] #转股价
        print u'转股价：', zgj
        cbdict['转股价：'] = ['zgj', zgj]

        ll = tmp[0][24] #利率
        print u'利  率：', ll
        cbdict['利  率：'] = ['ll', ll]

        qs = tmp[0][25] #已强赎天数
        print u'强赎天：', qs
        cbdict['强赎天：'] = ['qs', qs]

        qss = tmp[0][26] #剩余天数
        print u'剩余天：', qss
        cbdict['剩余天：'] = ['qss', qss]

        aqd = tmp[0][28] #安全度
        print u'安全度：', aqd
        cbdict['安全度：'] = ['aqd', aqd]

        pj = tmp[0][30] #评级
        print u'评  级：', pj
        cbdict['评  级：'] = ['pj', pj]

        tmp = tmp[0][31] #涨跌幅
        print u'涨跌幅：', tmp
        cbdict['涨跌幅：'] = ['tmp', tmp]
        print

        return cbdict

    except Exception, e :
        print 'getcb() Error:', e
        sys.exit()

#update
def UpDate(alias, k, kk, v):
    #print alias, k, kk, v
    #sql = "UPDATE cb SET " + kk +"= ? WHERE Alias = ?"
    #print sql
    
    try:
        conn = sqlite3.connect('cb.db')
        curs = conn.cursor()
        sql = "UPDATE cb SET " + kk +"= ? WHERE Alias = ?"
        curs.execute(sql, (v, alias))
        conn.commit()
        curs.close()
        conn.close()

        print "  " + k + u"已修改为 ", v

    except Exception, e:
        print 'UpDate() ERROR :', e
        sys.exit()


if  __name__ == '__main__': 

    msg = u"""
    本程序用于修改：
    - 名  称 Name
    - 特征码 code
    - 建仓价 jian
    - 加仓价 jia
    - 重仓价 zhong
    - 说  明 note
    - 新高价 HPrice
    - 新低价 LPrice
    - 持  仓 position
    - 平均价 avg
    - 转股价 zgj
    - 利  率 ll
    - 新低价 Lprice
    - 新高价 Hprice
    ......
    """
    print
    print msg
    alias = raw_input(u'输入可转债的简称缩写：')
    #cblist = getcb(alias)
    cbdict = getcb(alias)
    yn = raw_input(u'是否要修改(y/n)？')
    if yn == 'n':
        sys.exit()

    for k, v in cbdict.items():
        print u"\n原" + k, v[1]
        msg = u"新" + k
        v[1] = unicode(raw_input(msg))
        if v[1] != '':
            UpDate(alias, k, v[0], v[1])
        else:
            print "  " + k + u" 没有修改！"
    
    print u'\n全部修改结果如下：'
    getcb(alias)