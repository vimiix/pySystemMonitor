#coding=utf-8

import os
import psutil
import time
import urllib, urllib2

class MonitorAgent(object):
    def __init__(self, url='http://localhost:8000/cgi-bin/MonitorServer.py'):
        self.url = url
        self.hostInfo = {'memory':{}, 'cpu':{}, 'disk':{}, 'network':{}}
        
    #获取内存信息
    def memory(self):
        memKeys = ['total','available','percent','used','free']
        memValues = psutil.virtual_memory()
        self.memInfo = dict(zip(memKeys, memValues))
        self.memInfo = {k : '%.2f'%(v/pow(1024.0, 3))+'GB' for k, v in self.memInfo.items() if k != 'percent'}
        self.memInfo['percent'] = '%.1f%%'%memValues.percent
        return self.memInfo
        
    #获取cpu信息
    def cpu(self):
        cpuKeys = ['user','system','idle','interrupt','dpc']
        cpuValues = psutil.cpu_times()
        self.cpuInfo = dict(zip(cpuKeys, cpuValues))
        self.cpuInfo['percent'] = psutil.cpu_percent()
        return self.cpuInfo
    
    #获取磁盘信息
    def disk(self, diskName = '/'):
        diskKeys = ['total','used','free','percent']
        diskValues = psutil.disk_usage(diskName)
        self.diskInfo = dict(zip(diskKeys, diskValues))
        self.diskInfo = {k : '%.2f'%(v/pow(1024.0, 3))+'GB' for k, v in self.diskInfo.items() if k != 'percent'}
        self.diskInfo['percent'] = '%.1f%%'%diskValues.percent
        return self.diskInfo
    
    #获取网络信息
    def network(self):
        netKeys = ['bytes_sent','bytes_recv','packets_sent','packets_recv']
        netValues = psutil.net_io_counters()
        self.netInfo = dict(zip(netKeys, netValues))
        self.netInfo = {k : '%.2f'%(v/pow(1024.0, 2))+'MB' for k, v in self.netInfo.items()}
        return self.netInfo

    def send(self):
        url = self.url
        self.hostInfo['memory'] = self.memory()
        self.hostInfo['cpu'] = self.cpu()
        self.hostInfo['disk'] = self.disk()
        self.hostInfo['network'] = self.network()
        #print self.hostInfo
        self.data = urllib.urlencode(self.hostInfo)
        #print self.data
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.15 Safari/537.36'}
        req = urllib2.Request(url=url, data=self.data, headers=self.headers)
        content = urllib2.urlopen(req).read()
        #print content
        
	
if __name__ == '__main__':
    agent = MonitorAgent()
    count = 1
    while True:
        print('send data times: %d'%count)
        agent.send()
        count += 1
        time.sleep(5)
