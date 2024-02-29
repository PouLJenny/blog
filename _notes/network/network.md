# Computer Networks


## Data Link Layer

1. Providing a well-defined service interface to the network layer.
2. Dealing with transmission errors.
3. Regulating the flow of data so that slow receivers are not swamped by fast senders.


## Network Layer

### IPV4数据报

1. 版本 4位 固定4 也就是 0100
1. Intenet头部长度 IHL 4位 表示IPV4头部中32位字的数量 最大支持 $(2^4 - 1) \times 4 = 60$个字节
1. 服务类型 ToS 8位 最初由[RFC0791]指定的,由于从来没有被广泛使用，因此最终被拆分成两个字段，由一组RFC([RFC3260][RFC3168][RFC2474]和其它RFC)重新定义
    - 区分服务字段 DS 6位
    - 显示拥塞通知字段或指示位 ECN 
1. 总长度 16位 表示IPv4数据报的总长度 单位字节 所以IPv4数据报最大$(2^{16} - 1) = 65535$字节
1. 标识 16位
1. 标志 3位
1. 分片偏移 13位
1. 生存周期 8位
1. 协议 8位
1. 头部校验和 16位
1. 源IP地址 32位
1. 目标IP地址 32位
1. 头部选项可变长度，最多40个字节
1. IP数据 最多65515个字节

## Transport Layer


## Application Layer


## 粘包/拆包问题
其实就是TMD程序BUG，愣是给搞成了个专业名词，我真的是。。

https://www.zhihu.com/question/20210025


## 网络编程相关的书籍

1. 《UNIX网络编程》（卷一和卷二）作者：W.Richard Stevens
2. 《TCP/IP详解 卷一：协议》作者：W.Richard Stevens
3. 《TCP/IP详解 卷二：实现》作者：W.Richard Stevens
3. 《TCP/IP详解 卷三》作者：W.Richard Stevens
4. 《TCP/IP网络编程》作者：Richard Blum
5. 《网络是怎样连接的》作者：东野圭吾
6. 《深入浅出TCP/IP》作者：赵炯
7. 《计算机网络》作者：谢希仁
8. 《计算机网络：自顶向下方法》作者：James F.Kurose
9. 《UNIX网络编程实践》作者：Sean Walton