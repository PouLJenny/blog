# Kafka 安装


## Docker安装 集群

compose文件(`kafka-compose.yml`)如下
```yml
version: '3.7'

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

  kafka1:
    image: wurstmeister/kafka
    container_name: kafka1
    hostname: kafka1
    ports:
      - "9091:9092"
    links:
      - zoo1
      - zoo2
      - zoo3
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ADVERTISED_HOST_NAME: 192.168.0.101                   ## 修改:宿主机IP
      KAFKA_ADVERTISED_PORT: 9091                                  ## 修改:宿主机映射port
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://192.168.0.101:9091    ## 绑定发布订阅的端口。修改:宿主机IP
      KAFKA_ZOOKEEPER_CONNECT: "zoo1:2181,zoo2:2181,zoo3:2181"


  kafka2:
    image: wurstmeister/kafka
    container_name: kafka2
    hostname: kafka2
    ports:
      - "9092:9092"
    links:
      - zoo1
      - zoo2
      - zoo3
    environment:
      KAFKA_BROKER_ID: 2
      KAFKA_ADVERTISED_HOST_NAME: 192.168.0.101                ## 修改:宿主机IP
      KAFKA_ADVERTISED_PORT: 9092                               ## 修改:宿主机映射port
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://192.168.0.101:9092   ## 修改:宿主机IP
      KAFKA_ZOOKEEPER_CONNECT: "zoo1:2181,zoo2:2181,zoo3:2181"

  kafka3:
    image: wurstmeister/kafka
    container_name: kafka3
    hostname: kafka3
    ports:
      - "9093:9092"
    links:
      - zoo1
      - zoo2
      - zoo3
    environment:
      KAFKA_BROKER_ID: 3
      KAFKA_ADVERTISED_HOST_NAME: 192.168.0.101                 ## 修改:宿主机IP
      KAFKA_ADVERTISED_PORT: 9093                              ## 修改:宿主机映射port
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://192.168.0.101:9093   ## 修改:宿主机IP
      KAFKA_ZOOKEEPER_CONNECT: "zoo1:2181,zoo2:2181,zoo3:2181"


  kafka-manager:
    image: sheepkiller/kafka-manager:latest
    container_name: kafka-manager
    hostname: kafka-manager
    ports:
      - "9000:9000"
    links:            # 连接本compose文件创建的container
      - kafka1
      - kafka2
      - kafka3
      - zoo1
      - zoo2
      - zoo3
    environment:
      ZK_HOSTS: zoo1:2181,zoo2:2181,zoo3:2181                 ## 修改:宿主机IP
      TZ: CST-8
```

启动命令
```shell
sudo docker-compose -f kafka-compose.yml up -d
```