# Kafka源码阅读

kafka的后端是用scala写的
客户端是用java写的

## 环境准备
- jdk 1.8
- scala 2.13.x
- kafka 3.4.1 
- gradle 7.6
- idea 安装scala插件
- zookeeper 3.7.1

## 源码启动

1. 下载并解压[源码](https://archive.apache.org/dist/kafka/3.4.1/kafka-3.4.1-src.tgz )
2. 下载[scala](https://www.scala-lang.org/download/2.13.11.html ),并配置环境变量
    ```config
    export SCALA_HOME=/Users/liqiushi/poul/soft/scala/scala-2.13.11
    export PATH=$SCALA_HOME/bin:$PATH
    ```
3. idea 安装scala插件
4. idea 导入源码
5. `build.gradle`文件中添加配置，加速jar包的[导入](../../gradle/gradle.md ) 
6. idea配置jdk和scala sdk目录
7. docker中启动一个[zookeeper](../../zookeeper/install.md )
8. 修改文件`config/server.properties`
```properties
# 修改zk的连接地址
zookeeper.connect=poul-manjaro:2181
```

解决一下启动日志报错问题
文件`gradle/denpendencies.gradle`，添加
```
slf4jSimple: "org.slf4j:slf4j-simple:$versions.slf4j",
```
文件`build.gradle`
```
project(':core') {
      dependencies {
        implementation libs.slf4jSimple
      }
}
```

9. 找到主类 `core/src/main/scala/kafka/Kafka.scala` 直接启动
    看到下面的启动日志则表示启动成功
    ```log
    [main] INFO kafka.server.KafkaServer - [KafkaServer id=0] started
    ```

## 问题
1. 用git初始化源码目录后竟然会报错，无法启动，简直神奇
2. 