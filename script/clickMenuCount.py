#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    统计菜单点击  推广用户计算
    一分钟一次
'''
import os,json,sys,time

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')


from lib.Mysql import MySQL
from lib.Redis import CRedis
from config.config import *
class clickMenuCount:



    def __init__(self):

        self._true = False;
        self._time = int(time.time()) - 24*60*60
        self.redis = CRedis()
        self.redisKey = 'log:Oday';
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
        opendid = []
        for i in data:
            _data = json.loads(i)
            opendid.append(_data['FromUserName'])

        openids = list(set(opendid))
        m = self.checkMember(openids)
        if len(m) == 0:
            print 'Not in new_qcode_count'
            return
        print m

        return
    def checkMember(self, openids):
        id = ','.join(openids)
        sql = "SELECT openid,qcode_id FROM sed_new_qcode_count WHERE openid in ('%s')" % id;
        self.mysql.query(sql)
        v = self.mysql.fetchAllRows()
        r = {}
        if v == None:return r
        for i in v:
            r[v['openid']] = v['id']
        return r
    def get(self):
        e = []
        for i in range(0, 1):
            x = self.redis.lpop(self.redisKey)
            self.redis.lpush(self.redisKey,  x)
            if x == None:
                return e
            else:
                e.append(x)

        return e


if __name__ == "__main__":
    _logOp = clickMenuCount()
    _logOp.run()



