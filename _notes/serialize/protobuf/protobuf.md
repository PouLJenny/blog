# Google Protocol Buffers

## 简介




类似Json、XML的一种序列化方式，

[官网]('https://developers.google.com/protocol-buffers' '')

[Github]('https://github.com/protocolbuffers/protobuf' '')

## 性能对比

### 序列化响应时间对比

![序列化响应时间对比](../../static/images/protobuf/protobuf_bench_latency.png "")

### 序列化bytes对比

![序列化bytes对比](../../static/images/protobuf/protobuf_bench_bytes.png "")


## 安装protoc

### mac
mac可以直接通过brew安装 `brew install protobuf`

### binary
直接去[github](https://github.com/protocolbuffers/protobuf/releases '')下载编译好的可执行文件,解压即可

### 源码安装
protoc是用c++写的，懂c++的可以直接用[github](https://github.com/protocolbuffers '')源码安装


## 改进

由于protobuf在使用的时候需要通过`.proto`文件来生成相关语言的代码非常的不方便。所以有个哥们就写了个轮子[protostaff](https://dyuproject.com/ '')来做这个事，
[源码](https://gitlab.com/dyu/protostuffdb '')

_Waiting..._