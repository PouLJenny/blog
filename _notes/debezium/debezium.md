# debezium

## 简介

监听数据库同步的工具

[官网](https://debezium.io/ '')

[Github](https://github.com/debezium/debezium '')

## 使用

以版本1.6为例子的demo

### Mysql demo
准备docker镜像
```shell
docker pull debezium/zookeeper:1.6
docker pull debezium/kafka:1.6
docker pull debezium/example-mysql:1.6
docker pull debezium/connect:1.6
docker pull mysql:5.7
```


启动zookeeper
```shell
docker run -it --rm --name zookeeper -p 2181:2181 -p 2888:2888 -p 3888:3888 debezium/zookeeper:1.6
```

启动kafka
```shell
docker run -it --rm --name kafka -p 9092:9092 --link zookeeper:zookeeper debezium/kafka:1.6
```

启动mysql
```shell
docker run -it --rm --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=debezium -e MYSQL_USER=mysqluser -e MYSQL_PASSWORD=mysqlpw debezium/example-mysql:1.6
```

启动mysql客户端
```shell
docker run -it --rm --name mysqlterm --link mysql --rm mysql:5.7 sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'
```

启动kafka-connect

```shell
docker run -it --rm --name connect -p 8083:8083 -e GROUP_ID=1 -e CONFIG_STORAGE_TOPIC=my_connect_configs -e OFFSET_STORAGE_TOPIC=my_connect_offsets -e STATUS_STORAGE_TOPIC=my_connect_statuses --link zookeeper:zookeeper --link kafka:kafka --link mysql:mysql debezium/connect:1.6
```

校验kafka-connect启动状态
```shell
curl -H "Accept:application/json" localhost:8083/

{"version":"2.7.0","commit":"448719dc99a19793","kafka_cluster_id":"2sUP3K64S-WK6MEX3PzK0A"}
```


注册connector到数据库
```shell
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '{ "name": "inventory-connector", "config": { "connector.class": "io.debezium.connector.mysql.MySqlConnector", "tasks.max": "1", "database.hostname": "mysql", "database.port": "3306", "database.user": "debezium", "database.password": "dbz", "database.server.id": "184054", "database.server.name": "dbserver1", "database.include.list": "inventory", "database.history.kafka.bootstrap.servers": "kafka:9092", "database.history.kafka.topic": "dbhistory.inventory" } }'



HTTP/1.1 201 Created
Date: Thu, 02 Sep 2021 07:17:24 GMT
Location: http://localhost:8083/connectors/inventory-connector
Content-Type: application/json
Content-Length: 490
Server: Jetty(9.4.33.v20201020)

{"name":"inventory-connector","config":{"connector.class":"io.debezium.connector.mysql.MySqlConnector","tasks.max":"1","database.hostname":"mysql","database.port":"3306","database.user":"debezium","database.password":"dbz","database.server.id":"184054","database.server.name":"dbserver1","database.include.list":"inventory","database.history.kafka.bootstrap.servers":"kafka:9092","database.history.kafka.topic":"dbhistory.inventory","name":"inventory-connector"},"tasks":[],"type":"source"}
```

查询kafka的topic
```shell
docker run -it --rm --name watcher --link zookeeper:zookeeper --link kafka:kafka debezium/kafka:1.6 watch-topic -a -k dbserver1.inventory.customers
```

修改Mysql的数据查看更新的消息
```sql
UPDATE customers SET first_name='Anne Marie' WHERE id=1004;

DELETE FROM customers WHERE id=1004;

```


验证connect停机不会丢消息的机制
```shell
docker stop connect
```

```sql
INSERT INTO customers VALUES (default, "Sarah", "Thompson", "kitt@acme.com");
INSERT INTO customers VALUES (default, "Kenneth", "Anderson", "kander@acme.com");
```

```shell
docker run -it --rm --name connect -p 8083:8083 -e GROUP_ID=1 -e CONFIG_STORAGE_TOPIC=my_connect_configs -e OFFSET_STORAGE_TOPIC=my_connect_offsets -e STATUS_STORAGE_TOPIC=my_connect_statuses --link zookeeper:zookeeper --link kafka:kafka --link mysql:mysql debezium/connect:1.6
```
能看到kafka的topic中有两条新增的消息

停止所有的docker容器
```shell
docker stop mysqlterm watcher connect mysql kafka zookeeper
```

### Postgresql demo
[Postgresql相关的demo测试](https://github.com/debezium/debezium-examples/tree/master/tutorial#using-postgres '')
```shell
# Start the topology as defined in https://debezium.io/docs/tutorial/
export DEBEZIUM_VERSION=1.6
docker-compose -f docker-compose-postgres.yaml up

# Start Postgres connector
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @register-postgres.json

# Consume messages from a Debezium topic
docker-compose -f docker-compose-postgres.yaml exec kafka /kafka/bin/kafka-console-consumer.sh \
    --bootstrap-server kafka:9092 \
    --from-beginning \
    --property print.key=true \
    --topic dbserver1.inventory.customers

# Modify records in the database via Postgres client
docker-compose -f docker-compose-postgres.yaml exec postgres env PGOPTIONS="--search_path=inventory" bash -c 'psql -U $POSTGRES_USER postgres'

# Shut down the cluster
docker-compose -f docker-compose-postgres.yaml down
```