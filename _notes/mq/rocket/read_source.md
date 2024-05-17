# RocketMQ源码阅读


## 4.9.x 版本

### 源码环境准备

1. 下载源码
    ```shell
    git clone -b rocketmq-all-4.9.6 https://github.com/apache/rocketmq.git
    ```
2. 配置java 1.8的开发环境
3. idea导入项目



## 5.2.0 版本

### 源码环境准备
1. 下载源码
```shell
git clone -b rocketmq-all-5.2.0 https://github.com/apache/rocketmq.git
```
2. 配置java 1.8的开发环境
3. 编译
5.2.0版本在我本机（M2）上编译比较顺利,大大的赞
```shell
mvn -Prelease-all -DskipTests clean install -U
```
3. idea导入项目

### 源码调试

#### 一些重要的工程目录结构

- rocketmq-broker: broker的相关源码
- rocketmq-distribution: 项目发布编译的时候需要的一些默认配置什么的，而且通过上面的编译命令，最终rocketmq的发布版本会放在此模块的`target`目录下
- rocketmq-namesrv: nameserver相关的源码
- rocketmq-store: rocketmq存储相关的源码
- rocketmq-proxy: 路由、计算等功能从Broker中剥离出来。

#### 启动nameserv

在`rocketmq-namesrv`项目中，找到类`org.apache.rocketmq.namesrv.NamesrvStartup`,启动它的`main`方法.需要加上jvm启动参数`-Drocketmq.home.dir=/Users/poul/workspace/soft/rocketmq/rocketmq/distribution`, 参数值配置`rocketmq-distribution`模块的绝对路径即可

启动时也可以指定配置文件 `-c /Users/poul/workspace/soft/rocketmq/rocketmq/distribution/conf/namesrv.properties`

验证namesrv是否启动成功
~~~shell
The Name Server boot success...
~~~

#### 启动broker
在`rocketmq-broker`模块中，找到类`org.apache.rocketmq.broker.BrokerStartup`,启动它的`main`方法.需要加上jvm启动参数`-Drocketmq.home.dir=/Users/poul/workspace/soft/rocketmq/rocketmq/distribution`, 参数值配置`rocketmq-distribution`模块的绝对路径即可

启动时也可以指定配置文件 `-c /Users/poul/workspace/soft/rocketmq/rocketmq/distribution/conf/broker.conf`

验证broker是否启动成功, 比如, broker的ip是192.168.1.2 然后名字是broker-a
~~~shell
The broker[broker-a,192.169.1.2:10911] boot success...
~~~

#### 启动proxy
也可以使用proxy的方式启动broker，

在`rocketmq-proxy`模块中，找到类`org.apache.rocketmq.proxy.ProxyStartup`,启动它的`main`方法.需要加上jvm启动参数`-Drocketmq.home.dir=/Users/poul/workspace/soft/rocketmq/rocketmq/distribution`, 参数值配置`rocketmq-distribution`模块的绝对路径即可

启动时也可以指定broker配置文件 `-bc /Users/poul/workspace/soft/rocketmq/rocketmq/distribution/conf/broker.conf`，  
指定proxy配置文件`-pc /Users/poul/workspace/soft/rocketmq/rocketmq/distribution/conf/rmq-proxy.json`
指定proxy模式 `-pm local`

验证broker是否启动成功, 比如, broker的ip是192.168.1.2 然后名字是broker-a
~~~shell
The broker[broker-a,192.169.1.2:10911] boot success...
~~~

`rmq-proxy.json`文件内容
```json
{
  "rocketMQClusterName": "DefaultCluster",
  "namesrvAddr":"localhost:9876",
  "grpcServerPort": 19999
}
```
其中的`grpcServerPort`配置是客户端的配置

### 源码阅读

#### nameserv

其实就是个注册中心

源码入口`org.apache.rocketmq.namesrv.NamesrvStartup.main(String[] args)`,

rocketmq协议中通过`org.apache.rocketmq.remoting.protocol.RequestCode` 声明的code值，定义了非常多的命令,`RemotingCommand`,namesrv判断不同的命令来处理不同的逻辑.里面一共有148个code值。

大部分的命令处理逻辑在`org.apache.rocketmq.namesrv.processor.DefaultRequestProcessor`中

注册的信息都是放在类`org.apache.rocketmq.namesrv.routeinfo.RouteInfoManager`中

指的一提的是rocketmq，namesrv在设计上，多个节点之间是没有数据同步的逻辑的。这种就简化了实现逻辑，越简单的东西就越健壮。每个节点中的数据，依赖brocker上报的信息。


#### broker

rocketmq的核心

源码入口`org.apache.rocketmq.broker.BrokerStartup.main(String[] args)`,
启动`org.apache.rocketmq.broker.BrokerController`

1. 做一些初始化的操作
  1. 初始化元数据，主要就是加载一些配置
  2. 初始化消息存储
    1. 里面会存储，msgPutTotalYesterdayMorning，msgPutTotalTodayMorning，msgGetTotalYesterdayMorning，msgGetTotalTodayMorning
    1. 初始化定时消息模块
  3. 恢复并初始化服务




### 客户端源码

[示例代码](https://github.com/apache/rocketmq-clients/tree/java-5.0.6/java/client/src/main/java/org/apache/rocketmq/client/java/example)

### dashbord源码

[rocketmq-dashboard](https://github.com/apache/rocketmq-dashboard)

# EOF