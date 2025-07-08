---
layout: post
title:  "Redis 整体架构"
date:   2023-06-26 10:30:15 +0800
categories: Redis
tags: Redis
permalink: /redis/redis
published: true
publish_file: 2023-06-26-redis-redis.md
toc: true
---
# Redis

本文基于Redis 7.0.11源码来分析的

## 简介

内存的key-value数据库，一般做缓存用  
[官网](https://redis.io/)  
[Github](https://github.com/redis/redis)

## 源码调试

1. `make distclean`
2. `make BUILD_WITH_DEBUG=yes -j$(nproc)`
3. 添加 .vscode/launch.json
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Redis Server",
      "type": "cppdbg",
      "request": "launch",
      "program": "${workspaceFolder}/src/redis-server",
      "args": [],
      "stopAtEntry": false,
      "cwd": "${workspaceFolder}",
      "environment": [],
      "externalConsole": false,
      "MIMode": "gdb",
      "miDebuggerPath": "/usr/bin/gdb",
      "setupCommands": [
        {
          "description": "Enable pretty-printing",
          "text": "-enable-pretty-printing",
          "ignoreFailures": true
        }
      ],
      "logging": {
        "moduleLoad": true,
        "trace": true
      }
    }
  ]
}
```

## 数据类型
- Strings
- Lists
- Sets
- Hashes
- Sorted sets
- Streams
- Geospatial indexes
- Bitmaps
- Bitfields
- HyperLogLog

### Strings

SDS（Simple Dynamic String）

没有使用原生的c字符串，因为c的字符串是一个数组尾部\0 ，统计字符串长度的时候需要遍历数组

redis3.2之前实现的字符串数据结构

```c
struct sdshdr {
    int len; // 已使用的字节数 = 字符串长度
    int free; // 未使用的字节数
    char buf[];// 字符串本身内容
}
```

但是这个结构对小字符串来说，len和free所占的内存过大,后面分裂出来了5种数据类型
`sds.h`

```c
/* Note: sdshdr5 is never used, we just access the flags byte directly.
 * However is here to document the layout of type 5 SDS strings. */
