---
layout: post
title:  "Redis RESP协议"
date:   2024-03-04 23:06:00 +0800
categories: Redis
tags: Redis
permalink: /redis/resp
published: false
publish_file: 2024-03-04-redis-resp.md
toc: true
---
# Redis RESP协议

REdis Serialization Protocol (RESP). 即所谓的Redis序列化协议

[官方文档](https://redis.io/docs/reference/protocol-spec/) 

与Redis服务端通信，Redis的客户端使用的通信协议叫RESP.虽然此协议是为redis设计的，但也可以用在其他C-S架构的项目上。

RESP在下面的场景中做了折中处理：

- 简单实现
- 快速解析
- 可读性高

RESP可以序列化不同的数据类型，包括：integers,strings,arrays。还包含错误的类型。客户端发送请求到Redis服务器使用String数组。数组包含redis命令及其参数。服务端的响应类型取决于什么命令。

RESP是二进制安全的且使用前缀的长度来传输批量数据，因此不需要处理从一个进程传输到另一个进程的批量数据。

RESP协议需要在redis客户端实现.

> Note
>
> RESP协议只用来在客户端和服务端之间通信。Redis集群使用的是其它的二进制协议进行节点间的交换数据


## RESP版本

RESP协议最先出现在Redis 1.2中，并且是可选择的。

在Redis 2.0中，发布了新的RESP版本，又称为RESP2。成为了客户端和服务端之间通信的标准。

[RESP3](https://github.com/redis/redis-specifications/tree/master/protocol)是RESP2的超集，主要为了客户端编写者的生活更轻松一点。Redis6.0 试验性、选择性的支持了RESP3的特性（不包括streaming strings 和 streaming aggregates）。另外,`HELLO`命令允许客户端链接并升级协议版本（见 [Client handshake](https://redis.io/docs/reference/protocol-spec/#client-handshake)）

到了Redis 7,RESP2和RESP3的客户端都可以执行所有的命令。服务端根据协议的版本返回不同的响应数据格式。

未来的Redis版本或许会修改默认的协议版本，但也不会完全弃用RESP2.不过，有可能未来的一些新特性只支持RESP3.

## 网络层

客户端通过与服务端创建TCP链接来通信(服务端的默认端口为6379)

虽然RESP协议在技术上并非特定于TCP，但在Redis环境中该协议专门在TCP连接上使用(或者是等效的面相流的链接，比如 Unix sockets)。

## 请求-响应 模型

Redis服务端接收命令和不同的参数。然后，服务端执行命令，并发送结果给客户端。

这是个非常简单的模型。然而，其中存在一些异常：

- Redis客户端可以通过Pipeline的方式发起请求。这种模式下客户端可以一次性发送多个命令，并等待执行结果
- 当一个RESP2连接订阅了一个 发布/订阅的通道时，协议的语义变更成了推模型。客户端不在主动发送命令，因为服务端会自动发送新的消息给客户端(订阅此通道的客户端)，尽快让客户端收到消息。
- `MONITOR`命令把连接变成了 ad-hoc push模型。这种模式的协议没有被明确规定，但解析起来显而易见。
- 








