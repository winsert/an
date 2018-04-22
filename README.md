# 实时查询可转债、外汇等价格信息并进行分析的应用

- adjust.py
用于修改jian, jia, zhong, note, position数据

- an.py
用微信实现：每天执行一次的被动查询的主程序

- ann.py
用微信实现：可长期执行的被动查询的主程序

- qan.py
用QQBot实现：每天执行一次的被动查询的主程序, python qan.py -q 156XXXXXX

- qann.py
用QQBot实现：可长期执行的被动查询的主程序, python qann.py -q 156XXXXXX

- dao.py
用微信itchat实现主动查询的主程序

- qdao.py
用QQBot实现主动查询的主程序, python qdao.py -q 156XXXXXX

- cb.db
SQLite3数据库:cb是可转债表，eb是可交换债表

- ann.py
用微信实现：可长期执行的被动查询的主程序

- cx_cb.py
主动查询可转债,交换债是否满足三线条件的模块

- cxcb.py
被动查询可转债,交换债是否满足三线条件的模块

- cx_cpu.py
主动查询CPU温度的模块

- cx_cx.py
主动查询可转债信息的模块

- cx_ex.py
主动查询可交换债信息的模块

- cxhp.py
被动查询可转债是否满足高价折扣法的模块

- cx_index.py
主动查询证券指数的模块

- cxindex.py
被动查询证券指数的模块

- cx_jrtq.py
主动查询今日天气信息的模块

- cxjj.py
被动查询基金的模块

- cx_pm.py
主动查询PM等数据的模块

- cxqs.py
被动计算转债的强赎天数

- cx_tqsk
主动查询天气实况信息的模块

- cx_wh.py
主动查询外汇的模块

- cxwh.py
被动查询外汇的模块

- cxzg.py
被动查询可转债正股的模块

- jisilu.py
用于从jisilu.cn上爬取新转债的数据，并加入到数据库中。

- exchange.py
用于记录转债的每笔成交记录

- record.py
用于查询转债的每笔成交记录

- xxx.py
临时修改文件
