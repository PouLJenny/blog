# Rabbitmq

## AMQP 
https://www.amqp.org/
https://www.amqp.org/sites/amqp.org/files/amqp.pdf

https://zhuanlan.zhihu.com/p/147675691


## 架构

Server:又称 Broker，接受客户端的连接，实现 AMQP 实体服务，安装 rabbitmq-server

Connection:连接，应用程序与Broker的网络连接 TCP/IP 三次握手和四次挥手

Channel:网络信道，几乎所有的操作都在Channel中进行，Channel是进行消息读写的信道，客户端可以建立对各个Channel，每个Channel代表一个会话

Message：消息，服务与应用程序之间传送的数据，由Properties和body组成，properteis可以是对消息进行修饰，比如消息的优先级，延迟等高级特性，Body则是消息体的内容

Virtual Host：虚拟地址，用户逻辑隔离，最上层的消息路由，一个虚拟机可以有若干个Exchange和Queue，同一个虚拟主机里面不能有相同名字的Exchange

Exchange：交换机，接收消息，根据路由键发送消息到绑定到的队列（不具备消息存储能力）

Bindings：Exchange和Queue直接的虚拟连接，binding中可以保护多个routing key

Routing key：是一个路由规则，虚拟机可以用它来去定如何路由一个特定的消息

Queue：队列，也成为Message Queue，消息队列，保存消息并将它们转发给消费者


