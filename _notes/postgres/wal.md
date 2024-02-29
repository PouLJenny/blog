# WAL write-ahead log

[博客](http://blog.itpub.net/133735/viewspace-2295410/ '')
## 基本术语
为了更好的理解WAL和便于沟通，有必要首先对相关的WAL术语进行简要的介绍。

1. REDO log

Redo log通常称为重做日志，在写入数据文件前，每个变更都会先行写入到Redo log中。其用途和意义在于存储数据库的所有修改历史，用于数据库故障恢复（Recovery）、增量备份（Incremental Backup）、PITR(Point In Time Recovery)和复制（Replication）。

2. WAL segment file

为了便于管理，PG把事务日志文件划分为N个segment，每个segment称为WAL segment file，每个WAL segment file大小默认为16MB。

3. XLOG Record

这是一个逻辑概念，可以理解为PG中的每一个变更都对应一条XLOG Record，这些XLOG Record存储在WAL segment file中。PG读取这些XLOG Record进行故障恢复/PITR等操作。

4. WAL buffer

WA缓冲区，不管是WAL segment file的header还是XLOG Record都会先行写入到WAL缓冲区中，在"合适的时候"再通过WAL writer写入到WAL segment file中。

5. LSN

LSN即日志序列号Log Sequence Number。表示XLOG record记录写入到事务日志中位置。LSN的值为无符号64位整型（uint64）。在事务日志中，LSN单调递增且唯一。

6. checkpointer

checkpointer是PG中的一个后台进程，该进程周期性地执行checkpoint。当执行checkpoint时，该进程会把包含checkpoint信息的XLOG Record写入到当前的WAL segment file中，该XLOG Record记录包含了最新Redo pint的位置。

7. checkpoint

检查点checkpoint由checkpointer进程执行，主要的处理流程如下：

获取Redo point，构造包含此Redo point检查点（详细请参考Checkpoint结构体）信息的XLOG Record并写入到WAL segment file中；
刷新Dirty Page到磁盘上；
更新Redo point等信息到 pg_control 文件中。
8. REDO point

REDO point是PG启动恢复的起始点，是最后一次checkpoint启动时事务日志文件的末尾亦即写入Checkpoint XLOG Record时的位置（这里的位置可以理解为事务日志文件中偏移量）。

9. pg_control

pg_control 是磁盘上的物理文件，保存检查点的基本信息，在数据库恢复中使用，可通过命令 pg_controldata 查看该文件中的内容。