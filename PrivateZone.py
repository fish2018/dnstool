#!/usr/bin/env python
#coding=utf-8

from config import APP_ENV, logger
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkpvtz.request.v20180101.AddZoneRecordRequest import AddZoneRecordRequest
from aliyunsdkpvtz.request.v20180101.DescribeZoneRecordsRequest import DescribeZoneRecordsRequest

class PrivateZone:
    def __init__(self):
        self.client = AcsClient(APP_ENV.AccessKeyID, APP_ENV.AccessKeySecret, 'cn-hangzhou')
        self.zoneid = APP_ENV.ZoneId
        self.domains = APP_ENV.Domains
        self.records = APP_ENV.Records
        self.queue = [] # domains not in privateZone records list

    def checkExist(self):
        request = DescribeZoneRecordsRequest()
        request.set_accept_format('json')
        request.set_ZoneId(self.zoneid)

        for d in self.domains:
            request.set_Keyword(d)
            response = self.client.do_action_with_exception(request)
            state = json.loads(response.decode("utf-8")).get('TotalItems')
            if state < 3:
                self.queue.append(d)
            else:
                logger.warning("{} 已存在解析",d)

    @logger.catch
    def addRecords(self):
        request = AddZoneRecordRequest()
        request.set_accept_format('json')
        request.set_ZoneId(self.zoneid)
        request.set_Type("A")

        for d in self.queue:
            logger.info("域名：{}",d)
            request.set_Rr(d)

            for r in self.records:
                request.set_Value(r)
                response = self.client.do_action_with_exception(request)
                print(str(response, encoding='utf-8'))

    def work(self):
        self.checkExist()
        self.addRecords()

# PrivateZone().work()
