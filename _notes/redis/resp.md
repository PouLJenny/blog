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

> **Note**
>
> RESP协议只用来在客户端和服务端之间通信。Redis集群使用的是其它的二进制协议进行节点间的数据交换


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
- [Protected mode](https://redis.io/docs/management/security/#protected-mode).从非回环网络地址建立的连接，如果尝试进入保护模式会被拒绝并被服务端关闭此链接。关闭连接之前，服务端会无条件的发送`-DENIED`数据给客户端，不管客户端有没有写入socket数据。
- [RESP3 Push type](https://redis.io/docs/reference/protocol-spec/#resp3-pushes).看名字可以知道，推送类型允许服务端发送out-of-band数据到连接上。服务端可能在任意时间推送数据，但是数据不一定关联到客户端端发送的执行命令。
  
除了上面所说的异常情况，Redis协议总体上说是一个简单的请求-响应模式。

## RESP 协议描述

RESP本质上就是支持一系列数据类型的协议。RESP中，数据中的第一个字节来区分数据的类型。

Redis通常在下面几种情况使用RESP作为请求-响应协议：

- 客户端发送命令给服务端通过批量字符串数组。第一个（有时是第二个）数组元素是命令的名字。剩下的是命令的参数
- 服务端的通过RESP返回数据。返回的类型根据具体的命令和客户端的协议版本不同

RESP是一个使用标准的ASCII控制字符编码的二进制协议。比如，`A`字符被编码成65，同样的CR(`\r`),LF(`\n`)和SP(` `)分别编码成13,10,32。

`\r\n`(CRLF)是协议的分隔符。

RESP的数据可以分类成简单(simple)、批量(bulk)和聚合数据(aggregate)

简单类型的数据跟编程语言中的印刷字符相似。Booleans 和 Integers就是。

RESP字符串可以是简单的也可以是批量的。简单字符串不会包含`\r`或者`\n`字符。批量字符串可以包含任意字符，且可以代表二进制数据。注意：批量字符串可能会被客户端编码或者是解码。

聚合数据，比如Arrays、Maps，可以包含丰富的子元素和嵌套类型。

下面的表格汇总了RESP数据类型

|RESP data tpe|Minimal protocol version|Category|First byte|
|-|-|-|-|
|Simple strings|RESP2|Simple|+|
|Simple Errors|RESP2|Simple|-|
|Integers|RESP2|Simple|:|
|Bulk strings|RESP2|Aggregate|$|
|Arrays|RESP2|Aggregate|*|
|Nulls|RESP3|Simple|-|
|Booleans|RESP3|Simple|#|
|Doubles|RESP3|Simple|,|
|Big numbers|RESP3|Simple|(|
|Bulk errors|RESP3|Aggregate|!|
|Verbatim strings|RESP3|Aggregate|=|
|Maps|RESP3|Aggregate|%|
|Sets|RESP3|Aggregate|~|
|Pushes|RESP3|Aggregate|>|

## Simple strings

简单字符串，以编码的字符`+`，跟着的是字符串。后面的字符串**不能**包含`\r`或`\n`字符，因为`\r\n`字符是终结字符。

简单字符串可以传送短的、非二进制的字符，相对来说比较轻量。比如，大多数的Redis命令执行成功后返回给客户端的数据就只是个"OK"。用下面的5个字节即可表示:

```
+OK\r\n
```














