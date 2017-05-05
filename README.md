# pySystemMonitor
<hr>

##### (✪ω✪)这是一个系统状态信息监测的小项目（完善中...）

###### ps：仅作个人学习之用(๑╹◡╹)ﾉ"""

# 功能
<hr>

MonitorAgent文件每隔5秒，采集如下系统信息：

- 系统内存信息：memory
- 系统CPU使用信息：cpu
- 系统硬盘信息：disk
- 系统网络接发数据信息：network

将采集到的信息通过urllib和urllib2的模块以post方法提交到MonitorServer中，MonitorServer链接到MySQL数据库，将每个信息逐个存储进对应的表中。

# 项目流程图
<hr>

![](http://omfis13un.bkt.clouddn.com/pySystemMonitor.png)
