# Postgre SQL

## 简介


PostgreSQL 是一种对象-关系型数据库管理系统([ORDBMS]('https://en.wikipedia.org/wiki/Object%E2%80%93relational_database' ''))，基于 University of California at Berkeley Computer Science Department 开发的 [POSTGRES 4.2版本]('https://dsf.berkeley.edu/postgres.html' '')


## 表膨胀

表膨胀的直接触发因素是表上的大量更新，如全表的update操作，大量的insert+delete操作等，PG在更新数据的时候是不直接删除老数据的。一个update操作执行后，
被更改的数据的旧版本也被保留了下来，直到对表做vacuum操作时，才考虑回收旧版本。做数据更新时，这些旧版本不及时回收就会造成表膨胀。

线上的实例一般会配置autovacuum，然后PG会定期自动启动autovacuum worker进程，执行vacuum回收旧版本,防止表膨胀。

### 为什么旧版本没有回收
// TODO


### 回收膨胀的空间

长事物结束后，vacuum会回收一部分旧版本。但它回收数据页内的旧版本后，一般情况下并不能把空间还给操作系统。就是说，表所占的空间没有变化。
只有一种情况下，即回收的页处于存储数据的文件尾部，并且页内没有事物可见的tuple，即整个页都可以删除时，会做truncate操作，把尾部的这些页统一从文件中删除，
文件大小和表所占空间随之减少。

另一种回收膨胀空间的方法是，执行`vacuum full <table name>` 操作。vacuum full命令实际上重建了整张表和上面的索引。它的缺点是：需要长时间的锁住表，并耗费大量的IO，对应用影响很大。要减少vacuum full锁住表的时间，可以使用社区提供的pg_repack工具。它的原理是基于原表创建一张新表，同时利用触发器，将原表上当前的增量更新不断记录下来，新表建好后，将所记录的增量更新应用到新表，直到新旧表数据完全一致。最后将新旧表表名互换，删除旧表，即完成了表的空间整理，回收了空间。

### 避免表膨胀的方法

1. 尽早、及时提交事务
2. 设计应用时，要使事务尽量短小
3. 注意配置与应用规模相适应的硬件资源（IO能力、CPU、内存等） 、并调教好数据库的性能到最佳、避免有些事务因为资源或性能问题长时间无法完成
4. 提交autovacuum,使其能按照合理的周期执行
5. 定期监控系统中是否有长事物，可以用下面的sql监控持续时间超过一定阈值的事物

    ` select * from pg_stat_activity where state<>'idle' and pg_backend_pid() != pid and (backend_xid is not null or backend_xmin is not null ) and extract(epoch from (now() - xact_start))  > <时间阈值，单位秒> ;`




## 常用的工具sql

### 查询版本
`SELECT version();`
或者
`SHOW server_version;`

### 查询表结构
`\d table_name;`
或者
`\d+ tablename`

### 查询所有的表
`select * from pg_tables;`
或者
`\dt` 查询当前数据库中的表

### 查询所有的试图
`select * from pg_views;`
或者
`\dv` 查询当前数据库中所有的视图

### 查询所有的数据库

`select * from pg_database;`
或
`\l`


### 切换数据库

`\c dbname`

### 查看索引

`\di`

### 查询所有的序列

`\ds`

### 查询所有的schema

`select * from information_schema.schemata;`

### 命令行友好展示

执行sql之前，先执行 `\x` 开启， 完后在执行一下 `\x` 关闭