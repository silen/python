#!/usr/bin/env python
# -*- coding: utf-8 -*-
u'''

 Redis  消息队列
 silen<silenme@vip.qq.com>
'''

import time
import os,json,sys,time

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')
from lib.Redis import CRedis
class MQ:
    u'''对MySQLdb常用函数进行封装的类'''

    key = 'BabyMQ:' #MySQL错误号码

    def __init__(self):

        self.redis = CRedis()

    def add(self, key, val):
        key = self.key + key;
        self.redis.lpush(key, val)


    def get(self, key):
        key = self.key + key;
        return self.redis.lpop(key)


BabyMQ = MQ()