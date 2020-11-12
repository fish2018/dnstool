#!/usr/bin/env python
#coding=utf-8

from config import APP_ENV, logger
import winrm

class DnsCmd:
    def __init__(self):
        self.wintest = winrm.Session(APP_ENV.wmrTarget, auth=(APP_ENV.userName, APP_ENV.passWord))
        self.queue = []
        self.records = APP_ENV.Records
        self.domains = APP_ENV.Domains
        self.zone = APP_ENV.Zone

    def checkExist(self):
        for d in self.domains:
            r = self.wintest.run_cmd('dnscmd /enumrecords {zone} {record} /Type A'.format(zone=self.zone, record=d))
            res = str(r.std_out, encoding="utf-8")
            if "DNS_ERROR_NAME_DOES_NOT_EXIST" in res:
                # 添加到queue
                self.queue.append(d)
            else:
                logger.warning("{} 已存在解析", d)

    @logger.catch
    def addRecords(self):
        for d in self.queue:
            for r in self.records:
                self.wintest.run_cmd('dnscmd /recordadd {zone} {domain} A {record}'.format(zone=self.zone, domain=d, record=r))

    def work(self):
        self.checkExist()
        self.addRecords()

    def getAll(self):
        r = self.wintest.run_cmd('dnscmd /zoneprint {zone}'.format(zone=self.zone))
        res = str(r.std_out, encoding="utf-8")
        logger.info(res)


# DnsCmd().work()


'''
---------------------------------------------------------------------------------------------
新增一个正向区域：dnscmd  /zoneadd intramirror.com /primary
    新增一个主机 A 记录：dnscmd  /recordadd intramirror.com host01 A 172.16.11.75
        新增一个二级主机 A 记录：dnscmd  /recordadd intramirror.com  host02.2333  A 172.168.11.83   # host02.2333.intramirror.com
    新增一个正向 CNAME 记录：dnscmd  /recordadd intramirror.com host03 CNAME host01.intramirror.com

新增一个反向区域：dnscmd  /zoneadd 11.16.172.in-addr.arpa /primary
    新增一个 PTR 记录：dnscmd  /recordadd 11.16.172.in-addr.arpa 75 PTR host01.intramirror.com
    新增一个反向 CNAME 记录： dnscmd /recordadd 11.16.172.in-addr.arpa 76 CNAME 75.11.16.172.in-addr.arpa

---------------------------------------------------------------------------------------------
删除一个正向域节点：dnscmd /nodedelete  intramirror.com 2333 /tree /f
删除一个正向域：dnscmd /zonedelete intramirror.com /f

删除一条 A 记录：dnscmd /recorddelete intramirror.com host01 A 172.16.11.77 /f
删除一个主机所有 A 记录：dnscmd  /recorddelete intramirror.com host01 A /f

删除一个反向域：dnscmd /zonedelete 11.16.172.in-addr.arpa /f

删除一个 PTR 记录： dnscmd  /recorddelete 11.16.172.in-addr.arpa  98 PTR host06.intramirror.com /f
删除一个 IP 所有 PTR 记录：dnscmd /recorddelete 11.16.172.in-addr.arpa 88 PTR /f

---------------------------------------------------------------------------------------------
枚举所有正向域：dnscmd /enumzones /forward /primary
查询正向域某域所有记录：dnscmd /zoneprint intramirror.com  #包括子域记录
查询正向域某节点所有 A 记录：dnscmd /enumrecords intramirror.com @ /Type A
                          dnscmd /enumrecords intramirror.com 2333 /Type A

枚举所有反向域：dnscmd /enumzones /reverse /primary
查询反向域某域所有记录：dnscmd /zoneprint 11.16.172.in-addr.arpa
查询反向域某域 PTR 记录：dnscmd /enumrecords 11.16.172.in-addr.arpa @ /Type PTR
'''