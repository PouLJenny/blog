# PostgreSQL 复制


## logical replication 逻辑复制


### demo

创建逻辑复制的slot

```sql
SELECT * FROM pg_create_logical_replication_slot('regression_slot', 'test_decoding');
```

查询当前数据库中的 replication slot
```sql
SELECT * FROM pg_replication_slots;
```

创建一张新表
```sql
CREATE TABLE data(id serial primary key, data text);
```

查询复制槽里面的数据
```sql
SELECT * FROM pg_logical_slot_get_changes('regression_slot', NULL, NULL);

-- 如果插件转换的是字节信息的话则使用下面的sql
SELECT * FROM pg_logical_slot_get_binary_changes('regression_slot', NULL, NULL);
-- pgoutput 插件需要执行下面的命令
-- pg10版本后 新增了发布/订阅模块，这样可以过滤一些不想要的表
-- 创建发布
CREATE PUBLICATION cdc;
-- 添加要监听的表
ALTER PUBLICATION cdc ADD TABLE data;

SELECT * FROM pg_logical_slot_get_binary_changes('regression_slot', NULL, NULL,'publication_names', 'cdc','proto_version','1');
```

插入几行数据，然后查询复制槽(slot)中的数据，并消费

```sql
BEGIN;
INSERT INTO data(data) VALUES('1');
INSERT INTO data(data) VALUES('2');
COMMIT;
```

