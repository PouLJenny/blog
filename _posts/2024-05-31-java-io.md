---
layout: post
title:  "java中的IO模型"
date:   2024-05-31 18:00:00 +0800
categories: java
tags: java
permalink: /java/io
published: true
publish_file: 2024-05-31-java-io.md
toc: true
---
# IO

所谓的 I/O 就是计算机内存与外部设备之间拷贝数据的过程

我们知道 CPU 访问内存的速度远远高于外部设备，因此 CPU 是先把外部设备的数据读到内存里，然后再进行处理。请考虑一下这个场景，当你的程序通过 CPU 向外部设备发出一个读指令时，数据从外部设备拷贝到内存往往需要一段时间，这个时候 CPU 没事干了，你的程序是主动把 CPU 让给别人？还是让 CPU 不停地查：数据到了吗，数据到了吗……

这就是 I/O 模型要解决的问题

## I/O模型

一个输入操作通常包含两个不同的阶段：
1. 等待数据准备好
2. 从内核向进程复制数据
对于一个套接字上的输入操作，第一步通常涉及等待数据从网络中到达。当所等待分组到达时，它被复制到内核中的某个缓冲区。第二步就是把数据从内核缓冲区复制到进程缓冲区。


Unix下的5种I/O模型
- **阻塞式IO** blocking I/O
- **非阻塞式IO** nonblocking I/O
- **IO多路复用** I/O multiplexing (select and poll)
- **信号驱动式IO** signal driven I/O (SIGIO)
- **异步IO** asynchronous I/O (the POSIX aio_functions)

### blocking I/O
![](/assets/notes/io/blocking_io.svg)

