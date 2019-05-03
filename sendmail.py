#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 自动获取可转债、可交换债的最新价进行"三线"和"高价折扣法"分析

__author__ = 'winsert@163.com'

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

# SMTP 服务
mail_host="smtp.qq.com"  #设置服务器
mail_post=25
mail_passwd="usizkavruxkljhci"   #这个是发送QQ账号的授权码，而不是QQ账号的密码，否则发送会失败    
sender = '1569701115@qq.com'
receivers = ['13395317077@189.cn']  # 接收邮件的邮箱

def sendMail(msg):

    message = MIMEText('End', 'plain', 'utf-8')
    message['From'] = Header("三线提醒", 'utf-8')
    message['To'] =  Header("测试", 'utf-8')
      
    subject = msg
    message['Subject'] = Header(subject, 'utf-8')
        
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(sender, mail_passwd)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"


if __name__ == '__main__':
    
    msg = u'莫听穿林打叶声，何妨吟啸且徐行'
    sendMail(msg)