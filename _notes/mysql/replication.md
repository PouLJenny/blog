# Mysql 主从同步

Mysql复制基础
 Mysql的复制是异步复制
 主从复制是有延迟的
 TXC分布式事务？
 Mysql的复制是基于Binlog日志的
    存在三种日志格式
    Statement:Binlog中存储Sql语句，存储量是最小的，可能会造成数据不一致
    Row:存储event数据，存储日志量大，但是不能很直接的进行读取
    Mixed:介于Row和Statement之间，对于不确定的操作使用row记录，如果每天数据操作量大，产生的日志比较多，
          可以考虑选择使用mixed格式
 Mysql复制可以是对整个实例进行复制，也可以对实例中的某个库或是某个表进行复制
    Master端：
    --binlog-do-db
    --binlog-ignore-db
    Slave端
    --replicate-do-db
    --replicate-ignore-db
    --replicate-do-table
    --replicate-ignore-table
    --replicate-wild-do-table
    --replicate-wild-ignore-table
 Mysql复制类型
    基于二进制日志的复制
    使用GTIDs完成基于事务的复制（mysql5.6之后）
 Mysql支持半同步复制