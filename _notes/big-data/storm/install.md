# Storm安装

[官方安装文档](https://storm.apache.org/releases/current/Setting-up-a-Storm-cluster.html '')
## Docker中安装集群

下面的方式暂时不可用
storm.yml
```yml
version: '3.1'

services:

  zookeeper:
    image: zookeeper
    container_name: zookeeper

  nimbus:
    image: storm:2.2.0
    container_name: nimbus
    command: storm nimbus
    depends_on:
      - zookeeper
    links:
      - zookeeper
    ports:
      - 6627:6627

  supervisor-01:
    image: storm:2.2.0
    container_name: supervisor-01
    command: storm supervisor
    depends_on:
      - nimbus
      - zookeeper
    links:
      - nimbus
      - zookeeper

  supervisor-02:
    image: storm:2.2.0
    container_name: supervisor-02
    command: storm supervisor
    depends_on:
      - nimbus
      - zookeeper
    links:
      - nimbus
      - zookeeper

  supervisor-03:
    image: storm:2.2.0
    container_name: supervisor-03
    command: storm supervisor
    depends_on:
      - nimbus
      - zookeeper
    links:
      - nimbus
      - zookeeper

  nimbus-ui:
    image: storm:2.2.0
    container_name: nimbus-ui
    command: storm ui 
    depends_on:
      - zookeeper
      - nimbus
    links:
      - zookeeper
      - nimbus
    ports:
      - 6080:8080
```


```shell
docker run --link nimbus:nimbus --network storm_default -it --rm -v $(pwd)/topology.jar:/topology.jar storm:2.2.0 storm jar /topology.jar com.roncoo.eshop.storm.WordCountTopology WordCountTopology
```


## 本地搭建一个最小集群

1. 本地启动一个单节点的zookeeper
2. 本地启动一个nimbus、supervisor、ui 
3. supervisor上执行 `storm logviewer` 就可以查询topology的执行日志了 