### nonblocking I/O
![](/assets/notes/io//nonblocking_io.svg)

当一个进程像这样对一个非阻塞描述符循环调用recvfrom时，我们称之为轮询（polling）.应用进程持续轮询内核。以查看某个操作是否就绪。这么做往往耗费大量CPU时间，不过这种模型偶尔也会遇到，通常是在专门提供某一种功能的系统中才有。

### I/O multiplexing
![](/assets/notes/io//IO_Multiplexing.svg)

### signal driven I/O

![](/assets/notes/io//signal_io.svg)

### asynchronous I/O 

![](/assets/notes/io//asynchronous_io.svg)


POSIX中有两个名词，其定义为：
1. 同步I/O操作 (synchronous I/O operation) 导致请求进程阻塞，直到I/O操作完成
2. 异步I/O操作 (asynchronous I/O operation) 不导致请求阻塞

根据上面的定义，我们的前4种I/O模型（blocking io,nonblocking io,io multiplexing,signal io）都是同步I/O操作,因为真正的IO操作`recvfrom`都会阻塞进程，只有异步I/O模型跟POSIX定义的异步I/O匹配

![](/assets/notes/io//io_diff.svg)


## I/O多路复用

### select/pselect
```c
#include <sys/select.h>

/**
返回值跟poll一样
*/
int select(int nfds, 
    fd_set *restrict readfds,
    fd_set *restrict writefds, 
    fd_set *restrict errorfds,
    struct timeval *restrict timeout);
```
### poll
起源于UNIX System 3
```c
#include <poll.h>
/**
*return value,
*A positive value indicates the total number of pollfd structures that have selected events (that is, those for which the revents  member  is  non-zero).  
*A value of 0 indicates that the call timed out and no file descriptors have been selected. Upon failure, poll() shall return -1 and set errno to indicate the error.
*/
int poll(struct pollfd fds[], nfds_t nfds, int timeout);
```



从当今的可移植性角度考虑，支持select的系统比支持poll的系统要多。
### epoll
epoll API 是Linux系统专有的，在 2.6 版中新增
```c
#include <epoll.h>

int epoll_create(int size); // 创建了一个新的epoll实例

int epoll_ctl(int epfd,int op,int fd,struct epoll_event *ev); // 修改epoll的兴趣列表

int epoll_wait(int epfd,struct epoll_event *evlist,int maxevents,int timeout); // 等待有IO发生
```

epoll 的性能会根据发生 I/O 事件的数量而扩展(呈线性)。因此常见的能 够高效使用 epoll API 的应用场景就是需要同时处理许多客户端的服务器:需要监视大量的文件描述符，但大部分处于空闲状态，只有少数文件描述符处于就绪态。

https://www.coonote.com/network-note/unix-epoll-fun.html


## Java中的I/O模型

### IO
最开始的基本IO模型，也叫BIO，使用的是传统的阻塞I/O模型

`java.io`包下面和`java.net`包下面
![](/assets/notes/io//java_io_package.png)

#### 文件I/O

`java.io.FileInputStream#readBytes`
文件读 跟踪JDK源码我们能看到一段native的方法
```java
/**
 * Reads a subarray as a sequence of bytes.
 * @param b the data to be written
 * @param off the start offset in the data
 * @param len the number of bytes that are written
 * @exception IOException If an I/O error has occurred.
 */
private native int readBytes(byte b[], int off, int len) throws IOException;
```

从OPENJDK的源码中一路跟踪
`java.base/share/native/libjava/FileInputStream.c`
```c++
JNIEXPORT jint JNICALL
Java_java_io_FileInputStream_readBytes(JNIEnv *env, jobject this,
        jbyteArray bytes, jint off, jint len) {
    return readBytes(env, this, bytes, off, len, fis_fd);
}
```

`java.base/share/native/libjava/io_util.c`
```c++
jint
readBytes(JNIEnv *env, jobject this, jbyteArray bytes,
          jint off, jint len, jfieldID fid)
{
    jint nread;
    char stackBuf[BUF_SIZE];
    char *buf = NULL;
    FD fd;

    if (IS_NULL(bytes)) {
        JNU_ThrowNullPointerException(env, NULL);
        return -1;
    }

    if (outOfBounds(env, off, len, bytes)) {
        JNU_ThrowByName(env, "java/lang/IndexOutOfBoundsException", NULL);
        return -1;
    }

    if (len == 0) {
        return 0;
    } else if (len > BUF_SIZE) {
        buf = malloc(len);
        if (buf == NULL) {
            JNU_ThrowOutOfMemoryError(env, NULL);
            return 0;
        }
    } else {
        buf = stackBuf;
    }

    fd = GET_FD(this, fid);
    if (fd == -1) {
        JNU_ThrowIOException(env, "Stream Closed");
        nread = -1;
    } else {
        nread = IO_Read(fd, buf, len);
        if (nread > 0) {
            (*env)->SetByteArrayRegion(env, bytes, off, nread, (jbyte *)buf);
        } else if (nread == -1) {
            JNU_ThrowIOExceptionWithLastError(env, "Read error");
        } else { /* EOF */
            nread = -1;
        }
    }

    if (buf != stackBuf) {
        free(buf);
    }
    return nread;
}
```

`java.base/windows/native/libjava/io_util_md.h`
```c++
#define IO_Read handleRead
```
`java.base/unix/native/libjava/io_util_md.c`
```c++
ssize_t
handleRead(FD fd, void *buf, jint len)
{
    ssize_t result;
    RESTARTABLE(read(fd, buf, len), result);
    return result;
}
```
到这里我们看到了unix操作系统底层其实就是调用的`systemcall`方法`read`,符合**阻塞式I/O模型**，blocking I/O

对应的文件写,调用的是unix系统是`systemcall`的函数`write`

```c++
#include <unista.h>
ssize_t read(int fd,void *buf,size_t n);
ssize_t write(int fd,const void *buf,size_t n);
```

#### 网络I/O

基础的socket编程中的
java代码示例
```java
ServerSocket serverSocket = new ServerSocket(9000);
Socket socket = serverSocket.accept(); // 阻塞住获取TCP连接
try (InputStream inputStream = socket.getInputStream();
        OutputStream outputStream = socket.getOutputStream();
        InputStreamReader reader = new InputStreamReader(inputStream);) {
    char[] buf = new char[1024 * 1024];
    int read;
    while (reader.ready()) {
        read = reader.read(buf);// socket读取数据 java.net.SocketOutputStream#SocketInputStream
        String data = new String(buf, 0, read);
        String name = data.substring(data.indexOf(" ") + 1);
        System.out.println(data);
        outputStream.write(("Hell " + name + "!").getBytes()); // socket写入数据 java.net.SocketOutputStream#SocketOutputStream
    }
    System.out.println("socket连接断开" + socket);
} catch (Exception e) {
    e.printStackTrace();
} 
```

最终能跟到源码中，socket读取数据，底层linux实际调用的是systemcall, recv
```c++
#include <sys/socket.h>

ssize_t
recv(int socket, void *buffer, size_t length, int flags);
```

socket写入数据,底层linux实际调用的是systemcall, send ， 还是Blocking I/O模型
```c++
#include <sys/socket.h>

ssize_t
send(int socket, const void *buffer, size_t length, int flags);
```



### NIO(New IO)
为了提升I/O操作的性能，JDK1.4之后引入了NIO模型
NIO相关的类在`java.nio`，`sun.nio`包下面

那么NIO优化了些什么呢？特供了些哪些特性呢？

NIO定义了四个核心组件
- **Buffers** ,which are containers for data; 相比标准的IO，数据都要自己声明一个数组来说方便了很多。
- **Charsets** , and their associated decoders and encoders,which translate between bytes and Unicode characters; 相比于标准的I/O，没有个固定的方式来传入这个参数。
- **Channels** , and their associated decoders and encoders,which translate between bytes and Unicode characters; 读写一个Channel就可以搞定。
- **Selectors and selection keys**, which together with selectable channels define a multiplexed, non-blocking I/O facility. 相比于标准的I/O模型，底层走的是阻塞式I/O模型，NIO可以走I/O多路复用模型和non-blocking I/O模型了。主要是体现在网络IO。

#### Buffers

JDK中的顶级类`java.nio.Buffer`重要逻辑 ：

```java
 // Invariants: mark <= position <= limit <= capacity
private int mark = -1;
private int position = 0;
private int limit;
private int capacity;
```

> 0 <= mark <= position <= limit <= capacity

有几个重要的方法:

- **clear** makes a buffer ready for a new sequence of channel-read or relative put operations: It sets the limit to the capacity and the position to zero.
- **flip** makes a buffer ready for a new sequence of channel-write or relative get operations: It sets the limit to the current position and then sets the position to zero. If the mark is defined then it is discarded.
- **rewind** makes a buffer ready for re-reading the data that it already contains: It leaves the limit unchanged and sets the position to zero.

Buffers are not safe for use by multiple concurrent threads. If a buffer is to be used by more than one thread then access to the buffer should be controlled by appropriate synchronization.


JDK中内置的重要的Buffer类有：
- `ByteBuffer`, 这个是最重要的,其他的基本都是基于这个来实现的
- `ShortBuffer`
- `IntBuffer`
- `LongBuffer`
- `CharBuffer`
- `FloatBuffer`
- `DoubleBuffer`

#### Charsets

JDK中的顶级类`java.nio.charset.Charset`

#### Channels

JDK中的顶级类`java.nio.channels.Channel`

#### Selectors and selection keys



#### 文件I/O
java示例
```java
RandomAccessFile randomAccessFile = new RandomAccessFile(localFilePath, "r");
FileChannel channel = randomAccessFile.getChannel();
ByteBuffer buffer = ByteBuffer.allocate(64);
int read;
while ((read = channel.read(buffer)) != -1) {
    buffer.flip();
    while (buffer.hasRemaining()) {
        System.out.print(Character.toString((char)buffer.get()));
    }

    buffer.clear();
}

randomAccessFile.close();
```

JDK底层native方法实际执行的代码
`src/java.base/unix/native/libnio/ch/FileDispatcherImpl.c`
```c++
JNIEXPORT jint JNICALL
Java_sun_nio_ch_FileDispatcherImpl_read0(JNIEnv *env, jclass clazz,
                             jobject fdo, jlong address, jint len)
{
    jint fd = fdval(env, fdo);
    void *buf = (void *)jlong_to_ptr(address);

    return convertReturnVal(env, read(fd, buf, len), JNI_TRUE);
}


JNIEXPORT jint JNICALL
Java_sun_nio_ch_FileDispatcherImpl_write0(JNIEnv *env, jclass clazz,
                              jobject fdo, jlong address, jint len)
{
    jint fd = fdval(env, fdo);
    void *buf = (void *)jlong_to_ptr(address);

    return convertReturnVal(env, write(fd, buf, len), JNI_FALSE);
}
```

特点：
1. NIO更新和读取文件的时候使用一个Channel,维护一个`FileDescriptor`即可，相反标准的I/O需要使用两个Stream，使用两个`FileDescriptor`.
2. 文件IO的Channel是`sun.nio.ch.FileChannelImpl`,此类无法使用`Selector`,底层走的还是`read`，`write`的systemcall，这个地方猜测可能是，文件访问不像网络，走blocking I/O性能就很好了

#### 网络I/O
java代码示例
```java
ByteBuffer readBuffer = ByteBuffer.allocate(1024 * 1024);
ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
serverSocketChannel.configureBlocking(false);// 非阻塞 这个地方必须得设置成false不然会报错。。
serverSocketChannel.socket().bind(new InetSocketAddress(9000),100);
Selector selector = Selector.open();// 生成一个默认的selector对象，Linux默认生成的是EpollSelectorImpl
serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);
while (true) {
    selector.select();
    Iterator<SelectionKey> keyIterator = selector.selectedKeys().iterator();
    while (keyIterator.hasNext()) {
        SelectionKey selectionKey = keyIterator.next();
        keyIterator.remove();
        SocketChannel channel = null;
        try{
            if(selectionKey.isAcceptable()){
                ServerSocketChannel serverChannel = (ServerSocketChannel) selectionKey.channel();
                channel = serverChannel.accept();
                if (channel != null) {
                    channel.configureBlocking(false);
                    channel.register(selector,SelectionKey.OP_READ);
                }
            } else if(selectionKey.isReadable()){
                channel = (SocketChannel) selectionKey.channel();
                readBuffer.clear();
                int count = channel.read(readBuffer);

                if(count > 0){
                    readBuffer.flip();
                    CharBuffer charBuffer = decoder.decode(readBuffer);
                    String request = charBuffer.toString();
                    System.out.println(request);
                    String name = request.substring(request.indexOf(" ") + 1);
                    String response = "Hello " + name + "!";
                    channel.write(encoder.encode(CharBuffer.wrap(response)));
                } else{
                    channel.close();
                }
            }
        } catch(Throwable t){
            t.printStackTrace();
            if(channel != null){
                channel.close();
            }
        }
    }
}
```

可以看到代码中还能配置`SelectableChannel`是否是阻塞的，参见下面的源码注释。
```java
/**
 * Adjusts this channel's blocking mode.
 *
 * <p> If this channel is registered with one or more selectors then an
 * attempt to place it into blocking mode will cause an {@link
 * IllegalBlockingModeException} to be thrown.
 *
 * <p> This method may be invoked at any time.  The new blocking mode will
 * only affect I/O operations that are initiated after this method returns.
 * For some implementations this may require blocking until all pending I/O
 * operations are complete.
 *
 * <p> If this method is invoked while another invocation of this method or
 * of the {@link #register(Selector, int) register} method is in progress
 * then it will first block until the other operation is complete. </p>
 *
 * @param  block  If {@code true} then this channel will be placed in
 *                blocking mode; if {@code false} then it will be placed
 *                non-blocking mode
 *
 * @return  This selectable channel
 *
 * @throws  ClosedChannelException
 *          If this channel is closed
 *
 * @throws  IllegalBlockingModeException
 *          If {@code block} is {@code true} and this channel is
 *          registered with one or more selectors
 *
 * @throws IOException
 *         If an I/O error occurs
 */
public abstract SelectableChannel configureBlocking(boolean block)
    throws IOException;
```

下面是通过跟踪JDK源码发现的
```c++
static int
configureBlocking(int fd, jboolean blocking)
{
    int flags = fcntl(fd, F_GETFL);
    int newflags = blocking ? (flags & ~O_NONBLOCK) : (flags | O_NONBLOCK);

    return (flags == newflags) ? 0 : fcntl(fd, F_SETFL, newflags);
}
```
最后实际上是执行的`fcntl`函数来把socket的模式设置为非阻塞的，这个时候socket就会走non-blocking I/O模式了. 这里需要注意一下linux或者windows系统中，**socket创建的时候默认都是阻塞的，也就是java I/O最开始的标准版本，没有给接口设置这个值，所以都是走的blocking I/O模型**


我们跟踪源码发现Linux平台下，会走epoll_wait方法
```c++
JNIEXPORT jint JNICALL
Java_sun_nio_ch_EPoll_wait(JNIEnv *env, jclass clazz, jint epfd,
                           jlong address, jint numfds, jint timeout)
{
    struct epoll_event *events = jlong_to_ptr(address);
    int res = epoll_wait(epfd, events, numfds, timeout);
    if (res < 0) {
        if (errno == EINTR) {
            return IOS_INTERRUPTED;
        } else {
            JNU_ThrowIOExceptionWithLastError(env, "epoll_wait failed");
            return IOS_THROWN;
        }
    }
    return res;
}
```
此时使用的 **I/O multiplexing**模型，这么一看，配置阻塞还是不阻塞，跟这个没关系啊，两个走的不是一个I/O模型啊？？

然后查阅相关的资料发现

一个 socket 是否设置为阻塞模式，只会影响到 `connect/accept/send/recv` 等四个 socket API 函数，不会影响到 `select/poll/epoll_wait` 函数，后三个函数的超时或者阻塞时间是由其函数自身参数控制的。

非阻塞体现主要还是在Java代码中的：一个 select处理多个客户应用进程的 I/O，如果第一个 I/O 数据没有准备好，那么就去处理第二个客户端的 I/O，依此类推，客户端之间谁的数据先准备好就先处理谁的，不存在第二个要等第一个处理完才能开始处理的情况；



### NIO.2/Asynchronous I/O/AIO
JDK 1.7 之后引入的，给I/O带来了异步的特性，还有一些FileSystem的特性

#### 文件I/O

#### 网络I/O




## 零拷贝技术

java中可以通过`sun.nio.ch.FileChannelImpl#transferTo`

## 扩展阅读
[比较好的NIO博客](https://tech.meituan.com/2016/11/04/nio.html )


## EOF