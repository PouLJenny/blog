# Netty

[github](https://github.com/netty/netty )
[官网](https://netty.io/ )


## 线程池

每个线程就对应一个NioEventLoop

很多的线程，每个线程叫NioEventLoop,每个线程都会负责一部分的客户端连接的SocketChannel,对这些SocketChannel都会注册在线程自己的Selector中，
每个线程通过自己的Selector去轮询（Loop）他负责的这一批客户端连接的网络请求事件

NioEventLoop,负责轮询Nio事件的线程，轮询多个客户端连接的Nio事件

线程池的初始化，NioEventLoopGroup, cpu核心数 * 2 = 线程数量,每个线程就对应一个NioEventLoop，有一个自己的Selector,每个线程就通过Selector负责一批
SocketChannel (客户端连接)的Nio网络事件的轮询

## 
