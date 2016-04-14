#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    活动报名订单是否有过期
    一分钟一次
'''
import os,json,sys,time

sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../')


from lib.Mysql import MySQL
from lib.MQ import BabyMQ
from config.config import *
import phpserialize
class activity2order:



    def __init__(self):

        self._true = False;
        self._true1 = False;
        self._time1 = 24*60*60
        self._time = int(time.time()) - self._time1
        self.mysql = MySQL(dbConfig)

    def run(self):

        print 'Is now time -> ' , time.strftime('%Y-%m-%d %H:%I:%S',time.localtime(time.time()))
        print 'Out of time -> ' , time.strftime('%Y-%m-%d %H:%I:%S',time.localtime(self._time))
        self.check()
        self.checkOrder()
        return '';



    def checkOrder(self):
        for i in range(0, 100):
            if self._true1:
                print 'Analysis Total >> Ending!'
                return
            data = self.getOrderList()
            if data == None:
                print 'Data is Null'
                return
            Msg = BabyMQ.redis.hget('baby:message', '1')
            if Msg == None:
                print '微信消息提醒模板没有  请到MT后台添加模板'
                return
            Msg = phpserialize.unserialize(Msg)

            content = Msg['wechat_content']

            for i in data:

                order_no = i['orderId']
                order = self.getOrder(order_no)
                if order == 1:continue
                sql = "UPDATE sed_order_header SET `is_deleted`=1 WHERE id=%s" % (i['id'])
                r = self.mysql.insert(sql)

                pay_money = "%.2f" % order['pay_money']
                product_name = order['product_name']
                to_address = order['to_address']

                Msg['wechat_url'] = Msg['wechat_url'].replace('{site_url}', wechatConfig['site_url']).replace("{orderNum}", order_no.encode("utf-8"))
                Msg['content'] = content.replace("{money}", pay_money).replace("{goodsInfo}", product_name.encode("utf-8")).replace("{deliveryInfo}", to_address.encode("utf-8")).replace("{orderNum}", order_no.encode("utf-8"))
                _Msg = {}
                _Msg['openid'] = order['member_openid']
                _Msg['content'] = Msg['content']
                _Msg['title'] = Msg['name']
                _Msg['url'] = Msg['wechat_url']
                _Msg['type'] = 'news'
                BabyMQ.add('WechatMessage', json.dumps(_Msg))
                print order_no
            return
        return ''

    def getOrderList(self):
        sql = "select id,orderId from `sed_order_header` where `is_pay` = 0 AND `is_deleted`=0 AND UNIX_TIMESTAMP(createtime) <= UNIX_TIMESTAMP() - %s LIMIT 100" % self._time1;
        print sql
        e = self.mysql.query(sql)
        if e == False: return []
        list = self.mysql.fetchAllRows()
        if len(list) == 0:self._true1 = True;
        return list
        #print self.data
    def check(self):


        for i in range(0, 100):
            if self._true:
                print 'Analysis Total >> Ending!'
                return
            data = self.getList()

            if data == None:
                print 'Data is Null'
                return
            Msg = BabyMQ.redis.hget('baby:message', '1')
            if Msg == None:
                print '微信消息提醒模板没有  请到MT后台添加模板'
                return

            Msg = phpserialize.unserialize(Msg)
            content = Msg['wechat_content']

            for i in data:
                _data = json.loads(i['data'])
                if (_data.has_key('hash')):
                    num = BabyMQ.redis.hget("Activity:geoHash", _data['hash'])
                    if num != None:
                        num = int(num) - 1;
                        BabyMQ.redis.hset("Activity:geoHash", _data['hash'], num)
                sql = "UPDATE sed_new_activity_member SET `is_delete`=1 WHERE id=%s" % (i['id'])
                r1 = self.mysql.insert(sql)
                sql = "UPDATE sed_new_activity SET `amount`= `amount` + 1 WHERE id=%s" % (i['activity_id'])
                r = self.mysql.insert(sql)
                if r1 == 0 and i['open_id']:
                    order_no = i['order_no']
                    order = self.getOrder(order_no)
                    sql = "UPDATE sed_order_header SET `is_deleted`=1 WHERE id=%s" % (order['id'])
                    r = self.mysql.insert(sql)
                    pay_money = "%.2f" % order['pay_money']
                    product_name = order['product_name']
                    to_address = order['to_address']
                    Msg['wechat_url'] = Msg['wechat_url'].replace('{site_url}', wechatConfig['site_url']).replace("{orderNum}", order_no.encode("utf-8"))

                    Msg['content'] = content.replace("{money}", pay_money).replace("{goodsInfo}", product_name.encode("utf-8")).replace("{deliveryInfo}", to_address.encode("utf-8")).replace("{orderNum}", order_no.encode("utf-8"))
                    _Msg = {}
                    _Msg['openid'] = order['member_openid']
                    _Msg['content'] = Msg['content']
                    _Msg['title'] = Msg['name']
                    _Msg['url'] = Msg['wechat_url']
                    _Msg['type'] = 'news'
                    BabyMQ.add('WechatMessage', json.dumps(_Msg))

            return

    def getOrder(self, orderNo):
        sql = "SELECT * FROM sed_order_header h,sed_order_item i WHERE h.id=i.header_id AND h.orderId='%s' LIMIT 1" % orderNo
        e = self.mysql.query(sql)

        if e == False: return 1
        return self.mysql.fetchOneRow()
    def getList(self):

        #sql = "SELECT * FROM sed_new_activity_member WHERE is_pay = 0 AND is_order= 1 AND is_delete = 0 AND join_time < %s LIMIT 10" % self._time;
        sql = "SELECT * FROM sed_new_activity_member WHERE is_pay = 0 AND is_order= 1 AND is_delete = 0 AND join_time < %s LIMIT 10" % self._time;
        e = self.mysql.query(sql)

        if e == False: return
        list = self.mysql.fetchAllRows()
        if len(list) == 0:self._true = True;
        return list
        #print self.data


if __name__ == "__main__":
    _logOp = activity2order()
    _logOp.run()



