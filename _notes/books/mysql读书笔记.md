一共135个小节 一天看5个小节  一共需要27天看完
从2018/3/29号开始到4月24号截至 看完这本书

高性能Mysql

解决并发问题的方法是采用并发控制，通过实现一个有两种类型锁组成的锁系统来解决问题。
这两种类型的锁通常被称为共享锁(share lock)和排他锁(exclusive lock),也叫读锁(read lock)和写锁(write lock)
读锁是共享的，相互不阻塞的。多个客户在同一时刻可以同时读取同一个资源，而互不干扰。写锁是排他的，也就是说
一个写锁会阻塞其他的写锁或读锁

锁策略就是在锁的开销和数据的安全性之间寻求平衡，一般都是在表上施加行级锁(row-level lock)
写锁比读锁有更高的优先级，写锁可以插入到锁队列中读锁的前mian

事物的ACID概念
原子性（atomicity） 一致性（consistency） 隔离性（isolation） 持久性（durability）

事务的隔离级别
READ UNCOMMITTED(未提交读) READ COMMITTED(提交读) REPEATABLE READ(可重复读,MySQL 的默认隔离级别) SERIALIZABLE(可串行化)

InnoDB目前处理死锁的方式是，将持有最少行级排他锁的事务进行回滚(这是相对比较简单的思索回滚算法)。
mysql默认采用自动提交的模式

多版本并发控制MVCC，不仅是mysql，包括oracle和postgreSql也实现了MVCC，MVCC行级锁的一个变种

InnoDB是基于聚簇索引建立的
Myisam 全文索引、压缩、空间函数 但是不支持事务和行级锁而且崩溃后无法安全恢复
myISAM特性
加锁合并发、 修复 、基于分词创建的索引
创建myISAM表时如果指定了DELAY_KEY_WRITE选项时，在每次修改执行完成时，不会立刻将修改后的索引写入硬盘，二是会写到内存的缓冲区
Archive引擎只支持INSERT和SELECT操作
Memory表和临时表
InnoDB + Sphinx组合实现全文索引

Mysql基准测试(benchmark)
工具： 
       集成式测试工具
       ab - Apache HTTP 基准测试工具
       http_load
       Jmeter
       单组件式测试工具
       mysqlslap
       Mysql Benchmark Suite
       Super Smack
       Database Test Suite
       Percona's TPCC-Mysql Tool
       sysbench
       MySQL 内置的BENCHMARK()函数
吞吐量
    指的是单位时间内的事务处理数，一些标准的测试被广泛使用如TPC-C（参考http://www.tpc.org）
响应时间或者延迟
并发性
可扩展性

如果存储UUID值，则应该移除“-”符号，或者更好的做法是，用UNHEX()函数转换UUID值为16字节的数字，并存储在
BINARY(16)列中。检索时可以通过HEX()函数来格式化为十六进制格式。

ipv4地址实际上是32位无符号整数，不是字符串，用小数点将地址分成四段的表示方法，只是为了让人们阅读方便
所以应该使用无符号整数存储ip地址。Mysql提供INET_ATON()和INET_NTOA()函数在这两种表达方式之间转换。

Mysql会在索引中存储null值但是oracle不会