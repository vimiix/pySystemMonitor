#coding=utf-8

import cgi
import MySQLdb
import json

#这里配置要链接的数据库信息
myDatabase = {'host':'127.0.0.1',
              'port':3306,
              'user':'root',
              'passwd':'123456',
              'db':'Monitor'
              }

class hostInfo(object):
    def __init__(self):
        self.form = cgi.FieldStorage()

    def getHostInfo(self):
        return self.form

    def getMemInfo(self):
        return self.form['memory']

    def getCpuInfo(self):
        return self.form['cpu']

    def getDiskInfo(self):
        return self.form['disk']

    def getNetworkInfo(self):
        return self.form['network']

class mysql(object):
    def __init__(self, db):
        self.db = db

    def insertData(self, data):
        try:
            conn = MySQLdb.connect(host=self.db['host'], port=self.db['port'], user=self.db['user'], passwd=self.db['passwd'], db=self.db['db'])
            cur = conn.cursor()

            #获取到每个模块的字典信息
            memInfo = eval(data['memory'].value)
            cpuInfo = eval(data['cpu'].value)
            diskInfo = eval(data['disk'].value)
            netInfo = eval(data['network'].value)
            
            sql_insertMemInfo = 'insert into memory(total, available, used, free, percent) values ("%s", "%s", "%s", "%s", "%s");'\
            %(memInfo['total'], memInfo['available'], memInfo['used'], memInfo['free'], memInfo['percent'])
            sql_insertCpuInfo = 'insert into cpu(user, system, idle, interrupt, dpc) values ("%s", "%s", "%s", "%s", "%s");'\
            %(cpuInfo['user'], cpuInfo['system'], cpuInfo['idle'], cpuInfo['interrupt'], cpuInfo['dpc'])
            sql_insertDiskInfo = 'insert into disk(total, used, free, percent) values ("%s", "%s", "%s", "%s");'\
            %(diskInfo['total'], diskInfo['used'], diskInfo['free'], diskInfo['percent'])
            sql_insertNetInfo = 'insert into network(bytes_sent, bytes_recv, packets_sent, packets_recv) values ("%s", "%s", "%s", "%s");'\
            %(netInfo['bytes_sent'], netInfo['bytes_recv'], netInfo['packets_sent'], netInfo['packets_recv'])
            
            cur.execute(sql_insertMemInfo)
            cur.execute(sql_insertCpuInfo)
            cur.execute(sql_insertDiskInfo)
            cur.execute(sql_insertNetInfo)
            
            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error, e:
            print 'MySQL error msg: %d, %s'%(e.args[0], e.args[1])           
        
class frontEnd(object):
    def __init__(self, hostInfo):
        print "Content-type:text/html"
        print
        print "<html>"
        print "<head>"
        print "<meta charset=\"utf-8\">"
        print "<title>保存数据</title>"
        print "</head>"
        print "<body>"
        print 'meminfo: ',hostInfo
        print "</body>"
        print "</html>"


if __name__ == '__main__':
    data = hostInfo()
    mysql = mysql(myDatabase)
    mysql.insertData(data.getHostInfo())
    #frontEnd = frontEnd(data.getHostInfo())
    
