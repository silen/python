#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    活动报名订单是否有过期
    一分钟一次
'''
import os,json,sys,time

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')


from lib.Redis import CRedis
from lib.Mysql import MySQL
from wechatpy import WeChatClient
from lib.MQ import BabyMQ
from config.config import *
class SendMess:

    def __init__(self):

        self._true = False;
        self._time = int(time.time()) - 3*60*60
        self.mysql = MySQL(dbConfig)
        self.WeChatClient = WeChatClient(wechatConfig['appid'], wechatConfig['secret'])

    def run(self):
        return
        for i in range(0, 100):

            content = BabyMQ.get("WechatMessage")
            #BabyMQ.add("WechatMessage", content)
            if content:
                a = []
                content = json.loads(content)

                Message = {
                    'url' :content['url'],
                    'description' :content['content'],
                    'title' :content['title']
                }
                a.append(Message)
                try:
                    self.WeChatClient.message.send_articles(content['openid'], a)
                except:
                    content['isExcept'] = 1;
                    BabyMQ.add("WechatMessage", json.dumps(content))
                    return
            return

if __name__ == "__main__":
    _logOp = SendMess()
    _logOp.run()

'''
self._post(
            'message/custom/send',
            data=data
        )
'''


