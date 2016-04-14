#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    活动报名订单跟踪坐标检查
    10分钟一次
'''
import os,json,sys

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')


from lib.Mysql import MySQL

from config.config import *
import urllib2
import xml.etree.ElementTree as ET
class activity2check:



    def __init__(self):

        self._true = False;

        self.mysql = MySQL(dbConfig)
    def run(self):


        self.check()
        return '';

    def check(self):


        for i in range(0, 10):
            if self._true:
                print 'Analysis Total >> Ending!'
                return
            data = self.getList()
            if data == None:
                print 'Data is Null'
                return
            for i in data:
                _data = json.loads(i['data'])

                #_data = phpserialize.unserialize(i['data'], object_hook=phpserialize.phpobject)

                _data['from_address'] = ''
                _data['from_province'] = ''
                _data['from_city'] = ''
                _data['from_district'] = ''
                if i['longitude'] :
                    _address = self.getAddress(i['latitude'], i['longitude']);

                    if _address['status'] == "0":
                        _data['from_address'] = _address['formatted_address']
                        _data['from_province'] = _address['province']
                        _data['from_city'] = _address['city']
                        _data['from_district'] = _address['district']

                _data = json.dumps(_data, ensure_ascii=False)

                #_data = phpserialize.dumps(_data)
                sql = "UPDATE sed_new_activity_member SET `is_check`=1, `data`='%s' WHERE id=%s" % (_data, i['id'])

                self.mysql.insert(sql)
            return


    def getList(self):

        sql = "SELECT * FROM sed_new_activity_member WHERE is_check = 0 LIMIT 100";
        e = self.mysql.query(sql)
        if e == False: return
        list = self.mysql.fetchAllRows()
        if len(list) == 0:self._true = True;
        return list
        #print self.data
    def getAddress(self, x, y):
        str = 'http://api.map.baidu.com/geocoder/v2/?ak=Bmk22qGDPdkzxUG1D3mbtfja&coordtype=wgs84ll&callback=renderReverse&location=%s,%s&output=xml' % (x, y)

        content = urllib2.urlopen(str).read()
        #
        root = ET.fromstring(content)
        _arr = {}
        for neighbor in root.getiterator():
            if (neighbor.tag):_arr[neighbor.tag] = neighbor.text
            #print neighbor.tag ,'->' ,neighbor.text
        return _arr


if __name__ == "__main__":
    _logOp = activity2check()
    _logOp.run()



