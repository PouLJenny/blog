---
layout: post
title:  "tomcat请求url过长报400"
date:   2023-05-31 11:08:06 +0800
categories: tomcat
tags: tomcat
permalink: /tomcat/tomcat-url-too-long
published: true
publish_file: 2023-05-31-tomcat-tomcat-url-too-long.md
toc: true
---
# tomcat请求url过长报400

tomcat版本 `8.0.49`

出现的问题就是GET请求参数特别长，大概有1万个字符，请求的时候出现了HTTP 400的状态码

查了下`tomcat`的源码和官方文档发现了问题所在
1. HTTP url后面的参数是放在请求头里面的
2. `tomcat` 的 `http connector` 有个限制参数 `maxHttpHeaderSize` : `Provides the default value for maxHttpRequestHeaderSize and maxHttpResponseHeaderSize. If not specified, this attribute is set to 8192 (8 KB).`

```java
public abstract class AbstractHttp11Protocol<S> extends AbstractProtocol<S> {
    ...

    /**
     * Maximum size of the HTTP message header.
     */
    private int maxHttpHeaderSize = 8 * 1024;
    public int getMaxHttpHeaderSize() { return maxHttpHeaderSize; }
    public void setMaxHttpHeaderSize(int valueI) { maxHttpHeaderSize = valueI; }
    ...
}
```
3. `tomcat` 源码中有个类 `AbstractInputBuffer` 中存储header的有个字节数组 `protected byte[] buf;` 这个参数每次解析http请求都会按照配置的 `maxHttpHeaderSize` + `socketReadBufferSize` 直接初始化数组长度，并申请内存。
然后一行一行去解析http的请求头，每行数据都缓存到`buf`字段里。
所以这个值不能太大，不建议调整这个参数。比较合理的方案就是业务上限制输入参数的字符长度，超过长度限制则不请求后端接口。如果业务上就是需要这么长的参数，建议转成`POST + FORM`请求

```java
public abstract class AbstractInputBuffer<S> implements InputBuffer{
    ...
    /**
     * Pointer to the current read buffer.
     */
    protected byte[] buf;
```

4. `socketReadBufferSize` 这个参数，先读取配置 `socket.appReadBufSize`:`(int)Each connection that is opened up in Tomcat get associated with a read ByteBuffer. This attribute controls the size of this buffer. By default this read buffer is sized at 8192 bytes. For lower concurrency, you can increase this to buffer more data. For an extreme amount of keep alive connections, decrease this number or increase your heap size.`  如果没有的情况下后读取配置 ,`socket.rxBufSize` :`(int)The socket receive buffer (SO_RCVBUF) size in bytes. JVM default used if not set.`

```java
/**
 * Implementation of InputBuffer which provides HTTP request header parsing as
 * well as transfer decoding.
 */
public class InternalNioInputBuffer extends AbstractNioInputBuffer<NioChannel> {

    @Override
    protected void init(SocketWrapper<NioChannel> socketWrapper,
            AbstractEndpoint<NioChannel> endpoint) throws IOException {

        socket = socketWrapper.getSocket();
        if (socket == null) {
            // Socket has been closed in another thread
            throw new IOException(sm.getString("iib.socketClosed"));
        }
        socketReadBufferSize =
            socket.getBufHandler().getReadBuffer().capacity();

        int bufLength = headerBufferSize + socketReadBufferSize;
        if (buf == null || buf.length < bufLength) {
            buf = new byte[bufLength];
        }

        pool = ((NioEndpoint)endpoint).getSelectorPool();
    }
```

5. `SO_RCVBUF` 此参数控制的是操作系统层面每个TCP socket在内核中的接受缓冲区大小