# Canal

[github](https://github.com/alibaba/canal )

## 问题总结

1.  正常运行的canal，停止之后再启动报错： 

	2019-04-22 11:22:37.884 [destination = example , address = rm-2ze96704758roml73.mysql.rds.aliyuncs.com/10.50.154.68:3306 , EventParser] ERROR com.alibaba.otter.canal.common.alarm.LogAlarmHandler - destination:example[java.io.IOException: Received error packet: errno = 1236, sqlstate = HY000 errmsg = Could not find first log file name in binary log index file
		at com.alibaba.otter.canal.parse.inbound.mysql.dbsync.DirectLogFetcher.fetch(DirectLogFetcher.java:102)
		at com.alibaba.otter.canal.parse.inbound.mysql.MysqlConnection.dump(MysqlConnection.java:225)
		at com.alibaba.otter.canal.parse.inbound.AbstractEventParser$3.run(AbstractEventParser.java:257)
		at java.lang.Thread.run(Thread.java:745)
		
    解决方式： 
		删除实例下面的meta.dat文件可解决