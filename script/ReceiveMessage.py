#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    获取客服消息
'''
import os,json,sys,time,datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')


from lib.Redis import CRedis
from lib.Mysql import MySQL
from wechatpy import WeChatClient
from config.config import *
class ReceiveMessage:

    def __init__(self):

        self._true = False;
        self._time = int(time.time()) - 6*24*60*60
        self.mysql = MySQL(dbConfig)
        self.WeChatClient = WeChatClient(wechatConfig['appid'], wechatConfig['secret'])

    def run(self):
        t_str = '2016-03-18'

        sDate = int(time.mktime(time.strptime(t_str,"%Y-%m-%d")))
        eDate = sDate + 5*24*3600
        for i in range(1, 100):
            print i
            #print time.strftime('%Y-%m-%d %H:%M:%S', self._time)
            print time.strftime('%Y-%m-%d %H:%M:%S', time.time())
            x = self.WeChatClient.customservice.get_records(self._time, int(time.time()), 1, 10)
            print x
            if x:
                print x
            else:
                return

if __name__ == "__main__":
    _logOp = ReceiveMessage()
    _logOp.run()