struct __attribute__ ((__packed__)) sdshdr5 {
    unsigned char flags; /* 3 lsb of type, and 5 msb of string length */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr8 {
    uint8_t len; /* used */
    uint8_t alloc; /* excluding the header and null terminator */ // 申请长度/总长度
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr16 {
    uint16_t len; /* used */
    uint16_t alloc; /* excluding the header and null terminator */
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr32 {
    uint32_t len; /* used */
    uint32_t alloc; /* excluding the header and null terminator */
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr64 {
    uint64_t len; /* used */
    uint64_t alloc; /* excluding the header and null terminator */
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
```

优化了 `strlen` 命令

**二进制安全的**，如果你在字符串中输入了 `\0` 字符，比如`re\0di\0s` 
这样的话你从redis里面读出来的字符串可能是`re di s`,这样就不对了，redis自己实现的sds数据结构，通过`len`参数可以很好的解决这个问题

内存重分配

惰性释放




### Lists

```c
typedef struct listNode {
    struct listNode *prev;
    struct listNode *next;
    void *value;
}

typedef struct list{
    listNode *head;
    listNode *tail;
    unsigned long len;
    void *(*dup)(void *ptr);
}
```
### Sets


### Hashes


### Sorted sets
跳表实现的
`server.h`
```c
/* ZSETs use a specialized version of Skiplists */
typedef struct zskiplistNode {
    sds ele;
    double score;
    struct zskiplistNode *backward;
    struct zskiplistLevel {
        struct zskiplistNode *forward;
        unsigned long span;
    } level[];
} zskiplistNode;

typedef struct zskiplist {
    struct zskiplistNode *header, *tail;
    unsigned long length;
    int level;
} zskiplist;

typedef struct zset {
    dict *dict;
    zskiplist *zsl;
} zset;
```


### Streams


### Geospatial indexes


### Bitmaps


### Bitfields


## key过期

官方文档中介绍
redis过期有两种方式
1.  a passive way
2.  an active way

passive way:
A key is passively expired simply when some client tries to access it, 
and the key is found to be timed out.

active way:
redis 有1秒10次的检验
1. test 20 random keys from set of keys with an associated expire
2. delete all the keys found expired
3. if more than 25% of keys were expired, start again from step 1.

## redis持久化

[官网对持久化的介绍](https://redis.io/topics/persistence)

作用： 用于redis的故障恢复

redis的持久化机制：
Redis provides a different range of persistence options:
1. RDB  进行时间点的数据库快照保存操作，周期性的dump内存数据到文件中

2. AOF  记录每次的写操作，redis重启的时候会进行回放，you can have different fsync policies: 
		no fsync at all, fsync every second, fsync at every query

3. 通过RDB或者AOF，都可以将redis内存中的数据给持久化到磁盘上去，然后可以将这些数据备份到别的地方去，比如可靠的云存储服务，如果redis服务器挂了，磁盘上的数据都丢了，可以从备份的云存储服务器上copy备份文件到新的redis服务器上去，恢复数据

4. 如果同时启用了RDB和AOF两种持久化机制，那么在redis重启的时候，会使用AOF来重新构建数据，因为AOF中的数据更加完整  


### RDB

#### 优点：
- RDB会生成多个数据文件，每隔数据文件代表了某一个时刻中redis的数据，这种多个数据文件的方式，非常适合做冷备份，
可以将这种完整的数据文件发送到一些远程的安全存储上去，比如说Amazon的S3服务器，以预定好的备份策略来定期备份redis中的数据
    - AOF也可以做冷备份，可以周期性的copy AOF文件到备份服务器上去，但是需要自己写定时脚本处理
- RDB对redis对外提供的读写服务，影响非常小，可以让redis保持高性能，因为redis主进程只需要fork一个子进程执行磁盘IO操作来进行RDB持久化即可
    - RDB，每次写，都是直接写入redis内存中，只是在一定的时候，才会将数据写入磁盘
    - AOF，每次都是要写文件的，虽然可以快速写入os cache，但是还是有一定的时间开销的，速度肯定比RDB略慢一些
- 相对于AOF来说，直接基于RDB数据文件来重启和恢复redis数据，更加快速
    - AOF，存放的是指令日志，做数据恢复的时候，要回放所有的指令
    - RDB，就是一份数据文件，恢复的时候，直接加载到内存中即可

综上所述，RDB特别适合做冷备份

#### 缺点：
- 如果想要在redis故障时，尽可能少的丢失数据，那么RDB没有AOF好，一般RDB的快照周期是5分钟，或者更长时间一次，这个时候得接受一旦redis进程宕机，那么会丢失最近5分钟的数据
    - 这个问题是RDB最大的缺点，不适合做第一优先的恢复方案
- RDB诶次在fork子进程来执行RDB快照数据文件生成的时候，如果数据文件特别大，可能会导致对客户端提供的服务暂停数毫秒，或者甚至数秒


#### 如何配置

redis.conf文件中，  
`save 60 10000`  
每超过60s，如果有超过10000个key发生了变更，那么就生成一个新的dump.rdb文件，就是当前redis内存中完整的数据,
这个操作也被称之为snapshotting,

也可以手动调用`save`或者`bsave` 来同步或者异步的生成快照


#### 工作流程

1. redis根据配置的检查点，尝试去生成rdb快照文件
2. fork一个子进程出来
3. 子进程尝试将数据dump到临时的rdb快照文件中
4. 完成rdb快照文件的生成之后，就替换之前的旧的快照文件
5. 如果通过`redis-cli shutdown`的方式，关掉redis，会立即生成一份rdb快照


### AOF

#### 优点：

- AOF可以更好的保护数据不丢失，一般AOF会每隔1秒，通过一个后台线程执行一次fsync操作，最多丢失1秒钟的数据
- AOF日志文件是用append-only的模式写入的，没有任何磁盘寻址的开销，性能非常高，而且文件不易破损，即使文件尾部损坏，也很容易修复
- AOF日志文件即使过大的时候，出现后台重写操作，也不会影响客户端的读写，因为在rewrite log的时候，会对其中指令进行压缩，创建出一份需要恢复数据的最小日志出来，再创建新日志文件的时候，老的日志文件还是照常写入，当新的merge后的日志文件ready的时候，再交换新老日志文件即可，
- AOF日志文件的命令通过人类可读的方式进行记录，这个特性非常适合做灾难性的误删除的紧急恢复，比如某人不小心用flushall命令清空了所有数据，只要这个时候后台rewrite还没有发生，那么就可以立即copy AOF文件，将最后一条flushall命令给删了，然后再将该AOF文件放回去，就可以通过恢复机制，自动恢复所有数据

#### 缺点：

- 对于同一份数据来说，AOF日志文件通常比RDB数据快照文件要大
- AOF开启后，支持的写QPS会比RDB支持的写QPS低，因为AOF一般会配置成每秒fsync一次日志文件记录，当然，每秒一次fsync，性能还是很高的
    - 如果你要保证一条数据都不丢，也是可以的，AOF的fsync设置成每写入一条数据，fsync一次，那就完蛋了，redis的QPS会大大降低
- 以前AOF发生过BUG，就是通过AOF记录的日志，进行数据恢复的时候，没有恢复一模一样的数据出来，所以说，类似AOF这种缴费负载的基于命令日志/merge/回放的方式，比基于RDB每次持久化一份完整的数据快照文件的方式，更加脆弱一些，容易有bug，不过AOF就是为了避免rewrite过程导致的bug,因此每次rewrite并不是基于旧的指令日志进行merge的，而是基于当前内存中的数据进行指令的重新构建，这样健壮性会好很多

- 做数据恢复的时候比较慢，如果做冷备份的话，定期脚本要自己写


#### 如何配置

AOF持久化，默认是关闭的
`redis.conf`中`appendonly yes`配置后就可以打开了。在生产环境中，一般来说AOF都是要打开的，
即使AOF和RDB都打开了，redis重启的时候，也是优先通过AOF进行数据的恢复

可以配置AOF的fsync的策略
- `appendfsync always`  每次写入一条数据，立即将这个数据对应的写日志fsync到磁盘上去，新能非常差
- `appendfsync everysec` 每秒执行fsync操作，生产环境一般这样配置，性能很高
- `appendfsync no` redis仅仅将数据写入到`os cache`就不管了

#### 配置 AOF rewrite

redis的内存有限，很多数据可能会自动过期，可能会被用户删除，也可能会被redis用缓存清楚的算法清理掉

```conf
# Automatic rewrite of the append only file.
# Redis is able to automatically rewrite the log file implicitly calling
# BGREWRITEAOF when the AOF log size grows by the specified percentage.
#
# This is how it works: Redis remembers the size of the AOF file after the
# latest rewrite (if no rewrite has happened since the restart, the size of
# the AOF at startup is used).
#
# This base size is compared to the current size. If the current size is
# bigger than the specified percentage, the rewrite is triggered. Also
# you need to specify a minimal size for the AOF file to be rewritten, this
# is useful to avoid rewriting the AOF file even if the percentage increase
# is reached but it is still pretty small.
#
# Specify a percentage of zero in order to disable the automatic AOF
# rewrite feature.
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

#### AOF Rewrite流程

1. redis fork一个子进程
2. 子进程是基于当前内存中的数据，构建日志，开始往一个新的临时的AOF文件中写入日志
3. redis主进程在内存中写入日志，同时新的日志也继续写入旧的AOF文件
4. 子进程写完了之后，主进程将内存中的新日志再次追加到新的AOF文件中
5. 用新的日志文件替换掉旧的日志文件


#### AOF文件破损修复

如果redis在append数据到文件中时，机器宕机了，可能会导致AOF文件破损

可以使用 `redis-check-aof --fix` 命令来修复破损的AOF文件

#### AOF和RDB同时工作

1. 如果RDB在执行snapshotting的过程中，redis不会执行AOF rewrite操作，如果在执行AOF rewrite操作过程中，则不会执行RDB snapshotting
2. 如果RDB在执行snapshotting的过程中，用户手动执行了 `BGREWRITEAOF` 命令，要等RDB 快照生成后，才会执行
3. 同时有RDB和AOF的持久化文件，那么redis重启的时候，会优先使用AOF进行数据恢复，因为其中的日志更完整



### RDB和AOF该如何选择

- 不要仅仅使用RDB，因为那样会导致你丢失很多的数据
- 也不要仅仅使用AOF，因为那样有两个问题
    1. 你通过AOF做冷备份，没有RDB冷备份，来的恢复速度快
    2.  RDB每次简单粗暴生成快照数据，更加健壮，可以避免AOF这种复杂的备份和恢复机制的bug
- 综合使用AOF和RDB两种持久化机制，用AOF来保证数据不丢失，作为数据恢复的一种选择，用RDB来做不同程度的冷备份，在AOF文件都丢失或损坏的情况下，还可以使用RDB来进行快速的数据恢复 


### redis企业级配置方案

#### 企业级持久化配置策略

1. RDB的生成策略用默认的就差不多
2. AOF一定要打开， `fsync everysec`
3. 适当调整下面两个配置，用默认的也是可以的
```conf
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

#### 数据备份方案

1. 写crontab定时调度脚本去做数据备份
2. 每小时都copy一份rdb的备份，到一个目录中去，仅仅保留最近48小时的备份
3. 每天都保留一份当日的RDB的备份，到一个目录中去，仅仅保留最近一个月的备份
4. 每次copy备份的时候，都把太旧的备份给删了
5. 每天晚上将当前服务器上所有的数据备份，发送一份到远程的云服务器上去

##### 每小时copy一次备份，删除48小时前的数据
``` shell
crontab -e

0 * * * * sh /usr/local/redis/copy/redis_rdb_copy_hourly.sh
```

redis_rdb_copy_hourly.sh

```shell
#!/bin/sh 

cur_date=`date +%Y%m%d%k`
rm -rf /usr/local/redis/snapshotting/$cur_date
mkdir /usr/local/redis/snapshotting/$cur_date
cp /var/redis/6379/dump.rdb /usr/local/redis/snapshotting/$cur_date

del_date=`date -d -48hour +%Y%m%d%k`
rm -rf /usr/local/redis/snapshotting/$del_date
```

##### 每天copy一次备份

```shell
crontab -e

0 0 * * * sh /usr/local/redis/copy/redis_rdb_copy_daily.sh
```

redis_rdb_copy_daily.sh

```shell
#!/bin/sh 

cur_date=`date +%Y%m%d`
rm -rf /usr/local/redis/snapshotting/$cur_date
mkdir /usr/local/redis/snapshotting/$cur_date
cp /var/redis/6379/dump.rdb /usr/local/redis/snapshotting/$cur_date

del_date=`date -d -1month +%Y%m%d`
rm -rf /usr/local/redis/snapshotting/$del_date
```

#####  每天一次将所有数据上传一次到远程的云服务器上去

#### 数据恢复方案

1. 如果是redis进程挂掉，那么重启redis进程即可，直接基于AOF日志文件恢复数据
2. 如果是redis进程所在机器挂掉，那么重启机器后，尝试重启redis进程，尝试直接基于AOF日志文件进行数据恢复
3. 如果redis当前最新的AOF和RDB文件出现了丢失/损坏，那么可以尝试基于该机器上当前的某个最新的RDB数据副本进行数据恢复
    1. 停止redis
    2. 配置文件关闭AOF
    3. 拷贝rdb备份 
    4. 重启redis 
    5. 确认数据恢复
    6. 在命令行热修改redis配置，打开AOF，这个时候redis会将内存中的数据对应的日志，写入AOF文件中去
    7. 停止redis
    8. 修改配置文件，打开AOF
    9. 再次重启AOF
4. 如果当前机器上的所有RDB文件全部损坏，那么从远程的云服务上拉取最新的RDB快照回来恢复数据
5. 如果是发现有重大的数据错误，比如某个小时上线的程序一下子将数据全部污染了，数据全错了，那么可以选择某个更早的时间点，对数据进行恢复
   - 举个例子，12点上线了代码，发现代码有bug，导致代码生成的所有的缓存数据，写入redis，全部错了
     找到一份11点的rdb的冷备，然后按照上面的步骤，去恢复到11点的数据，不就可以了吗






## Redis主从架构+读写分离

redis replication -> 主从架构 -> 读写分离 -> 水平扩容支撑读高并发

### redis replication

#### 核心机制
[官方文档](https://redis.io/topics/replication) 

1. redis采用异步方式复制数据到slave节点，不过redis 2.8开始，slave node会周期性地确认自己每次复制的数据量
2. 一个master node是可以配置多个slave node的
3. slave node也可以连接其他的slave node
4. slave node做复制的时候，是不会block master node的正常工作的
5. slave node在做复制的时候，也不会block对自己的查询操作，它会用旧的数据集来提供服务; 但是复制完成的时候，需要删除旧数据集，加载新数据集，这个时候就会暂停对外服务了
6. slave node主要用来进行横向扩容，做读写分离，扩容的slave node可以提高读的吞吐量

#### 核心原理

当启动一个slave node的时候，它会发送一个PSYNC命令给master node

如果这是slave node重新连接master node，那么master node仅仅会复制给slave部分缺少的数据; 否则如果是slave node第一次连接master node，那么会触发一次full resynchronization

开始full resynchronization的时候，master会启动一个后台线程，开始生成一份RDB快照文件，同时还会将从客户端收到的所有写命令缓存在内存中。RDB文件生成完毕之后，master会将这个RDB发送给slave，slave会先写入本地磁盘，然后再从本地磁盘加载到内存中。然后master会将内存中缓存的写命令发送给slave，slave也会同步这些数据。

slave node如果跟master node有网络故障，断开了连接，会自动重连。master如果发现有多个slave node都来重新连接，仅仅会启动一个rdb save操作，用一份数据服务所有slave node。

#### 主从复制的断点续传

从redis 2.8开始，就支持主从复制的断点续传，如果主从复制过程中，网络连接断掉了，那么可以接着上次复制的地方，继续复制下去，而不是从头开始复制一份

master node会在内存中常见一个backlog，master和slave都会保存一个replica offset还有一个master id，offset就是保存在backlog中的。如果master和slave网络连接断掉了，slave会让master从上次的replica offset开始继续复制

但是如果没有找到对应的offset，那么就会执行一次resynchronization

#### 无磁盘化复制

master在内存中直接创建rdb，然后发送给slave，不会在自己本地落地磁盘了

repl-diskless-sync
repl-diskless-sync-delay，等待一定时长再开始复制，因为要等更多slave重新连接过来

#### 过期key处理

slave不会过期key，只会等待master过期key。如果master过期了一个key，或者通过LRU淘汰了一个key，那么会模拟一条del命令发送给slave。


#### 安装redis集群

#### Docker安装

1. 配置Master redis.conf文件

创建目录
```shell
mkdir -p /home/poul/workspace/soft/docker/redis-01/data
## 复制一份默认的redis配置文件到 /home/poul/workspace/soft/docker/redis-01 下
```

修改Master redis.conf配置

```conf
## 修改bind地址
bind 0.0.0.0 -::1
## RDB配置
save 3600 1
save 300 100
save 60 10000

## 打开AOF
appendonly yes
appendfsync everysec
## 持久化目录
dir /data
## 安全认证
masterauth redis-pass
requirepass redis-pass
```

2. 启动Master Docker镜像 将目录 `/usr/local/etc/redis/` 映射到到宿主机的目录方便操作

```shell
## 先用`--rm`参数测试 不要加`-d` 
sudo docker run --rm -v /home/poul/workspace/soft/docker/redis-01:/usr/local/etc/redis  -v /home/poul/workspace/soft/docker/redis-01/data:/data -p 6379:6379 --name redis-01 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

## 测试通过后再加上`-d` 参数，并去掉 `--rm`参数
sudo docker run  -v /home/poul/workspace/soft/docker/redis-01:/usr/local/etc/redis  -v /home/poul/workspace/soft/docker/redis-01/data:/data -p 6379:6379 --name redis-01 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
```

3. 配置Slave `redis.conf`文件

```shell
mkdir -p /home/poul/workspace/soft/docker/redis-02/data
## 复制一份默认的redis配置文件到 /home/poul/workspace/soft/docker/redis-01 下

## 查询一下主节点的ip 给下面的配置使用
sudo docker inspect redis-01 | grep IPAddres
```

修改Slave redis.conf配置

```conf
## 修改bind地址
bind 0.0.0.0 -::1
## RDB配置
save 3600 1
save 300 100
save 60 10000

## 打开AOF
appendonly yes
appendfsync everysec
## 持久化目录
dir /data
## 安全认证
masterauth redis-pass
requirepass redis-pass

## 配置master机器
replicaof 172.17.0.2 6379

## 从节点设置为制度
replica-read-only yes
```


4. 启动Slave Docker镜像 将目录 `/usr/local/etc/redis/` 映射到到宿主机的目录方便操作

```shell
## 先用`--rm`参数测试 不要加`-d` 
sudo docker run --rm -v /home/poul/workspace/soft/docker/redis-02:/usr/local/etc/redis  -v /home/poul/workspace/soft/docker/redis-02/data:/data -p 6479:6379 --name redis-02 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

## 测试通过后再加上`-d` 参数，并去掉 `--rm`参数
sudo docker run -v /home/poul/workspace/soft/docker/redis-02:/usr/local/etc/redis  -v /home/poul/workspace/soft/docker/redis-02/data:/data -p 6479:6379 --name redis-02 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
```

5. 在redis命令行里可以通过执行 `info replication` 命令 查看节点的复制状态 



### redis主从架构下如果做到99.99%高可用

如果你的系统可以保证在全年，99.99%的时间内，都是处于可用的状态的，那么就可以称之为高可用性

redis主从架构下有个问题，就是master节点，一点挂掉后，整个集群就不可以用了，以此，引出了，一个概念，sentinel/sentry 哨兵模式

#### 哨兵

[官方文档](https://redis.io/topics/sentinel '')

哨兵是redis集群架构中非常重要的一个组件,主要功能如下
1. 集群监控 负责监控redis master 和 slave进程是否正常工作
2. 消息通知 如果某个redis 实例有故障，那么哨兵负责发送消息作为报警通知给管理员
3. 故障转移(failover) 如果master node挂掉了，会自动转移到slave node上
4. 配置中心， 如果故障转移发生了，通知client客户端新的master地址


哨兵本身也是分布式的，作为一个哨兵集群去运行，互相协同工作
1. 故障转移时，判断一个master node是否宕机了，需要大部分的哨兵都同意才行，涉及到了分布式选举的问题
2. 即使部分哨兵节点挂掉了，哨兵集群还是能正常工作的，因为如果一个作为高可用机制重要组成部分的故障转移系统本身就是单点的，那就很坑了


哨兵的核心知识
1. 哨兵至少需要3个实例，来保证自己的健壮性
2. 哨兵+redis主从的部署架构，是不会保证数据零丢失的，只能保证redis集群的高可用性
3. 对于哨兵 + redis主从这种复杂的部署架构，尽量在测试环境和生产环境，都进行充足的测试和演练


为什么哨兵集群只有两个节点无法正常工作，哨兵集群必须部署2个以上节点？

如果哨兵集群仅仅部署了个2个哨兵实例，quorum=1

```
+----+         +----+
| M1 |---------| R1 |
| S1 |         | S2 |
+----+         +----+
```
Configuration: quorum = 1

master宕机，s1和s2中只要有1个哨兵认为master宕机就可以还行切换，同时s1和s2中会选举出一个哨兵来执行故障转移
同时这个时候，需要majority，也就是大多数哨兵都是运行的，2个哨兵的majority就是2（2的majority=2，3的majority=2，5的majority=3，4的majority=2），2个哨兵都运行着，就可以允许执行故障转移
但是如果整个M1和S1运行的机器宕机了，那么哨兵只有1个了，此时就没有majority来允许执行故障转移，虽然另外一台机器还有一个R1，但是故障转移不会执行

经典的3节点哨兵集群

```
       +----+
       | M1 |
       | S1 |
       +----+
          |
+----+    |    +----+
| R2 |----+----| R3 |
| S2 |         | S3 |
+----+         +----+
```
Configuration: quorum = 2，majority
如果M1所在机器宕机了，那么三个哨兵还剩下2个，S2和S3可以一致认为master宕机，然后选举出一个来执行故障转移
同时3个哨兵的majority是2，所以还剩下的2个哨兵运行着，就可以允许执行故障转移

#### 哨兵的安装
##### Docker下安装

复制一份默认的sentinel.conf文件到目录 `/home/poul/workspace/soft/docker/redis-sentinel-01`

修改sentinel的配置文件如下:
```conf
## 配置工作目录
dir /data

## 监听的master结点
sentinel monitor mymaster 172.17.0.2  6379 2

sentinel down-after-milliseconds mymaster 30000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1

## master节点的密码
sentinel auth-pass mymaster redis-pass
```

```shell
## 先测试
sudo docker run --rm -v /home/poul/workspace/soft/docker/redis-sentinel-01:/usr/local/etc/redis -v /home/poul/workspace/soft/docker/redis-sentinel-01/data:/data -p 26379:26379 --name redis-sentinel-01 redis:6.2.5 redis-sentinel /usr/local/etc/redis/sentinel.conf

## ok后直接后台启动
sudo docker run -it -v /home/poul/workspace/soft/docker/redis-sentinel-01:/usr/local/etc/redis -v /home/poul/workspace/soft/docker/redis-sentinel-01/data:/data -p 26379:26379 --name redis-sentinel-01 -d redis:6.2.5 redis-sentinel /usr/local/etc/redis/sentinel.conf

## 其他两个节点如法炮制
sudo docker run --rm -v /home/poul/workspace/soft/docker/redis-sentinel-02:/usr/local/etc/redis -v /home/poul/workspace/soft/docker/redis-sentinel-02/data:/data -p 26479:26379 --name redis-sentinel-02 redis:6.2.5 redis-sentinel /usr/local/etc/redis/sentinel.conf

sudo docker run -it -v /home/poul/workspace/soft/docker/redis-sentinel-02:/usr/local/etc/redis -v /home/poul/workspace/soft/docker/redis-sentinel-02/data:/data -p 26479:26379 --name redis-sentinel-02 -d redis:6.2.5 redis-sentinel /usr/local/etc/redis/sentinel.conf


sudo docker run --rm -v /home/poul/workspace/soft/docker/redis-sentinel-03:/usr/local/etc/redis -v /home/poul/workspace/soft/docker/redis-sentinel-03/data:/data -p 26579:26379 --name redis-sentinel-03 redis:6.2.5 redis-sentinel /usr/local/etc/redis/sentinel.conf

sudo docker run -it -v /home/poul/workspace/soft/docker/redis-sentinel-03:/usr/local/etc/redis -v /home/poul/workspace/soft/docker/redis-sentinel-03/data:/data -p 26579:26379 --name redis-sentinel-03 -d redis:6.2.5 redis-sentinel /usr/local/etc/redis/sentinel.conf
```

连到某个哨兵上查询信息 

```shell
redis-cli -p 26379
```

```shell
sentinel master mymaster
```


### redis cluster

#### 原理

多master + 读写分离 + 高可用

- [Redis Cluster tutorial](https://redis.io/topics/cluster-tutorial): a gentle introduction and setup guide to Redis Cluster.
- [Redis Cluster specification](https://redis.io/topics/cluster-spec): the more formal description of the behavior and algorithms used in Redis Cluster.

1. 自动将数据进行分片，每个master上放一部分数据
2. 提供内置的高可用支持，部分master不可用时，还是可以继续工作的

在redis cluster架构下，每个redis要放开两个端口号，比如一个是6379，另外一个就是加10000的端口号，比如16379  
16379端口号是用来进行节点间通信的，也就是cluster bus的东西，集群总线。cluster bus的通信，用来进行故障检测，配置更新，故障转移授权  
cluster bus用了另外一种二进制的协议，主要用于节点间进行高效的数据交换，占用更少的网络带宽和处理时间

至少3个master节点启动，官方建议每个master带一个slave，这样就是6台机器

分布式数据存储的核心算法  
hash算法 -> 一致性hash算法（memcached） -> redis cluster，hash slot算法

1. 最老土的hash算法和弊端（大量缓存重建）
2. 一致性hash算法（自动缓存迁移）+虚拟节点（自动负载均衡）
3. redis cluster的hash slot算法  
    redis cluster有固定的16384个hash slot，对每个key计算CRC16值，然后对16384取模，可以获取key对应的hash slot  
    redis cluster中每个master都会持有部分slot，比如有3个master，那么可能每个master持有5000多个hash slot  
    hash slot让node的增加和移除很简单，增加一个master，就将其他master的hash slot移动部分过去，减少一个master，就将它的hash slot移动到其他master上去  
    移动hash slot的成本是非常低的  
    客户端的api，可以对指定的数据，让他们走同一个hash slot，通过hash tag来实现  



#### 安装Redis Cluster

##### Docker中安装

1. 配置redis.conf文件

```conf
bind 0.0.0.0
port 7001
cluster-enabled yes
cluster-config-file /data/7001.conf
cluster-node-timeout 15000
daemonize	yes	

pidfile		/var/run/redis_7001.pid 						
dir 		/data	
appendonly yes

## 安全认证
masterauth redis-pass
requirepass redis-pass
```

2. 启动docker container

```shell
# 创建一个给redis-cluster使用的网络
sudo docker network create redis-cluster

# 尝试启动一下
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-01/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-01/data:/data -p 7001:7001 --name redis-cluster-01 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-01/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-01/data:/data -p 7001:7001 --name redis-cluster-01 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

## 其他5个节点 如法炮制
## 02
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-02/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-02/data:/data -p 7002:7001 --name redis-cluster-02 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-02/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-02/data:/data -p 7002:7001 --name redis-cluster-02 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

## 03
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-03/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-03/data:/data -p 7003:7001 --name redis-cluster-03 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-03/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-03/data:/data -p 7003:7001 --name redis-cluster-03 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

## 04 
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-04/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-04/data:/data -p 7004:7001 --name redis-cluster-04 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-04/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-04/data:/data -p 7004:7001 --name redis-cluster-04 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
## 05 
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-05/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-05/data:/data -p 7005:7001 --name redis-cluster-05 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-05/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-05/data:/data -p 7005:7001 --name redis-cluster-05 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
## 06
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-06/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-06/data:/data -p 7006:7001 --name redis-cluster-06 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-06/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-06/data:/data -p 7006:7001 --name redis-cluster-06 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
# 后台启动
```

3. 创建集群

`gem install redis`

```shell
/home/poul/workspace/soft/redis/redis6/bin/redis-cli --cluster create 172.18.0.2:7001 172.18.0.3:7001 172.18.0.4:7001 172.18.0.5:7001  172.18.0.6:7001  172.18.0.7:7001 --cluster-replicas 1 -a redis-pass
```

校验一下  

```shell
/home/poul/workspace/soft/redis/redis6/bin/redis-cli --cluster check 172.17.0.2:7001 -a redis-pass
```

**注意：** 
1. 在slave节点上查询操作，第一次建立连接时 需要执行一下 `readonly` 命令
2. 通过 `./redis-cli -c` 可以自动重定向到key所在的节点
3. 读写分离的redis-cluster，的java客户端实现问题   
    如果你要让最流行的jedis做redis cluster的读写分离的访问，那可能还得自己修改一点jedis的源码，成本比较高  
    要不然你就是自己基于jedis，封装一下，自己做一个redis cluster的读写分离的访问api  
    核心的思路，就是说，redis cluster的时候，就没有所谓的读写分离的概念了  
    读写分离，是为了什么，主要是因为要建立一主多从的架构，才能横向任意扩展slave node去支撑更大的读吞吐量  
    redis cluster的架构下，实际上本身master就是可以任意扩展的，你如果要支撑更大的读吞吐量，或者写吞吐 量，或者数据量，都可以直接对master进行横向扩展就可以了?? 但是某个master挂了数据不久丢了吗  

4. 压测一下试试

```shell
/home/poul/workspace/soft/redis/redis6/bin/redis-benchmark -p 7001 --cluster -a redis-pass --csv
```

5. 手动扩容redis集群

```conf
## 07 
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-07/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-07/data:/data -p 7007:7001 --name redis-cluster-07 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-07/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-07/data:/data -p 7007:7001 --name redis-cluster-07 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
## 08
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-08/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-08/data:/data -p 7008:7001 --name redis-cluster-08 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-08/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-08/data:/data -p 7008:7001 --name redis-cluster-08 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
```

执行命令

```shell
/home/poul/workspace/soft/redis/redis6/bin/redis-cli --cluster add-node 172.17.0.8:7001 172.17.0.2:7001 -a redis-pass

/home/poul/workspace/soft/redis/redis6/bin/redis-cli --cluster add-node 172.17.0.9:7001 172.17.0.2:7001 -a redis-pass --cluster-slave --cluster-master-id 98c710d43e7ff7f9a035cdba511d621ec0bbd423
```

6. reshard 

```shell
/home/poul/workspace/soft/redis/redis6/bin/redis-cli --cluster reshard 172.17.0.2:7001 -a redis-pass

## 然后根据下面的提示一步一步操作
## 会提示要移动多少slots 这个地方用公式 (2 ^ 14 / master数量 ) 得到这个数就可以了
How many slots do you want to move (from 1 to 16384)?

## 输入要接受 新的slot的节点id 
What is the receiving node ID?

## 输入 想从哪些节点 move slot 可输入多个 输入完成后 再输入done 结束
Please enter all the source node IDs.
  Type 'all' to use all the nodes as source nodes for the hash slots.
  Type 'done' once you entered all the source nodes IDs.
  Source node #1:

## 是否接受 reshard plan，接受的话 输入yes 
Do you want to proceed with the proposed reshard plan (yes/no)? 
```

删除node

```shell
## 如果被删除的节点的slot非空的话需要先把结点中的slot平均move到其他节点 需要移动的slot数目为 被移除节点slot / 剩余master节点数量 ，然后一个一个的移动
/home/poul/workspace/soft/redis/redis6/bin/redis-cli --cluster del-node 127.0.0.2:7001 54478f516721e01586322939a5044169abc670f7 -a redis-pass
```

#### Slave的自动迁移
比如现在有10个master，每个有1个slave，然后新增了3个slave作为冗余，有的master就有2个slave了，有的master出现了salve冗余  
如果某个master的slave挂了，那么redis cluster会自动迁移一个冗余的slave给那个master  
只要多加一些冗余的slave就可以了  
为了避免的场景，就是说，如果你每个master只有一个slave，万一说一个slave死了，然后很快，master也死了，那可用性还是降低了  
但是如果你给整个集群挂载了一些冗余slave，那么某个master的slave死了，冗余的slave会被自动迁移过去，作为master的新slave，此时即使那个master也死了  
还是有一个slave会切换成master的  
之前有一个master是有冗余slave的，直接让其他master其中的一个slave死掉，然后看有冗余slave会不会自动挂载到那个master  

#### 节点间的通信机制

##### gossip协议

翻译过来是 小道流言

所有节点都持有一份元数据，不同的节点如果出现了元数据的变更之后，就不断将元数据发送给其他的节点，让其他节点也进行元数据的变更

跟集中式（比如zookeeper）不同的是，不是将集群元数据（节点信息，故障等等）集中存储在某个节点上，而是互相之间不断通信，保持整个集群所有节点的数据是完整的，

集中式  
优点： 元数据的更新和读取，实效性非常好，一旦元数据出现了变更，立即就更新到集中式的存储中，其他节点读取的时候立即就可以感知到  
缺点： 所有的元数据的更新压力全部集中在一个地方，可能会导致元数据的存储有压力

gossip：  
优点: 元数据的更新比较分散，不是集中在一起，更新请求会陆陆续续，打到所有的节点上去更新，有一定的延时，降低了压力  
缺点：元数据更新有延时，可能导致集群的一些操作会有一些滞后  

##### 10000端口号

每个节点都有一个专门用于节点间通信的端口，就是自己提供服务的端口号 + 10000，比如7001，那么用于节点间通信的端口就是17001

每个节点，每隔一段时间都会往另外几个节点发送ping消息，同时其他几点接收到ping之后返回pong

##### 交换的信息

节点间，交换的信息有 故障信息，节点的增加和移除，hash slot信息，等等


gossip协议包含多种消息，包括ping pong meet fail 等等

- meet 某个节点发送meet给新加入的节点，让心节点加入集群中，然后新节点就会开始与其他节点进行通信 `./redis-cli --cluster add-node` 命令其实内部就是发送了一个gossip meet消息，给新加入的节点，通知那个节点去加入我们的集群
- ping 每个节点都会频繁给其他节点发送ping 其中包含自己的状态还有自己维护的集群元数据，互相通过ping 交换元数据，每个节点每秒都会频繁发送ping给其他的集群，ping，频繁的互相之间交换数据，互相进行元数据的更新
- pong 返回ping和meet,包含自己的状态和其他信息，也可以用于信息广播和更新
- fail 某个节点判断另一个节点fail之后。就发送fail给其他节点，通知其他节点，指定的节点宕机了

##### ping消息深入

ping很频繁，而且要携带一些元数据，所以可能会加重网络负担。每个节点每秒会执行10次ping.每次会选择5个最久没有通信的其他节点，当然如果发现某个节点通信延时达到了cluster_node_timeout / 2，那么立即发送ping,避免数据交换延时过长，  
所以cluster_node_timeout可以调节,如果调节比较大，那么会降低发送的频率。每次ping，一个是带上自己节点的信息。还有就是带上1/10其他节点的信息。发送出去，进行数据交换。至少包含3个其他节点的信息。最多包含总节点-2个其他节点的信息


#### 高可用和主备切换原理

判断节点宕机

如果一个节点认为另外一个节点宕机，那就是pfail，主观宕机  
如果多个节点都认为另外一个节点宕机了，那么就是fail，客观宕机，跟哨兵的原理一样  
在`cluster-note-timeout`内，某个节点一直没有返回pong，那么就被任务pfail  
如果一个节点认为某个节点fail了，那么就会在gossip消息中，ping给其他节点，如果超过半数的节点都认为pfail了，那么就会变成fail

从节点过滤

对宕机的master node，从其所有的slave node中，选择一个切换成master node  
检查每个slave node与master node断开链接的时间，如果超过了cluster-node-timeout * cluster-slave-validity-factor ，那么就没有资格切换成master,这个跟哨兵的原理是一样的。  
每个从节点，都根据自己对master复制数据的offset，来设置一个选举时间，offset越大（复制数据越多）的从节点，选举时间越靠前，优先进行选举。  
所有的master node开始投票，给所有的slave进行投票，如果大部分master node (N/2 + 1) 都投票给了某个从节点，那么就选举通过，从节点执行主备切换，从节点切换为主节点  

与哨兵比较

整个流程跟哨兵相比，非常类似，所以说redis cluster功能强大，直接集成了replication和sentinal的功能

## 压测

### 工具

使用官方的redis-benchmark就可以了  
[官方文档](https://redis.io/docs/management/optimization/benchmarks/)

```shell
./redis-benchmark -h 127.0.0.1 -p 6379
```
## 常见问题和优化思路

### maxmemory-policy，
[Redis LRU官方文档](https://redis.io/topics/lru-cache)
可以设置内存达到最大闲置后，采取什么策略来处理 
1. noeviction: 如果内存使用达到了maxmemory，client还要继续写入数据，那么就直接报错给客户端
2. allkeys-lru: 就是我们常说的LRU算法，移除掉最近最少使用的那些keys对应的数据
3. volatile-lru: 也是采取LRU算法，但是仅仅针对那些设置了指定存活时间（TTL）的key才会清理掉
4. allkeys-random: 随机选择一些key来删除掉
5. volatile-random: 随机选择一些设置了TTL的key来删除掉
6. volatile-ttl: 移除掉部分keys，选择那些TTL时间比较短的keys

### fork耗时导致高并发请求延时

RDB和AOF的时候，其实会有生成RDB快照，AOF rewrite，耗费磁盘IO的过程，主进程fork子进程  
fork的时候，子进程是需要拷贝父进程的空间内存页表的，也是会耗费一定的时间的  
一般来说，如果父进程内存有1个G的数据，那么fork可能会耗费在20ms左右，如果是10G~30G，那么就会耗费20 * 10，甚至20 * 30，也就是几百毫秒的时间  
info stats中的latest_fork_usec，可以看到最近一次form的时长  
redis单机QPS一般在几万，fork可能一下子就会拖慢几万条操作的请求时长，从几毫秒变成1秒  

优化思路  
fork耗时跟redis主进程的内存有关系，一般控制redis的内存在10GB以内，slave -> master，全量复制  

### AOF的阻塞问题

redis将数据写入AOF缓冲区，单独开一个现场做fsync操作，每秒一次  
但是redis主线程会检查两次fsync的时间，如果距离上次fsync时间超过了2秒，那么写请求就会阻塞  
everysec，最多丢失2秒的数据  
一旦fsync超过2秒的延时，整个redis就被拖慢  

优化思路  
优化硬盘写入速度，建议采用SSD，不要用普通的机械硬盘，SSD，大幅度提升磁盘读写的速度

### 主从复制延迟问题

主从复制可能会超时严重，这个时候需要良好的监控和报警机制  
在info replication中，可以看到master和slave复制的offset，做一个差值就可以看到对应的延迟量  
如果延迟过多，那么就进行报警  

### 主从复制风暴问题

如果一下子让多个slave从master去执行全量复制，一份大的rdb同时发送到多个slave，会导致网络带宽被严重占用  
如果一个master真的要挂载多个slave，那尽量用树状结构，不要用星型结构  

### vm.overcommit_memory

- 0: 检查有没有足够内存，没有的话申请内存失败
- 1: 允许使用内存直到用完为止
- 2: 内存地址空间不能超过swap + 50%   
如果是0的话，可能导致类似fork等操作执行失败，申请不到足够的内存空间

```shell
cat /proc/sys/vm/overcommit_memory
echo "vm.overcommit_memory=1" >> /etc/sysctl.conf
sysctl vm.overcommit_memory=1
```

### swapiness
cat /proc/version，查看linux内核版本  
如果linux内核版本<3.5，那么swapiness设置为0，这样系统宁愿swap也不会oom killer（杀掉进程）  
如果linux内核版本>=3.5，那么swapiness设置为1，这样系统宁愿swap也不会oom killer  

保证redis不会被杀掉

```shell
echo 0 > /proc/sys/vm/swappiness
echo vm.swapiness=0 >> /etc/sysctl.conf
```

### 最大打开文件句柄

```shell
ulimit -n 10032 10032
```

自己去上网搜一下，不同的操作系统，版本，设置的方式都不太一样

### tcp backlog

```shell
cat /proc/sys/net/core/somaxconn
echo 511 > /proc/sys/net/core/somaxconn
```

### 监控redis命令执行耗时
配置打印慢日志 一般redis单机qps可以达到几万 

### Pipline 或者lua脚本 批量执行命令
网络耗时是redis的性能瓶颈，内存操作非常快微妙级别的，网络操作就比较慢了ms级别的


### Redis连接池
Redis连接池，搞多个针对redis的链接

```config
## 最大等待获取连接的时间 通常不会超过1s
maxWaitMillis=
## 资源耗尽 是否立即失败 ，当false时，maxWaitMillis才会起作用
blockWhenExhausted=false
```

### Redis持久化

RDB和AOF Rewrite的持久化机制不要自动处理，而是放到半夜，系统负载低的时候再跑


### Linux 内存参数

```conf
vm.overcommit_memory=1
vm.swappiness=1
ulimit -Sn 
```

### Redis 性能问题
[一文讲透如何排查 Redis 性能问题！](https://heapdump.cn/article/3523071)

### Redis MONITOR命令 排查redis的性能
https://www.ipcpu.com/2021/07/redis-monitor-3/#:~:text=Redis%E4%B8%ADMONITOR%E5%91%BD%E4%BB%A4%E7%94%A8,%E8%BF%94%E5%9B%9E%E5%80%BC%E6%80%BB%E6%98%AFOK%E3%80%82

https://pdai.tech/md/db/nosql-redis/db-redis-y-monitor.html

[官方文档](https://redis.io/commands/monitor/)

搭配[redis-faina](https://github.com/facebookarchive/redis-faina)分析日志


数据样例：
```shell
1709621398.306134 [1 172.18.70.172:55316] "GET" "NOTIFICATION_IMG"
1709621398.306397 [1 172.18.70.179:46196] "HEXISTS" "nginx_log" "\x04>\x1cotJL05wjIShlwogRpcyfMkn_dllo"
1709621398.306415 [1 172.18.70.170:50418] "GET" "LOGIN:SALT:extension"
1709621398.307246 [1 172.18.70.172:55790] "GET" "USER:63f7lB8I7Off2KSN98rE2MZO"
```

其中第一个值为


# EOF