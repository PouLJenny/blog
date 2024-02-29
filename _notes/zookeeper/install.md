# Zookeeper安装


## Docker中集群安装

compose文件(`zookeeper-compose.yml`)如下
```yml
version: '3.3'

services:
  zoo1:
    image: zookeeper
    hostname: zoo1
    ports:
      - 2181:2181
    environment:
      ZOO_MY_ID: 1
      ZOO_SERVERS: server.1=zoo1:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=zoo3:2888:3888;2181

  zoo2:
    image: zookeeper
    hostname: zoo2
    ports:
      - 2182:2181
    environment:
      ZOO_MY_ID: 2
      ZOO_SERVERS: server.1=zoo1:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=zoo3:2888:3888;2181

  zoo3:
    image: zookeeper
    hostname: zoo3
    ports:
      - 2183:2181
    environment:
      ZOO_MY_ID: 3
      ZOO_SERVERS: server.1=zoo1:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=zoo3:2888:3888;2181  
```

启动
```shell
docker-compose -f zookeeper-compose.yml up
```
加上参数`-d`可以后台执行
```shell
docker-compose -f zookeeper-compose.yml up -d
```

停止
```shell
docker-compose -f zookeeper-compose.yml down
```