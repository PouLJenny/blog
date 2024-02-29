# 分布式id生成

当数据量越来越大的时候，数据库单表无法支撑业务，这个时候就需要做分库分表，
分表之后就需要有个统一的id生成器

https://github.com/soulmachine/system-design/blob/master/cn/distributed-id-generator.md

## 数据库主键自增
优点: 实现起来比较简单
缺点：单库单表并发扛不住，每秒几千扛不住了,而且表里面会有很多数据

一般不在生产中用

## PG的sequeue
优点: 实现简单 不用担心数据量变大的问题

## UUID
优点： 本地生成，没有并发的压力
缺点： 主键太长，而且主键不是顺序的数据库频繁的页分裂

一般不考虑，不好用

## Twitter开源的Snowflake方案（第二推荐）

核心思想： 64bit 最高位0，接着41位放时间戳（毫秒，最多可使用69年），10位放机器标识（最多把snowflake程序部署到1024台机器上），12位放序号（每毫米，每台机器，可以顺序生成4096个id）

时间戳 + 机器id + 序号

优点： 高性能 高并发 分布式 可伸缩，最多扩展1024台机器，id绝对够用
缺点： 需要考虑时钟回拨的问题，还得单独部署机器 有维护成本

可投入生产

### 解决时钟回拨

1. 关闭时钟同步
    这个不太可能
2. 记录上次生成id的时间戳
   如果当前时间比上次生成的时间小 则一直等待
3. 针对第二种办法的优化，
   1s内 服务器内部记录每毫秒对应的
   服务每次启动获取新的机器id

## Redis自增机制
核心思想 使用incr命令 redis集群 比如有n台机器 没台机器的id初始值是 1，2，3，4。。。n , id自增步长n 

优点： redis一般公司都有现成的直接用就行
缺点： redis扩容比较麻烦，还有就是redis集群的主从同步一般是异步的，如果主节点挂了，从节点顶上之后可能会出现id不是最新的问题。。

## 时间戳 + 业务id (第一推荐)
核心思想： 比如打车软件，可以用时间戳 + 起点编号 + 车牌号作为一个id，业务组合上是不会有重复的。

优点： 实现简单，没有并发类的扩容问题
缺点： 理论上还是有重复的概率的，但是很小

部分适用于生产

## [flickr](http://code.flickr.net/2010/02/08/ticket-servers-distributed-unique-primary-keys-on-the-cheap/ ) （雅虎旗下图片分享平台） 数据库id生成方案 （第三推荐）

```sql
CREATE TABLE `id_generator` (
    `id` bigint(20) unsigned not null auto_increment,
    `stub` char(1) NOT NULL default ``,
    PRIMARY KEY (`id`),
    UNIQUE KEY `stub`(`stub`)
) ENGINE=MyISAM

REPLACE INTO id_generator(stub) values('a');
select LAST_INSERT_ID();
```

优点： REPLACE INTO 语法替代 INSERT 语法，表里面只有一行数据
缺点： 数据库不太好扩容，无法在高并发量的情况下使用

优化： 可以用自己的机器ip地址+线程id 或者是业务key 避免并发冲突问题,id生成的库最好是双机的步长设置成不一样的跟redis的实现方式类似

低并发场景可以用于生产

因为是单库，怎么解决单点故障问题呢？把ID的数值分成奇数和偶数，在两台数据库服务器上部署。
配置如下：
```config
TicketServer1:
auto-increment-increment = 2
auto-increment-offset = 1

TicketServer2:
auto-increment-increment = 2
auto-increment-offset = 2
```

### 变种优化

每台机器拿到的id 属于一个号段 比如id = n, 号段长度是 m , 这次的id范围就是 [n * m,(n + 1) * m - 1]
这样的话号段 在jvm内存中自增， 效率非常高， 解决了高并发的问题

数据库的话部署 s台，s > 1 , 初始值 1，2，3，4。。。s,步长s,解决了高可用的问题

这样的话就变成了非常棒的生产方案


缺点： 每次服务重启都会浪费一个号段

可以吧jvm的主键持久化到磁盘，每次重启的话读磁盘

有普通高并发场景的生产环境，还是可用的。

## 美团开源Leaf

https://tech.meituan.com/2019/03/07/open-source-project-leaf.html



## 总结

推荐的方式
1. 时间戳 + 业务id
2. Snowflake
3. flickr

美团的Leaf开源框架集成了 Flickr和Snowflake



# id混淆算法

