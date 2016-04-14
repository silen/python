#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    分享点击统计
    五分钟一次
'''
import os,json,sys,time,hashlib
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')


from lib.Mysql import MySQL
from lib.Redis import CRedis
from config.config import *

class ShareCount:



    def __init__(self):

        self._true = False;
        self._time = int(time.time()) - 24*60*60
        self.redis = CRedis()
        self.redisKey = 'log:share';
        self.mysql = MySQL(dbConfig)

    def run(self):

        print 'Is now time -> ' , time.strftime('%Y-%m-%d %H:%I:%S',time.localtime(time.time()))
        print 'Out of time -> ' , time.strftime('%Y-%m-%d %H:%I:%S',time.localtime(self._time))
        self.check()
        return '';

    def check(self):

        data = self.get()
        if len(data) == 0:
            print 'Data is Null'
            return

        sql = []
        for i in data:
            _data = json.loads(i)
            type = _data['type']
            url = _data['url']
            if url:
                m = hashlib.md5()
                m.update(url)
                md5url = m.hexdigest()
                insertSql = "INSERT INTO sed_new_share_click (`url`, `md5url`, `type`) VALUES ('%s', '%s', '%s');" %(url, md5url, type);
                self.mysql.insert(insertSql)

    def get(self):
        e = []
        for i in range(0, 400):
            x = self.redis.lpop(self.redisKey)
            if x == None:
                return e
            else:
                e.append(x)

        return e


if __name__ == "__main__":
    _logOp = ShareCount()
    _logOp.run()



