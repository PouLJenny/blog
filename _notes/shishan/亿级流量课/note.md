# 亿级流量课

## 架构方案

电商网站里，大概可以说分成两种，一种小型电商的简单架构方案-页面静态化，大型电商时一套复杂的架构

### 页面静态化

首先有个详情页面的模版，然后通过业务数据渲染，转换成静态的html页面。用户直接访问静态的html就可以了，一般这种方式适用于小网站

优点
- 此方式实现起来比较简单，

缺点
- 当商品数量非常庞大时，每次更改页面的模版，都要刷很多，很久的数据


### 大型网站电商详情页


![架构图](../../static/images/shishan/note_cache_arch1.png '架构图')


## 需要掌握的技术点

### redis架构

#### redis生产环境的启动方案

如果一般的学习课程，你就随便用redis-server启动一下redis，做一些实验，这样的话，没什么意义

要把redis作为一个系统的daemon进程去运行的，每次系统启动，redis进程一起启动

1. redis utils目录下，有个redis_init_script脚本
2. 将redis_init_script脚本拷贝到linux的/etc/init.d目录中，将redis_init_script重命名为redis_6379，6379是我们希望这个redis实例监听的端口号
3. 修改redis_6379脚本的第6行的REDISPORT，设置为相同的端口号（默认就是6379）
4. 创建两个目录：/etc/redis（存放redis的配置文件），/var/redis/6379（存放redis的持久化文件）
5. 修改redis配置文件（默认在根目录下，redis.conf），拷贝到/etc/redis目录中，修改名称为6379.conf
6. 修改redis.conf中的部分配置为生产环境
```conf
daemonize	yes							#让redis以daemon进程运行
pidfile		/var/run/redis_6379.pid 	#设置redis的pid文件位置
port		6379						#设置redis的监听端口号
dir 		/var/redis/6379				#设置持久化文件的存储位置
```
7. 启动redis，执行cd /etc/init.d, chmod 777 redis_6379，./redis_6379 start
8. 确认redis进程是否启动，ps -ef | grep redis
9. 让redis跟随系统启动自动启动
在redis_6379脚本中，最上面，加入两行注释
```conf
# chkconfig:   2345 90 10
# description:  Redis is a persistent key-value database
chkconfig redis_6379 on
```




## 问题优化
https://heapdump.cn/article/5123637
### 缓存雪崩
考虑的比较完善的一套方案，分为事前，事中，事后三个层次去思考怎么来应对缓存雪崩的场景
1. 事前解决方案

发生缓存雪崩之前，事情之前，怎么去避免redis彻底挂掉
redis本身的高可用性，复制，主从架构，操作主节点，读写，数据同步到从节点，一旦主节点挂掉，从节点跟上
双机房部署，一套redis cluster，部分机器在一个机房，另一部分机器在另外一个机房

还有一种部署方式，两套redis cluster，两套redis cluster之间做一个数据的同步，redis集群是可以搭建成树状的结构的

一旦说单个机房出了故障，至少说另外一个机房还能有些redis实例提供服务

2. 事中解决方案

redis cluster已经彻底崩溃了，已经开始大量的访问无法访问到redis了

（1）ehcache本地缓存

所做的多级缓存架构的作用上了，ehcache的缓存，应对零散的redis中数据被清除掉的现象，另外一个主要是预防redis彻底崩溃

多台机器上部署的缓存服务实例的内存中，还有一套ehcache的缓存

ehcache的缓存还能支撑一阵

（2）对redis访问的资源隔离

（3）对源服务访问的限流以及资源隔离

3. 事后解决方案

（1）redis数据可以恢复，做了备份，redis数据备份和恢复，redis重新启动起来

（2）redis数据彻底丢失了，或者数据过旧，快速缓存预热，redis重新启动起来

redis对外提供服务

缓存服务里，熔断策略，自动可以恢复，half-open，发现redis可以访问了，自动恢复了，自动就继续去访问redis了

基于hystrix的高可用服务这块技术之后，先讲解缓存服务如何设计成高可用的架构

缓存架构应对高并发下的缓存雪崩的解决方案，基于hystrix去做缓存服务的保护

要带着大家去实现的有什么东西？事前和事后不用了吧

事中，ehcache本身也做好了

基于hystrix对redis的访问进行保护，对源服务的访问进行保护，讲解hystrix的时候，也说过对源服务的访问怎么怎么进行这种高可用的保护

但是站的角度不同，源服务如果自己本身不知道什么原因出了故障，我们怎么去保护，调用商品服务的接口大量的报错、超时

限流，资源隔离，降级