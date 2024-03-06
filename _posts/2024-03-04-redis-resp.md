---
layout: post
title:  "Redis RESP协议"
date:   2024-03-04 23:06:00 +0800
categories: Redis
tags: Redis
permalink: /redis/resp
published: true
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

这是个非常简单的模型。然而，其中存在一些例外：

- Redis客户端可以通过Pipeline的方式发起请求。这种模式下客户端可以一次性发送多个命令，并等待执行结果
- 当一个RESP2连接订阅了一个 发布/订阅的通道时，协议的语义变更成了推模型。客户端不在主动发送命令，因为服务端会自动发送新的消息给客户端(订阅此通道的客户端)，尽快让客户端收到消息。
- `MONITOR`命令把连接变成了 ad-hoc push模型。这种模式的协议没有被明确规定，但解析起来显而易见。
- [Protected mode](https://redis.io/docs/management/security/#protected-mode).从非回环网络地址建立的连接，如果尝试进入保护模式会被拒绝并被服务端关闭此链接。关闭连接之前，服务端会无条件的发送`-DENIED`数据给客户端，不管客户端有没有写入socket数据。
- [RESP3 Push type](https://redis.io/docs/reference/protocol-spec/#resp3-pushes).看名字可以知道，推送类型允许服务端发送out-of-band数据到连接上。服务端可能在任意时间推送数据，但是数据不一定关联到客户端端发送的执行命令。
  
除了上面所说的例外情况，Redis协议总体上说是一个简单的请求-响应模式。

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

### Simple strings

简单字符串，以编码的字符`+`，跟着的是字符串。后面的字符串**不能**包含`\r`或`\n`字符，因为`\r\n`字符是终结字符。

简单字符串可以传送短的、非二进制的字符，相对来说比较轻量。比如，大多数的Redis命令执行成功后返回给客户端的数据就只是个"OK"。用下面的5个字节即可表示:

```
+OK\r\n
```

当Redis服务端返回简单字符串时，客户端的解析库需要返回`+`（不包含）后面的所有字符,直到CRLF(不包含)

如果想发送二进制数据，请参考 bulk strings.

### Simple errors

RESP支持异常的错误类型数据。Simple errors，或者是simply just errors。跟simple strings差不多，但是它的第一个字符是`-`。Simple strings和errors之间的差别就是客户端需要把errors数据看作是异常，具体的异常类型是`-`后面的字符数据。

基本的格式如下：

```
-Error message\r\n
```

当出现一些错误的时候Redis服务端会返回error数据。比如，命令和实际的数据类型不匹配，亦或是命令不存在。客户端收到error数据的时候需要把错误抛出来。

下面是一些错误的数据例子：

```
-ERR unknown command 'asdf'
-WRONGTYPE Operation against a key holding the wrong kind of value
```

`-`后面的大写字符，直到空格字符或者是新的行，代表了返回的具体的错误类型。被称为**错误前缀**(*error prefix*).请注意，错误前缀是 Redis 使用的一种约定，而不是 RESP 错误类型的一部分

比如，在Redis中，`ERR`是比较宽泛的错误，然而`WRONGTYPE`则更具体一点，指明了是客户端发起的命令跟实际的数据类型不匹配。错误前缀允许客户端在没有读取详细的错误信息的时候，就能知道是什么类型的错误。

具体的客户端在实现的时候可以针对不同的错误响应返回不同的错误形式，或者是提供一个比较宽泛的形式，只把错误的名字返回给客户端的调用者。

但是这种特性必须要特别重视，因为它很少被用到。而且，一些简单的客户端实现的时候可能仅仅返回一个错误的值，比如 `false`


### Integers

此类型是CRLF结尾的字符数据，代表了有符号的、10进制的、64位整形数字。

RESP编码整形数字为下面的形式：

```
:[<+|->]<value>\r\n
```

- 第一个字节是`:`
- 可选的`+`和`-`符号，分别表示为正数和负数
- 一个或多个数字(0..9)
- CRLF结尾符

比如，`:0\r\n`和`:1000\r\n`分别代表0和1000.

很多Redis命令都会返回RESP的整形数字，包括 `INCR`,`LLEN`,和`LASTSAVE`。整形数字，只有在具体的命令上下文中才有意义。比如`INCR`返回增长的值,`LASTSAVE`返回UNIX时间戳.然而，返回的数组必须保证在有符号的64位可表示的范围内。

有些情况，数字可以表示true或者false。比如,`SISMEMBER`返回1为true，0为false。

其它的命令，包括`SADD`,`SREM`和`SETNX`,返回1表示数据变更了，0则表示其它情况。

### Bulk strings

Bulk strings表示二进制的字符串.字符串可以是任意大小，但是默认情况，Redis限制大小为512MB（见proto-max-bulk-len配置）

RESP把bulk string编码如下:

```
$<lenght>\r\n<data>\r\n
```

- 第一个字节为`$`
- 一个或多个数字(0..9)表示字符串的长度，单位是字节,数字是无符号，10进制的
- CRLF分隔符
- 数据
- CRLF结尾符

下面是“hello”字符串的编码：

```
$5\r\nhello\r\n
```

空字符的编码如下:

```
$0\r\n\r\n
```

#### Null bulk strings

RESP3可以直接表示null，RESP2则没有这种类型。历史原因RESP2通过bulk strings和arrays类型来表示。

null bulk string代表不存在的值。`GET`命令如果key不存在的时候，会返回Null Bulk String

编码如下:

```
$-1\r\n
```

Redis客户端收到null bulk string时，相比于返回空字符串，最好是返回`nil`对象。比如，Ruby库会返回`nil`,C库则会返回`NULL`（或者是在返回的对象中指定特殊的标识）。

### Arrays

客户端通过RESP arrays格式发送命令给Redis服务端。同样的，一些Redis命令使用arrays返回元素的集合。比如 `LRANGE`命令.

RESP Arrays 的编码如下：

```
*<number-of-elements>\r\n<element-1>...<element-n>
```


- 第一个字节为`*`
- 一个或多个10进制数字(0..9)表示元素的个数。
- CRLF分隔符
- 每个元素都是一种RESP类型

空数组表示为下：

```
*0\r\n
```

下面是两个bulk string的数组编码 "hell"和"world"：

```
*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n
```

下面是三个数字组成的数组编码:

```
*3\r\n:1\r\n:2\r\n:3\r\n
```

数组中的元素类型可以是混合的，下面是4个数字加一个bulk string组成的数组:

```
*5\r\n
:1\r\n
:2\r\n
:3\r\n
:4\r\n
$5\r\n
hello\r\n
```
(上面本身是不存在换行的，只是为了方便阅读)

所有的aggragate RESP数据类型都支持嵌套。比如，下面是两个数组元素组成的一个数组的编码：

```
*2\r\n
*3\r\n
:1\r\n
:2\r\n
:3\r\n
*2\r\n
+Hello\r\n
-World\r\n
```
(上面本身是不存在换行的，只是为了方便阅读)

上面的编码中数组有两个元素。第一个元素也是一个数组，包含了三个数字（1，2，3）。第二个数组包含了两个元素，一个simple string和一个simple error.

> **Multi bulk reply**
>
> 在有些地方，RESP数组被认为是 *multi bulk*。这俩是一样的。

#### Null arrays

RESP3可以直接表示null，RESP2则没有这种类型。历史原因RESP2通过bulk strings和arrays类型来表示。

null arrays代表不存在的数组。比如，当`BLPOP`命令超时时，它会返回一个null array.

null array编码如下：

```
*-1\r\n
```

当Redis返回null array时，客户端应该返回null对象，而不是空数组。


#### Null elements in arrays

数组中可能会有null，用null bulk string表示。比如，`SORT`命令，`GET pattern`命令，指定的key不存在的时候.

下面是一个示例编码：

```
*3\r\n
$5\r\n
hello\r\n
$-1\r\n
$5\r\n
world\r\n
```
(上面本身是不存在换行的，只是为了方便阅读)

上面的第二个元素是null。客户端库解析的时候应该返回下面这种数据：

```
["hell",nil,"world"]
```

### Nulls

null代表不存在的数据。

下面是编码：

```
_\r\n
```

- 第一个字节是`_`
- CRLF结尾

> **Null Bulk String,Null Arrays and Nulls**
> 
> 由于历史原因，RESP2 特性包含了两个专门设计的值，用于表示批量字符串和数组的空值。这种二元性一直是一种冗余，对协议本身没有添加任何语义值
> 
> RESP3中的null类型，解决了这个问题。

### Booleans

编码如下：

```
#<t|f>\r\n
```

- 第一个字节是`#`
- `t`代表true，`f`代表false
- CRLF结尾符

### Doubles

双精度浮点型，编码如下：

```
,[<+|->]<integral>[.<fractional>][<E|e>[sign]<exponent>]\r\n
```

- 第一个字节是`,`
- 可选的`+`和`-`符号，分别表示为正数和负数
- 一个或多个数字(0..9)
- 可选字符`.`，跟着一个或多个数字(0..9)，表示小数值
- 可选的字符`E`或`e`,跟着可选的`+`和`-`符号，分别表示为正指数和负指数，一个或多个数字(0..9)结尾表示指数
- CRLF结尾符

下面是数字1.23的编码：

```
,1.23\r\n
```

由于小数部分不是必须的，数字10可以编码成两种形式：

```
:10\r\n
,10\r\n
```

上面的示例中，客户端需要分别解析成整形数字，和浮点数。

正无穷、负无穷、NaN分别表示为

```
,inf\r\n
,-inf\r\n
,nan\r\n
```


### Big numbers

可以编码超过64位符号数的表示范围的数字.

编码格式如下：

```
([+|-]<number>\r\n
```

- 第一个字节是`(`
- 可选的`+`和`-`符号，分别表示为正数和负数
- 一个或多个数字(0..9)
- CRLF结尾符

示例：

```
(3492890328409238509324850943850943825024385\r\n
```

大数可以是正数也可以是负数，但是不能有小数。客户端的解析库应该解析成大数对象。如果编程语言不支持的话。客户端应该返回string类型，并且尽可能的说明这是一个大数。

### Bulk errors

这种类型结合了简单错误的目的和批量字符串的表现力

编码为：

```
!<length>\r\n<error>\r\n
```

- 第一个字节为`!`
- 一个或多个数字(0..9)，表示错误的长度，单位字节
- CRLF分隔符
- 错误
- CRLF结尾符

作为一种惯例，错误以大写字母开头（以空格分隔的）单词开始，传达错误消息。

例如，错误"SYNTAX invalid syntax",编码如下:

```
!21\r\n
SYNTAX invalid syntax\r\n
```
(上面本身是不存在换行的，只是为了方便阅读)

### Verbatim strings

跟bulk string相似,此外，还提供了关于数据编码的提示。

编码如下：

```
=<length>\r\n<encoding>:<data>\r\n
```

- 第一个字节是`=`
- 一个或多个数字(0..9)，表示字符串的总长度，单位字节
- CRLF分隔符
- 3个字节表示数据的编码方式
- `:`后面为数据部分
- 数据部分
- CRLF结尾符

示例：

```
=15\r\n
txt:Some string\r\n
```
(上面本身是不存在换行的，只是为了方便阅读)

一些客户端库可能会忽略此类型和字符串类型之间的差异，并在两种情况下返回本机字符串。然而，交互式客户端，比如命令行界面（例如 redis-cli），可以使用此类型，并且知道它们的输出应该按原样呈现给用户，且不用引号引用字符串。

例如，Redis 命令 INFO 输出一个包含换行符的报告。当使用 RESP3 时，redis-cli 正确显示它，因为它被发送为Verbatim String（其三个字节为“txt”）。然而，当使用 RESP2 时，redis-cli 是硬编码的，以确保对 INFO 命令的正确显示给用户。

### Maps

RESP map编码为键值对的集合，或者是字典、哈希表

编码如下：

```
%<number-of-entries>\r\n<key-1><value-1>...<key-n><value-n>
```
- 第一个字节是`%`
- 一个或多个数字(0..9)，表示键值对的数量
- CRLF分隔符
- 每个键值对都是两个RESP类型

例如下面是json的数据格式

```json
{
    "first": 1,
    "second": 2
}
```

编码成RESP时为：

```
%2\r\n
+first\r\n
:1\r\n
+second\r\n
:2\r\n
```
(上面本身是不存在换行的，只是为了方便阅读)

Redis 客户端应该返回其所在语言提供的惯用字典类型。然而，低级编程语言（例如 C）可能会返回一个数组，以及指示给调用者它是一个字典的类型信息。

> **Map pattern in RESP2**
>
> RESP2 没有显式的map类型。在 RESP2 中，map被表示为一个扁平的数组，其中包含键和对应的值。第一个元素是一个键，后跟相应的值，然后是下一个键，以此类推，就像这样：key1, value1, key2, value2, ....

### Sets

Sets跟Arrays比较像，不过不是按顺序的且元素都是唯一的

编码如下：

```
~<number-of-elements>\r\n<element-1>...<element-n>
```

- 第一个字节是`~`
- 一个或多个数字(0..9)，表示元素的数量
- CRLF分隔符
- 每个元素都是RESP数据类型

客户端应该返回其编程语言中提供的原生集合类型，如果该类型可用的话。另外，在没有原生集合类型的情况下，可以使用数组，同时附带类型信息（例如在 C 中）。

### Pushes
RESP 的推送包含带外(out-of-band)数据。它们是协议请求-响应模型的例外，并为连接提供了一种通用的推送模式。

推送事件编码跟arrays差不多，只有第一个字节不同:

```
><number-of-elements>\r\n<element-1>...<element-n>
```

- `>`为第一个字节
- 一个或多个数字(0..9)，表示元素的数量
- CRLF分隔符
- 每个元素都是RESP数据类型

推送的数据可能出现在 RESP 的任何数据类型之前或之后，但绝不会出现在其中。这意味着客户端不会在映射回复中找到推送数据。这也意味着推送的数据可能出现在命令的回复之前或之后，也可能单独出现（不调用任何命令）。

客户端应通过调用实现推送数据处理的回调来对推送做出反应。

### Client handshake

新的RESP连接需要发送`HELLO`命令来创建会话。这种做法有两个目的：

1. 它允许服务器与 RESP2 版本向后兼容。在 Redis 中，这是为了使协议转换到第3版更加平滑
1. `HELLO` 命令返回有关服务器和协议的信息，客户端可以用于不同的目标。

`HELLO`命令的格式如下：

```
HELLO <protocol-version> [optional-arguments]
```

第一个参数是协议的版本号。默认情况，连接使用的是RESP2.如果指定的连接版本服务端不支持，会返回`-NOPROTO`的错误.比如：

```
Client: HELLO 4
Server: -NOPROTO sorry, this protocol version is not supported.
```

同时，客户端会使用较低的协议版本进行重试。

同样的，客户端可以方便地知道服务端只支持RESP2:

```
Client: HELLO 3
Server: -ERR unknown command 'HELLO'
```

随后客户端可以直接使用RESP2跟服务端通信.

请注意，即使协议的版本得到支持，`HELLO` 命令可能会返回错误，不执行任何操作，并保持 RESP2 模式。例如，当在命令的可选 `AUTH` 子句中使用无效的身份验证凭据时。

```
Client: HELLO 3 AUTH default mypassword
Server: -ERR invalid password
(the connection remains in RESP2 mode)
```

`HELLO`命令成功的响应是一个map。
回复中的信息在某种程度上取决于服务器，但对所有 RESP3 实现来说，某些字段是必需的：

- **server**: "redis"(或者是其他的软件名称)
- **version**: 服务器的版本
- **proto**: RESP最高支持的版本

在Redis RESP3的实现中，还会发送以下字段：

- **id**: 连接的唯一标识
- **mode**: "standalone", "sentinel" or "cluster".
- **role**: "master" or "replica".
- **modules**: 返回Array of Bulk Strings表示加载的模块集合

### Sending commands to a Redis server

现在你已经熟悉了 RESP 序列化格式，你可以用它来帮助编写一个 Redis 客户端库。我们可以进一步指定客户端和服务器之间的交互方式：

- 客户端向 Redis 服务器发送一个只包含批量字符串的数组。
- Redis 服务器回复客户端时，发送任何有效的 RESP 数据类型作为回复。

例如，一个典型的交互过程可能如下所示

客户端发送命令 `LLEN mylist` 来获取存储在键 *mylist* 中列表的长度。然后服务器回复一个整数回复，如下例所示（C: 代表客户端，S: 代表服务器）。

```
C: *2\r\n
C: $4\r\n
C: LLEN\r\n
C: $6\r\n
C: mylist\r\n

S: :48293\r\n
```

像往常一样，为了简化起见，我们使用换行符分隔协议的不同部分，但实际的交互是客户端将 `*2\r\n$4\r\nLLEN\r\n$6\r\nmylist\r\n` 作为一个整体发送。

### Multiple commands and pipelining

客户端可以使用相同的连接来发出多个命令。支持流水线处理，因此客户端可以通过单个写操作发送多个命令。客户端可以跳过读取回复并继续一次又一次地发送命令。所有的回复都可以在最后读取。

有关更多信息，请参阅 [Pipelining](https://redis.io/topics/pipelining).

### Inline commands

有时您可能需要向 Redis 服务器发送命令，但只能使用 telnet。尽管 Redis 协议易于实现，但不太适合交互式会话，并且 redis-cli 可能并不总是可用。因此，Redis 还接受以内联命令格式发送的命令。

以下示例演示了使用内联命令进行服务器/客户端交换的情况（服务器对话以 S: 开头，客户端对话以 C: 开头）：

```
C: PING
S: +PONG
```


下面是另一个例子:

```
C: EXISTS somekey
S: :0
```

基本上，要发出内联命令，您在 telnet 会话中写入以空格分隔的参数。由于没有命令以 * 开头（RESP 数组的标识字节），Redis 检测到此条件并解析您的命令内联。

### High-performance parser for the Redis protocol

虽然 Redis 协议易于阅读且易于实现，但其实现的性能可能类似于二进制协议。

RESP 使用前缀长度来传输批量数据。这使得扫描载荷以查找特殊字符是不必要的（与解析 JSON 不同，例如）。出于同样的原因，引用和转义载荷也是不需要的。

读取聚合类型的长度（例如，批量字符串或数组）可以使用代码来处理，该代码在同时扫描 CR 字符时执行每个字符的单个操作。

示例（C语言）

```c
#include <stdio.h>

int main(void) {
    unsigned char *p = "$123\r\n";
    int len = 0;

    p++;
    while(*p != '\r') {
        len = (len*10)+(*p - '0');
        p++;
    }

    /* Now p points at '\r', and the len is in bulk_len. */
    printf("%d\n", len);
    return 0;
}
```

在识别到第一个回车符（CR）后，可以将其连同后面的换行符（LF）一起跳过而无需进一步处理。然后，可以使用单个读取操作读取批量数据，而不对载荷进行任何检查。最后，剩余的回车符和换行符会被丢弃而无需额外处理。

与二进制协议性能相当的同时，Redis 协议在大多数高级语言中实现起来明显更简单，减少了客户端软件中的错误数量。


