#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    活动坐标更新

'''
import os, json, sys
from math import radians, cos, sin, asin, sqrt
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

from lib.Redis import CRedis
from lib.Mysql import MySQL
from config.config import *
import urllib2, xml
import xml.etree.ElementTree as ET


class activity2member:
    def __init__(self):

        self.redis = CRedis()
        self.redisKey = 'member:sight';
        self.data = []
        self.mysql = MySQL(dbConfig)

    def run(self):

        self.insert()
        return '';

    def insert(self):
        data = self.getRedisList()

        if (len(data) == 0):
            print '啦啦啦 ---> 没有数据'
            return ''
        sql = []

        for k in data:
            print k['id']
            address = province = city = district = ''
            distance = upsystemid = 0

            _address = self.getAddress(k['latitude'], k['longitude']);

            if _address and _address['status'] == "0":
                address = _address['formatted_address']
                province = _address['province']
                city = _address['city']
                district = _address['district']
            else:
                continue;
            s1 = "SELECT * FROM sed_new_qcode WHERE id='%s'" % k['qcode_id']
            self.mysql.query(s1)

            Qcode = self.mysql.fetchOneRow()
            if Qcode != None:
                longitudeA = float(Qcode['longitude'])
                latitudeA = float(Qcode['latitude'])
                longitudeB = float(_address['lng'])
                latitudeB = float(_address['lat'])
                distance = int(haversine(longitudeA, latitudeA, longitudeB, latitudeB))

            sql ="UPDATE sed_new_qcode_count SET `province`='%s', `city`='%s', `district`='%s', `address`='%s', `distance`='%s' WHERE id=%s" %(province, city, district, address, distance, k['id'])
            self.mysql.query(sql)
        print 'lalal';
    def getRedisList(self):
        sql = "SELECT * FROM sed_new_qcode_count WHERE longitude != '' AND province=''";
        e = self.mysql.query(sql)
        if e == False: return []
        list = self.mysql.fetchAllRows()
        if len(list) == 0:self._true1 = True;
        return list
        # print self.data

    def getAddress(self, x, y):
        '''http://api.map.baidu.com/geocoder/v2/?ak=Bmk22qGDPdkzxUG1D3mbtfja&coordtype=$type&callback=renderReverse&location=$latitude,$longitude&output=json&pois=0'''

        str = 'http://api.map.baidu.com/geocoder/v2/?ak=Bmk22qGDPdkzxUG1D3mbtfja&coordtype=wgs84ll&callback=renderReverse&location=%s,%s&output=xml' % (
            x, y)
        content = urllib2.urlopen(str).read()
        #
        root = ET.fromstring(content)
        _arr = {}
        for neighbor in root.getiterator():
            if (neighbor.tag): _arr[neighbor.tag] = neighbor.text
            # print neighbor.tag ,'->' ,neighbor.text
        return _arr




def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000

if __name__ == "__main__":
    _logOp = activity2member()
    _logOp.run()
