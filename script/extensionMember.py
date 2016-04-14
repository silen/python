#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    会员的关注下级会员统计

'''
import os,json,sys

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')

from lib.Redis import CRedis
from lib.Mysql import MySQL
from config.config import *

class extensionMember:

    def __init__(self):
        self.redis = CRedis()
        self.redisKey = 'member:extension';

        self.mysql = MySQL(dbConfig)
    def run(self):


        self.insert()
        return '';

    def insert(self):

        for i in range(0, 50):
            val = self.redis.lpop(self.redisKey);
            if val == None:return
            #self.redis.lpush(self.redisKey, val);
            val = json.loads(val)
            upsystemid = val['upsystemid']
            systemid = val['systemid']
            level = {'level1':0, 'level2':0, 'level3':0, 'level4':0, 'level5':0, 'level6':0,'level7':0,'level8':0,'level9':0,'level10':0,}
            self.data = {}
            self.DxMember(upsystemid, 1)
            if len(self.data) > 0:
                sql = "";
                for i in self.data:
                    key = 'level'+str(i)
                    level[key] = self.data[i]
                sql = "UPDATE sed_new_member_relation SET `level_1`=%s, `level_2`=%s, `level_3`=%s, `level_4`=%s, `level_5`=%s, `level_6`=%s, `level_7`=%s, `level_8`=%s, `level_9`=%s, `level_10`=%s WHERE userid=%s" % (level['level1'], level['level2'], level['level3'], level['level4'], level['level5'], level['level6'], level['level7'], level['level8'], level['level9'], level['level10'], upsystemid)

                print self.mysql.insert(sql)

    def DxMember(self, upid, l):
        if (l + 1) == 10:return ''
        upsystemidCount, ids = self.countMember(upid)
        if self.data.has_key(l) == False:self.data[l] = 0
        self.data[l] = self.data[l] + upsystemidCount
        if upsystemidCount > 0:
            for i in ids:
                self.DxMember(i, l+1)

    def countMember(self, id):
        key = self.redisKey + '_' + str(id)
        return self.redis.hlen(key), self.redis.hkeys(key)


if __name__ == "__main__":
    _logOp = extensionMember()
    _logOp.run()



