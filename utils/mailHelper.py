#-*- coding:utf-8 -*-

from email.mime.text import MIMEText
from configReader import configReader
from mcclog import mcclog
import poplib
import smtplib
import re
import chardet
# import sys

# reload(sys)
# sys.getdefaultencoding()

class mailHelper(object):
    CONFIGPATH = '_config.ini'

    def __init__(self):
        self.mcclog = mcclog()
        cfReader = configReader(self.CONFIGPATH)
        self.pophost = cfReader.readConfig('Slave','pophost')
        self.smtphost = cfReader.readConfig('Slave','smtphost')
        self.port = cfReader.readConfig('Slave','port')
        self.username = cfReader.readConfig('Slave','username')
        self.password = cfReader.readConfig('Slave','password')
        self.bossMail = cfReader.readConfig('Boss','mail')
        self.loginMail()
        self.configSlaveMail()

    def loginMail(self):
        self.mcclog.mccWriteLog(u'开始登陆邮箱')
        try:
            self.pp = poplib.POP3_SSL(self.pophost)
            # print self.pophost
            self.pp.set_debuglevel(0)
            self.pp.user(self.username)
            self.pp.pass_(self.password)
            self.pp.list()
            print u'登陆成功！'
            self.mcclog.mccWriteLog(u'登陆邮箱成功')
        except Exception,e:
            print u'登陆失败'
            self.mcclog.mccError(u'登陆邮箱失败'+str(e))
            exit()

    def acceptMail(self):
        self.mcclog.mccWriteLog(u'开始抓住邮件内容。')
        try:
            ret = self.pp.list()
            # print 'OK'
            mailBody = self.pp.retr(len(ret[1]))
            print 'OK'
            self.mcclog.mccWriteLog(u'抓取邮件成功')
            return mailBody
        except Exception,e:
            self.mcclog.mccError(u'抓取邮件失败'+str(e))
            return None

    def analysisMail(self,mailBody):
        self.mcclog.mccWriteLog(u'开始分析获取subject和发件人')
        try:
            subject = re.search("'Subject: (.*?)'",str(mailBody[1]),re.S).groups(0)
            # subj = subject
            # print type(subj)
            # print subj[0]
            sender = re.search("'From: .* <(.*?)>'",str(mailBody[1]),re.S).groups(0)
            print sender
            command = {'subject':subject[0],'sender':sender[0]}
            self.mcclog.mccWriteLog(u'分析获取subject和发件人成功')
            return command
        except Exception,e:
            self.mcclog.mccError(u'分析获取subject和发件人失败'+str(e))
            return None

    def configSlaveMail(self):
        self.mcclog.mccWriteLog(u'开始配置发件箱')
        try:
            self.handle = smtplib.SMTP(self.smtphost,self.port)
            self.handle.login(self.username,self.password)
            self.mcclog.mccWriteLog(u'发件箱配置成功')
        except Exception,e:
            self.mcclog.mccError(u'发件箱配置失败'+str(e))
            exit()

    def sendMail(self,subject,receiver,bodycon="aaaaa"):
        msg = MIMEText(bodycon,'plain','utf-8')
        msg['Subject'] = subject
        msg['from'] = self.username
        self.mcclog.mccWriteLog(u'开始发送邮件'+'to'+receiver)
        if receiver == 'Slave':
            try:
                self.handle.sendmail(self.username,self.username,msg.as_string())
                self.mcclog.mccWriteLog(u'发送邮件成功')
                return True
            except Exception,e:
                self.mcclog.mccError(u'发送邮件失败'+str(e))
                return False

        elif receiver == 'Boss':
            try:
                self.handle.sendmail(self.username,self.bossMail,msg.as_string())
                self.mcclog.mccWriteLog(u'发送邮件成功')
            except Exception,e:
                self.mcclog.mccError(u'发送邮件失败'+str(e))
                return False

if __name__ == '__main__':
    mail = mailHelper()
    body = mail.acceptMail()
    print body
    print mail.analysisMail(body)
    # mail.sendMail('aaa','Boss')