[设置表的REPLICA-IDENTITY](https://www.postgresql.org/docs/9.6/sql-altertable.html#SQL-CREATETABLE-REPLICA-IDENTITY '')后再执行sql，观察数据的对比
有四种选择
- **DEFAULT** `UPDATE` and `DELETE` events will only contain the previous values for the primary key columns of a table
- **NOTHING** `UPDATE` and `DELETE` events will not contain any information about the previous value on any of the table columns
- **FULL** - `UPDATE` and `DELETE` events will contain the previous values of all the table’s columns, 这个模式下，如果是走数据库发布订阅的方式的话，订阅方会全表扫描，性能非常差，慎用！！
- **INDEX** `index name` - `UPDATE` and `DELETE` events will contains the previous values of the columns contained in the index definition named index name
```sql
ALTER TABLE data REPLICA IDENTITY FULL;
```
查询表的REPLICA IDENTITY
```sql
\d+ tablename
```
或者是
```sql
SELECT CASE relreplident
          WHEN 'd' THEN 'default'
          WHEN 'n' THEN 'nothing'
          WHEN 'f' THEN 'full'
          WHEN 'i' THEN 'index'
       END AS replica_identity
FROM pg_class
WHERE oid = 'mytablename'::regclass;
```
```sql
-- d: default n: nothing f:full i:index
select relreplident from pg_class where relname = 'mytablename';
```

也可以，查询复制槽中的数据但是不消费

```sql
INSERT INTO data(data) VALUES('3');

-- 查询复制槽中的数据但是不消费
SELECT * FROM pg_logical_slot_peek_changes('regression_slot', NULL, NULL);

-- 如果插件转换的是字节信息的话则使用下面的sql
SELECT * FROM pg_logical_slot_peek_binary_changes('regression_slot', NULL, NULL);

-- pgoutput需要执行下面的命令
SELECT * FROM pg_logical_slot_peek_binary_changes('regression_slot', NULL, NULL, 'publication_names', 'cdc', 'proto_version', '1');
```

output plugin，可能传入参数来格式化数据
```sql
SELECT * FROM pg_logical_slot_peek_changes('regression_slot', NULL, NULL, 'include-timestamp', 'on');
```

删除用来测试的复制槽
```sql
SELECT pg_drop_replication_slot('regression_slot');
```

删除用来测试的表
```sql
drop table data;
```

删除订阅
```sql
DROP PUBLICATION cdc;
```

### output plugins

复制槽的插件用来格式刷，wal中的数据

- test_decoding pg自带的用来测试的demo
- [wal2json](https://github.com/eulerto/wal2json '') 转换成json的插件
- [decoderbufs](https://github.com/debezium/postgres-decoderbufs '') google的protobuf插件
- pgoutput pg 10+自带的格式化插件


#### test_decodeing slots输出

##### DEFAULT 模式下
```
INSERT 
table inventory.data: INSERT: id[integer]:1 data[character varying]:'1'

UPDATE 
table inventory.data: UPDATE: id[integer]:1 data[character varying]:'6666'

DELETE 
table inventory.data: DELETE: id[integer]:1
```

##### INDEX data 模式下
```
INSERT 
table inventory.data: INSERT: id[integer]:1 data[character varying]:'1'

UPDATE 
table inventory.data: UPDATE: old-key: data[character varying]:'1' new-tuple: id[integer]:1 data[character varying]:'6666'

DELETE 
table inventory.data: DELETE: data[character varying]:'6666'

```
##### FULL 模式下
```
INSERT 
table inventory.data: INSERT: id[integer]:1 data[character varying]:'1'

UPDATE 
table inventory.data: UPDATE: old-key: id[integer]:1 data[character varying]:'1' new-tuple: id[integer]:1 data[character varying]:'6666'

DELETE 
table inventory.data: DELETE: id[integer]:1 data[character varying]:'6666'
```

##### NOTHING 模式下

```
INSERT 
table inventory.data: INSERT: id[integer]:1 data[character varying]:'1'

UPDATE 
table inventory.data: UPDATE: id[integer]:1 data[character varying]:'6666'

DELETE 
table inventory.data: DELETE: (no-tuple-data)
```

#### wal2json 插件slots输出

##### DEFAULT 模式下
```
INSERT 
{"change":[{"kind":"insert","schema":"inventory","table":"data","columnnames":["id","data"],"columntypes":["integer","character varying"],"columnvalues":[1,"1"]}]}

UPDATE 
{"change":[{"kind":"update","schema":"inventory","table":"data","columnnames":["id","data"],"columntypes":["integer","character varying"],"columnvalues":[1,"6666"],"oldkeys":{"keynames":["id"],"keytypes":["integer"],"keyvalues":[1]}}]}

DELETE 
{"change":[{"kind":"delete","schema":"inventory","table":"data","oldkeys":{"keynames":["id"],"keytypes":["integer"],"keyvalues":[1]}}]}
```

##### INDEX data 模式下
```
INSERT 
{"change":[{"kind":"insert","schema":"inventory","table":"data","columnnames":["id","data"],"columntypes":["integer","character varying"],"columnvalues":[1,"1"]}]}

UPDATE 
{"change":[{"kind":"update","schema":"inventory","table":"data","columnnames":["id","data"],"columntypes":["integer","character varying"],"columnvalues":[1,"6666"],"oldkeys":{"keynames":["data"],"keytypes":["character varying"],"keyvalues":["1"]}}]}

DELETE 
{"change":[{"kind":"delete","schema":"inventory","table":"data","oldkeys":{"keynames":["data"],"keytypes":["character varying"],"keyvalues":["6666"]}}]}

```
##### FULL 模式下
```
{"change":[{"kind":"insert","schema":"inventory","table":"data","columnnames":["id","data"],"columntypes":["integer","character varying"],"columnvalues":[1,"1"]}]}

UPDATE 
{"change":[{"kind":"update","schema":"inventory","table":"data","columnnames":["id","data"],"columntypes":["integer","character varying"],"columnvalues":[1,"6666"],"oldkeys":{"keynames":["id","data"],"keytypes":["integer","character varying"],"keyvalues":[1,"1"]}}]}

DELETE 
{"change":[{"kind":"delete","schema":"inventory","table":"data","oldkeys":{"keynames":["id","data"],"keytypes":["integer","character varying"],"keyvalues":[1,"6666"]}}]}
```

##### NOTHING 模式下

```
INSERT 
{"change":[{"kind":"insert","schema":"inventory","table":"data","columnnames":["id","data"],"columntypes":["integer","character varying"],"columnvalues":[1,"1"]}]}

UPDATE 
{"change":[]}

DELETE 
{"change":[]}
```


## publication & subscription
[官方文档](https://www.postgresql.org/docs/current/logical-replication-subscription.html '')
从11版本才支持


## HA 高可用
[官方文档](https://www.postgresql.org/docs/9.6/high-availability.html '')

### 主从架构搭建


#### docker 
9.6版本的主从搭建，通过docker

[参考文章](https://blog.csdn.net/shenlongyu/article/details/87741576 '')

1. 启动docker并挂载目录
```shell
mkdir -p /Users/admin/Workspace/docker/postgres-master-slave
cd /Users/admin/Workspace/docker/postgres-master-slave

# 主库
docker run -it --name pgmaster -p 54320:5432 -e POSTGRES_PASSWORD=123456 -v /etc/localtime:/etc/localtime -v /Users/admin/Workspace/docker/postgres-master-slave/pgmaster:/var/lib/postgresql/data -d postgres:9.6.2

# 从库
docker run -it --name pgslave -p 54321:5432 -e POSTGRES_PASSWORD=223456 -v /etc/localtime:/etc/localtime -v /Users/admin/Workspace/docker/postgres-master-slave/pgslave:/var/lib/postgresql/data -d postgres:9.6.2

# 获取主从库的docker ip
docker inspect pgmaster |grep IPAddress
docker inspect pgslave |grep IPAddress
```
2. 配置Master

编辑pg_hba.conf，在最下面添加如下：
```conf
# replication_username: 复制账号; slave_ip: 从库所在的服务器ip
# host    replication     <replication_username>      <slave_ip>/32          md5  
host    replication     repuser      172.17.0.3/32         trust
```

编辑postgresql.conf更改如下：
```conf
wal_level = hot_standby
max_wal_senders = 2
wal_keep_segments = 16
wal_sender_timeout = 60s
hot_standby = on
synchronous_standby_names = '*'
```

 进入容器，登录PostgreSQL，创建复制账号并验证：【如果用postgres用户可不进行此步骤】
 ```conf
 # 1.进入容器
docker exec -it pgmaster /bin/bash

# 2.连接PostgreSQL
psql -U postgres

# 3.创建用户，如果不是用postgres用户需要添加用户
set synchronous_commit =off;
# replication_username: 对应上面设置的复制账号; replication_username_password: 认证密码
create role repuser login replication encrypted password 'repuser123';  
# 4.验证用户
\du
 ```


停止PostgreSQL
```conf
docker stop pgmaster pgslave
```

3. 配置Slave（从库）

同步主从库数据(必须)【如果是在单机2容器下，请直接用已认证方式】
```shell
# 已ssh认证，请将$(pwd)更改为实际的路径
rsync -cva --inplace --exclude=*pg_xlog* /Users/admin/Workspace/docker/postgres-master-slave/pgmaster/ /Users/admin/Workspace/docker/postgres-master-slave/pgslave/
```

编辑postgresql.conf更改如下
```conf
hot_standby = on
```

新建recovery.conf，添加如下内容：
```conf
standby_mode = 'on'

#replication_username: 复制账号(同主库); master_ip: 主库所在的服务器ip; master_port: 主库端口; replication_username_password: 认证密码
# primary_conninfo = 'host=<master_ip> port=<master_port> user=<replication_username> password=<replication_username_password>'
primary_conninfo = 'host=172.17.0.2 port=5432 user=repuser password=repuser123'
```

4. 分别启动主从数据库
```shell
docker start pgmaster
docker start pgslave
```

5. 查询复制状态
```shell
# 进入主库容器
docker exec -it pgmaster bash
# 查看复制状态
psql -U postgres -x -c "select * from pg_stat_replication;"
```

6. 测试从库访问
```shell
# 主库postgres账号执行：
CREATE USER pguser WITH PASSWORD 'pguser123';
CREATE DATABASE testdb OWNER pguser;

# 主库切换到pguser账号执行：
psql -U pguser
# 创建数据库和数据
CREATE TABLE test(a int);
INSERT INTO test(a) VALUES(100);
INSERT INTO test(a) VALUES(222);

# 从库pguser账号执行：
psql -U pguser -d testdb
select * from test;
```

