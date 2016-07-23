#-*-coding:utf-8-*-

from mcclog import mcclog
from mailHelper import mailHelper
# import sys
import os
import win32api

class executor(object):
    def __init__(self,commandDict,openDict):
        self.mcclog = mcclog()
        self.mailHelper = mailHelper()
        self.commandDict = commandDict
        self.openDict = openDict

    def execute(self,exe):
        subject = exe['subject']
        self.mcclog.mccWriteLog(u'开始处理命令...')
        self.mailHelper.sendMail('pass','Boss','邮件接收分析ok，开始处理命令')
        if subject in self.commandDict:
            self.mcclog.mccWriteLog(u'执行命令')
            try:
                command = self.commandDict[subject]
                os.system(command)
                self.mailHelper.sendMail('Success','Boss')
                self.mcclog.mccWriteLog(u'执行命令成功')
            except Exception,e:
                self.mcclog.mccError(u'执行命令失败'+str(e))
                self.mailHelper.sendMail('error','Boss',e)
        elif subject in self.openDict:
            self.mcclog.mccWriteLog(u'打开文件')
            try:
                openFile = self.openDict[subject]
                win32api.ShellExecute(0,'open',openFile,'','',1)
                self.mailHelper.sendMail('Success','Boss','恭喜您，成功执行命令')
                self.mcclog.mccWriteLog(u'打开文件成功')
            except Exception,e:
                self.mcclog.mccError(u'打开文件失败，'+str(e))
                self.mailHelper.sendMail('error','Boss',e)
        else:
            self.mailHelper.sendMail('error','Boss','no such command')
