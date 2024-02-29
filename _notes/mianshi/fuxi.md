# 复习

这个阶段需要自己思考各种异常情况，和解决方式，框架的一个处理机制

what 是什么
why  为什么
how  怎么用
where 适用什么场景，有什么优缺点

学习的时候一定要多问自己问题，为什么样这样搞。其他的搞法行不行。

(分布式)系统中的一些关键角色

1. 网关   zuul gateway    
2. 消息队列  kafka rabbit rocket
2. 配置中心 disconf ,spring cloud config
2. 注册中心 zookeeper consule 
3. RPC/服务间的通讯框架 负载均衡机制 限流/服务降级/服务隔离机制 dubbo hystrix feign ribbon sentinal 
4. 分布式事务 seata 
5. 分库分表 + 分布式ID leaf
6. 分布式锁 redis zookeeper
7. 分布式缓存 redis
8. 关系数据库 MySql Postgresql 
9. 分库分表
10. 搜索引擎 Elasticsearch Lucene
11. No-sql数据库 redis MongoDB 
12. 大数据技术栈 hadoop hbase spark clickhouse flink hdfs 数据仓库
13. 即时通信技术 WebSocket WebRTC MQTT IVR
14. 服务器容器 tomcat jetty netty
15. 网络编程 IO模型
16. 文件系统 

## 儒猿的课程学习时间表 
1. 阶段一（可以不看)    218:50:00
2. 阶段二   181:25:00
    1. Spring Cloud Nefflix     90:54
    1. 分布式事务   42:38
    1. 分布式锁     16:28
    1. 分布式架构实战   31:22
3. 阶段三   45:08:00
4. 阶段四   13:53:00
5. 阶段五   26:23:00
6. 阶段六   03:26:00
7. 阶段七   46:27:00
8. 阶段八   69:19:00
9. 阶段九   111:41:00
10. 阶段十  61:05:00
11. 阶段十一 选修课
    1. ES   43:12:00
    2. 亿级流量     59:15:00
    3. 面试突击     11:22:00
    4. 幂等一致性   03:15:00
    5. 数据库缓存双写一致性     01:35:00
    6. 跳槽训练营   62:20:00
    7. Seata分布式事务  02:11:00
    8. Nacos    08:07:00
    9. DDD  81:49:00
12. P7: 阶段一      235:09:00
13. P7: 阶段二      79:06:00
14. P7: 阶段三      184:08:00
15. P7: 阶段四      84:33:00
16. P7: 阶段七      68:46:00
17. 大数据:阶段一:zk        25:26:00
18. 大数据:阶段一:ES        07:19:00
18. 大数据:阶段一:kafka     38:36:14
19. [JVM专栏](https://apppukyptrl1086.pc.xiaoe-tech.com/p/t_pc/course_pc_detail/column/p_5d0ef9900e896_MyDfcJi8 )
20. [MySql专栏](https://apppukyptrl1086.pc.xiaoe-tech.com/p/t_pc/course_pc_detail/column/p_5e0c2a35dbbc9_MNDGDYba )

总计	1735.166667	小时	
总计	173.5	天	
总计	5.766666667	月	全职学得学6个月 学到P7
"这只是看视频的时间，还得自己领悟、消化，又得花时间，*2的话 那就是1年了。。。，这还是全天啥也不管就是学这玩意"	

## 儒猿推荐快速学习路径

- 数据结构和算法
    - 看一本书
- java并发编程
- 网络与IO知识体系
- Netty网络编程（可选，不一定每次面试都会问，如果简历里面没写一般也不会问）
    - 如果简历上写了，必须深入理解
- jvm原理和调优
- MySQL数据库原理优化
- （<span style="color: red">重点</span>）分布式架构： 服务注册和发现、RPC调用、<span style="color: red">分布式事务</span>、分布式锁、接口幂等性、限流熔断
    - Spring Cloud Netflix: Eureka、Feign、Ribbo、Zuul、Hystrix
    - Spring Cloud Alibaba: Dubbo（需要源码级别）、Sentinel、Seata、Nacos

- 微服务技术体系： 日志、监控、链路、配置、治理、开发、测试、上线、部署的流程和规范，项目管理流程和规范，代码质量规范和code review是怎么来做的，可能会辅助性的问道

- 中间件问的浅的话就是一些原理，深的话要到源码级别

- RocketMQ、Kafka、RabbitMQ
- redis
- 分库分表和ShardingSphere
- Elasticsearch

<span style="color: red">源码级别的深入必须得下一番苦功夫</span>


现在面试一般都是**死扣项目**


需要理解我的业务流程、模块、技术架构、生产如何来进行部署，线上生产他的各种数据。

开拓思路，你的项目未来要是遇到了xx问题之后，你会如何来考虑，如何来设计，如何来优化，如果你的系统未来的并发量，数据量，遇到了**10倍 100倍 1000倍**的扩张，你觉得你的系统架构可能会出现哪些瓶颈，应该如何来重构设计架构，让系统可以扛住更大规模的体量。

一个工程师，技术广度和深度是肯定要有的，各种技术核心原理，深度对部分技术要有源码级别的一个研究，项目经验，拷问出来你入职以后，凭借你的技术和项目能力，可以hold住我们公司里什么样的项目和开发任务

P6+和P7以上的，还会问道系统设计、架构设计、架构演进、如何一步一步来进行演进，系统设计问题，设计12306售票系统，设计双11大促系统，你会如何考虑，分析业务流程，实际高并发场景之下，会有哪些瓶颈和问题，如何来设计。



DDD可以是一个很大的亮点，

rocketmq，rocketmq的整体原理和设计

千万级用户量的营销push项目案例，基于rocketmq构建和开发的营销push案例，千万级用户量场景来设计，自己的业务里是否可能会存在一些针对C端或者是B端用户的push推送的场景，b端项目，b端项目也可以是saas，几十万级别，百万级别，不一定说是千万级

大量的运用rocketmq

简历的badcase 流水帐。STAR模型+数字化

完全不建议把你素有的项目的流水账写出来。

S situation 面临的场景
T task 要解决的问题
A action 采用的行动
R result 拿到的结果


### bad case
- 自我介绍千万不要流水账，建议分两步
    1. 最近23个重点项目按照STAR模型，简单的讲讲、自己设计的方案和取得的成果，数字亮出来
    2. 自己阅读过的源码


把我的es那个改进一下，队列改到mq中去




