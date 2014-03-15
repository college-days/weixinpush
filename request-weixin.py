#-* coding:utf-8 -*-

import requests
import json
import re
import time
import os
#from pyquery import PyQuery as pq
#from BeautifulSoup import BeautifulSoup
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
#from PyQt4.QtWebKit import *
import sys   
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
sys.setdefaultencoding('utf-8') 

cookiePath = './login_cookie'
usercopyPath = './usercopy'
usercountPath = './usercount'
sendmsgErrlogPath = './errorlog'

class User:
    """docstring for User"""
    def __init__(self, userid, nickname, remarkname='', groupid=-1):
        self.userid = userid
        self.nickname = nickname
        self.remarkname = remarkname
        self.groupid = groupid

class WeixinPublic:
    """docstring for WeixinPublic"""
    def __init__(self):
        self.session = requests.Session()
        self.loginUrl = 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'
        self.singlePushUrl = 'https://mp.weixin.qq.com/cgi-bin/singlesend'
        self.token = ''
        self.pageCount = 0
        self.userCount = 0
        self.userList = []

    def login(self):
        """docstring for login"""

        loginParams = {
            'username': '',
            'pwd': '',
            'imgcode': '',
            'f': 'json'
        }

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '72',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'mp.weixin.qq.com',
            'Origin': 'https://mp.weixin.qq.com',
            'Referer': 'https://mp.weixin.qq.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = self.session.post(self.loginUrl, loginParams, headers=headers)
        content = response.json()
        token = content['ErrMsg'].split('=')[-1]
        self.token = token
        print self.token
    
    def singlePushMsg(self, msg, userID):
        """docstring for pushSingleMsg"""
        pushMsgParams= {
            'type': '1',
            'content': msg,
            'tofakeid': userID,
            'imgcode': '',
            'token': self.token,
            'lang': 'zh_CN',
            'random': '0.7429829628672451',
            'f': 'json',
            'ajax': '1',
            't': 'ajax-response'
        }
    
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01', 
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '131',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'mp.weixin.qq.com',
            'Origin': 'https://mp.weixin.qq.com',
            'Referer': 'https://mp.weixin.qq.com/cgi-bin/singlesendpage?t=message/send&action=index&tofakeid=1835682900&token=1168938150&lang=zh_CN',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        response = self.session.post(self.singlePushUrl, data=pushMsgParams, headers=headers)
        content = response.json()
        errMsg = content['base_resp']['err_msg']
        if errMsg == "ok":
            print 'send successful'
        elif errMsg == "customer block":
            print '需要等待用户回复'
            file = open(sendmsgErrlogPath, 'a')
            file.write('block error\n')
            file.close()
        else:
            print 'something is wrong'
            file = open(sendmsgErrlogPath, 'a')
            file.write('other error\n')
            file.close()
    
    def getUserCount(self):
        """docstring for getuserCount"""
        values = {
            't': 'user/index',
            'pagesize': 10,
            'pageidx': 0,
            'type': 0,
            'token': self.token,
            'lang': 'zh_CN'
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'mp.weixin.qq.com',
            'Referer': 'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=%s' % (self.token),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36'
        }

        userManageUrl = 'https://mp.weixin.qq.com/cgi-bin/contactmanage?t=%s&pagesize=%d&pageidx=%d&type=%d&token=%s&lang=%s' % (values['t'], values['pagesize'], values['pageidx'], values['type'], values['token'], values['lang'])
        
        response = self.session.get(userManageUrl, headers=headers)
        result = response.text
        totalUserCount = re.findall(r"totalCount : '(.*?)' \* 1", result)
        #print int(totalUserCount[0])
        self.userCount = int(totalUserCount[0])
        print self.userCount
        file = open('./usercount', 'w')
        file.write("%d" % self.userCount)
        file.close()

    def getAllUserList(self):
        """docstring for getAllUserList"""
        values = {
            't': 'user/index',
            'pagesize': 10,
            'pageidx': 0,
            'type': 0,
            'token': self.token,
            'lang': 'zh_CN'
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'mp.weixin.qq.com',
            'Referer': 'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=%s' % (self.token),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36'
        }

        userManageUrl = 'https://mp.weixin.qq.com/cgi-bin/contactmanage?t=%s&pagesize=%d&pageidx=%d&type=%d&token=%s&lang=%s' % (values['t'], values['pagesize'], values['pageidx'], values['type'], values['token'], values['lang'])
        
        response = self.session.get(userManageUrl, headers=headers)
        result = response.text
        pageNum = re.findall(r'pageCount : (.*?),', result)
        userList = re.findall(r'friendsList : \({"contacts":\[(.*?)\]}\).contacts,', result)
        print int(pageNum[0])
        self.pageCount = int(pageNum[0])
        newUserList = re.findall(r'\{(.*?)\}', userList[0])
        for user in newUserList:
            userDetailList = user.split(',')
            newUserDetailList = []
            for detail in userDetailList:
                newUserDetailList.append(detail.split(':')[-1])
            print newUserDetailList
            self.userList.append(User(newUserDetailList[0], newUserDetailList[1], newUserDetailList[2], newUserDetailList[3]))

        for i in xrange(1, self.pageCount):
            time.sleep(3)
            self.getUserFromSinglePage(i, headers)
            time.sleep(3)
    
    def getUserFromSinglePage(self, pageidx, headers):
        """docstring for getUserFromSinglePage"""
        values = {
            't': 'user/index',
            'pagesize': 10,
            'pageidx': pageidx,
            'type': 0,
            'token': self.token,
            'lang': 'zh_CN'
        }

        userManageUrl = 'https://mp.weixin.qq.com/cgi-bin/contactmanage?t=%s&pagesize=%d&pageidx=%d&type=%d&token=%s&lang=%s' % (values['t'], values['pagesize'], values['pageidx'], values['type'], values['token'], values['lang'])
        print userManageUrl

        response = self.session.get(userManageUrl, headers=headers)
        result = response.text
        userList = re.findall(r'friendsList : \({"contacts":\[(.*?)\]}\).contacts,', result)
        newUserList = re.findall(r'\{(.*?)\}', userList[0])
        for user in newUserList:
            userDetailList = user.split(',')
            newUserDetailList = []
            for detail in userDetailList:
                newUserDetailList.append(detail.split(':')[-1])
            print newUserDetailList
            self.userList.append(User(newUserDetailList[0], newUserDetailList[1], newUserDetailList[2], newUserDetailList[3]))


    def echoAllUser(self):
        """docstring for echoAllUser"""
        
        file = open('./usercopy', 'w')
        for user in self.userList:
            print "id: %d, name: %s" % (int(user.userid), user.nickname)
            file.write("id:%d, name:%s\n" % (int(user.userid), user.nickname))
        file.close()

        print "has %d users" % int(len(self.userList))
    
    def pushMsgToAll(self, msg):
        """docstring for pushMsgToAll"""
        for user in self.userList:
            time.sleep(1)
            self.singlePushMsg(msg, int(user.userid))
            time.sleep(1)

if __name__ == '__main__':
    while True:
        weixin = WeixinPublic()
        if os.path.exists(usercountPath):
            file = open(usercountPath, 'r')
            oldUserCount = int(file.readline())
            file.close()
        else:
            print 'no oldUserCount exists'
        
        if os.path.exists(usercopyPath):
            file = open(usercopyPath, 'r')
            for line in file.readlines():
                userDetails = line[:-1].split(', ')
                userInfos = []
                for detail in userDetails:
                    userInfos.append(detail.split(':')[-1])
                weixin.userList.append(User(userInfos[0], userInfos[1]))
            file.close()
        else:
            print 'no oldUserList exists'

        weixin.login()
        weixin.getUserCount()
        if weixin.userCount != oldUserCount or weixin.userList == []:
            weixin.getAllUserList()
            weixin.echoAllUser()        
            print 'should refresh userlist!'
        else:
            weixin.echoAllUser()
            print 'userlist is not changed'
        
        time.sleep(3)
        weixin.singlePushMsg('3', 1835682900)
        time.sleep(3)
        weixin.singlePushMsg('3', 1534621360)
        #weixin.pushMsgToAll('大家新年快乐!')

