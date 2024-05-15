# Message Queue/ 消息队列中间件

## 开源框架
- ActiveMQ
- RabbitMQ
- Kafka
- RocketMQ
## 功能
它具有低耦合、可靠投递、广播、流量控制、最终一致性等一系列功能，成为异步RPC的主要手段之一
- 系统解耦
- 提高系统响应时间
例如原来的一套逻辑，完成支付可能涉及先修改订单状态、计算会员积分、通知物流配送几个逻辑才能完成；通过MQ架构设计，就可将紧急重要（需要立刻响应）的业务放到该调用方法中，响应要求不高的使用消息队列，放到MQ队列中，供消费者处理。	
- 为大数据处理架构提供服务
- Java消息服务——JMS 
Java消息服务（Java MessageService，JMS）应用程序接口是一个Java平台中关于面向消息中间件（MOM）的API，用于在两个应用程序之间，或分布式系统中发送消息，进行异步通信。 
JMS中的P2P和Pub/Sub消息模式：点对点（point to point， queue）与发布订阅（publish/subscribe，topic）最初是由JMS定义的。这两种模式主要区别或解决的问题就是发送到队列的消息能否重复消费(多订阅)。
## 组成
- Broker   消息服务器，作为server提供消息核心服务
- Producer 消息生产者，业务的发起方，负责生产消息传输给broker，
- Consumer 消息消费者，业务的处理方，负责从broker获取消息并进行业务逻辑处理
- Topic    主题，发布订阅模式下的消息统一汇集地，不同生产者向topic发送消息，由MQ服务器分发到不同的订阅者，实现消息的广播
- Queue    队列，PTP模式下，特定生产者向特定queue发送消息，消费者订阅特定的queue完成指定消息的接收
- Message  消息体，根据不同通信协议定义的固定格式进行编码的数据包，来封装业务数据，实现消息的传输
## 模式分类
- PTP点对点:使用queue作为通信载体 
	消息生产者生产消息发送到queue中，然后消息消费者从queue中取出并且消费消息。 
	消息被消费以后，queue中不再存储，所以消息消费者不可能消费到已经被消费的消息。 
	Queue支持存在多个消费者，但是对一个消息而言，只会有一个消费者可以消费。
- 发布/订阅： Pub/Sub发布订阅（广播）：使用topic作为通信载体
	消息生产者（发布）将消息发布到topic中，同时有多个消息消费者（订阅）消费该消息。和点对点方式不同，发布到topic的消息会被所有订阅者消费。


## 常见问题

### 如何保证消息不丢失

### 如何保证消息的顺序性

### 怎么处理消息积压问题

### 怎么进行消息追踪


	    
## 博客&文章：
https://blog.csdn.net/wqc19920906/article/details/82193316
https://blog.csdn.net/wqc19920906/article/details/82193593
https://www.cnblogs.com/likehua/p/3999538.html  kafka
https://boilingfrog.github.io/2021/12/10/%E5%87%A0%E7%A7%8D%E5%B8%B8%E8%A7%81%E7%9A%84%E6%B6%88%E6%81%AF%E9%98%9F%E5%88%97%E7%9A%84%E5%AF%B9%E6%AF%94/
[对比各个MQ的性能](https://www.3mu.me/activemqrabbitmqkafkarocketmq-you-lie-shi-bi-jiao/)
[对比各个MQ的性能](https://blog.csdn.net/chaochao2113/article/details/127378685)