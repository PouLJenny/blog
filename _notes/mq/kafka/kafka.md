# Kafka

## 简介

[官网](https://kafka.apache.org/ '')
[github](https://github.com/apache/kafka '')
[官方文档](https://kafka.apache.org/27/documentation.html '')

## 常用命令

kafka常用管理命令  https://www.cnblogs.com/wangzhuxing/p/10127497.html#_label0_3
kafka的分区策略    https://www.iteblog.com/archives/2209.html

- 查询所有的topic
`./kafka-topics.sh --bootstrap-server localhost:9091,localhost:9092,localhost:9093 --list`
- 创建topic
`./kafka-topics.sh --create --topic access-log --bootstrap-server localhost:9091,localhost:9092,localhost:9093`
- 查询topic的详细信息
`./kafka-topics.sh --bootstrap-server localhost:9091 --topic access-log --describe`
- 启动生产者
`./kafka-console-producer.sh --bootstrap-server  localhost:9091,localhost:9092,localhost:9093 --topic cache-message`
- 启动消费者
`./kafka-console-consumer.sh --bootstrap-server localhost:9091,localhost:9092,localhost:9093 --topic access-log --from-beginning`


## 原理

### KRaft
- 2.8 KRaft mode was released in early access.
- 3.0 it was in preview.
- 3.3 Mark KRaft as production-ready for new clusters, [Production-Ready](https://cwiki.apache.org/confluence/display/KAFKA/KIP-833%3A+Mark+KRaft+as+Production+Ready )
- 3.4 Migration from ZK mode supported as Early Access (EA)

### 低延迟、高吞吐

先写入os cache，然后顺序写入文件

### Kafka的零拷贝是怎么回事？
kafka消费端消费数据的时候，位于磁盘文件中的消息，是直接通过linux的`sendfile()`系统调用，把文件中的数据直接发送到网卡中去，省去了磁盘到内核态，然后内核态再到用户态，然后再从用户态到socket

### 消息存储格式

### partition和多副本冗余

### ISR列表机制 保证消息不丢失

### 基于Zookeeper实现无状态的可伸缩架构
维护集群的元数据，维护结点的上线，下线，故障转移

### LEO （ Log end Offset） ，HW 高水位


### JMX指标