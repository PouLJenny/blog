---
layout: post
title:  "Mysql 索引删除后，磁盘文件没有变化?"
date:   2023-03-19 22:19:00 +0800
categories: mysql
tags: mysql
permalink: /mysql/file-clean
published: true
publish_file: 2023-03-19-mysql-file-clean.md
toc: true
---
# Mysql 索引删除后，磁盘文件没有变化?


今天碰到一个问题，线上数据库磁盘文件快满了，最后定位发现某张表的索引文件过大，里面有6个索引！！打算清理一下释放一下磁盘空间。可以没想到的是索引删除之后磁盘占用丝毫没有降低。这个就离了个大谱了！！

然后自己做了个实验：

## 首先创建一个测试表`your_table_name`
```sql
-- 创建表
CREATE TABLE your_table_name (
    id INT AUTO_INCREMENT PRIMARY KEY,
    indexed_column VARCHAR(255), -- 第二个字段设置索引
    column_3 INT,
    column_4 VARCHAR(255),
    column_5 TIMESTAMP
);
-- 创建索引
CREATE INDEX idx_indexed_column ON your_table_name (indexed_column);
```

## 插入10万行数据
```sql
-- 生成插入10万条数据的SQL语句
DELIMITER //

CREATE PROCEDURE InsertDummyData()
BEGIN
    DECLARE counter INT DEFAULT 0;
    WHILE counter < 100000 DO
        INSERT INTO your_table_name (indexed_column, column_3, column_4, column_5) VALUES 
        (CONCAT('Value', counter), RAND() * 1000, CONCAT('Description', counter), NOW());
        SET counter = counter + 1;
    END WHILE;
END//

DELIMITER ;

CALL InsertDummyData();
```

## 查询表的磁盘占用

```sql
SELECT 
    table_name AS `Table`,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS `Size (MB)`,
    ROUND((data_length / 1024 / 1024), 2) AS `Data Size (MB)`,
    ROUND((index_length / 1024 / 1024), 2) AS `Index Size (MB)`
FROM 
    information_schema.tables 
WHERE 
    table_schema = 'test_char_col'
ORDER BY 
    (data_length + index_length) DESC;
```

结果如下:

```shell
+-----------------+-----------+----------------+-----------------+
| Table           | Size (MB) | Data Size (MB) | Index Size (MB) |
+-----------------+-----------+----------------+-----------------+
| your_table_name |     11.03 |           6.52 |            4.52 |
+-----------------+-----------+----------------+-----------------+
1 row in set (0.03 sec)
```

可以看到表的数据本身占用了6MB左右，索引占用了4MB左右，整体表一共占用了11M左右的磁盘大小

再去实际的磁盘上查看文件占用的大小。具体的目录在`mysql数据根目录/数据库名`

```shell
-rw-r-----  1 999 adm   19M  3月19日 21:58 your_table_name.ibd
```

可以看到实际的磁盘上文件占用了19M。这里面其实是有空间浪费的。

## 删除索引

```sql
ALTER TABLE `your_table_name` DROP INDEX `idx_indexed_column`;
```

执行成功后再观察表占用的磁盘空间大小：

```shell
+-----------------+-----------+----------------+-----------------+
| Table           | Size (MB) | Data Size (MB) | Index Size (MB) |
+-----------------+-----------+----------------+-----------------+
| your_table_name |     11.03 |           6.52 |            4.52 |
+-----------------+-----------+----------------+-----------------+
1 row in set (0.02 sec)
```

```shell
-rw-r-----  1 999 adm   19M  3月19日 22:04 your_table_name.ibd
```

发现实际的磁盘文件和mysql的`information_schema.tables`表中的信息没有任何变化。下面需要执行一些特殊的命令来执行真正的删除操作

## 清理

首先执行:
```sql
optimize table your_table_name;
```
结果：
```shell
+-------------------------------+----------+----------+-------------------------------------------------------------------+
| Table                         | Op       | Msg_type | Msg_text                                                          |
+-------------------------------+----------+----------+-------------------------------------------------------------------+
| test_char_col.your_table_name | optimize | note     | Table does not support optimize, doing recreate + analyze instead |
| test_char_col.your_table_name | optimize | status   | OK                                                                |
+-------------------------------+----------+----------+-------------------------------------------------------------------+
```


再来看磁盘占用信息:
```shell
+-----------------+-----------+----------------+-----------------+
| Table           | Size (MB) | Data Size (MB) | Index Size (MB) |
+-----------------+-----------+----------------+-----------------+
| your_table_name |     11.03 |           6.52 |            4.52 |
+-----------------+-----------+----------------+-----------------+
```

```shell
-rw-r-----  1 999 adm   13M  3月19日 22:08 your_table_name.ibd
```
可以看到实际磁盘文件已经减少到13M了但是msyql的`information_schema.tables`表中信息没有变化。

然后需要执行下面的sql
```sql
analyze table your_table_name;
```
结果：
```shell
+-------------------------------+---------+----------+----------+
| Table                         | Op      | Msg_type | Msg_text |
+-------------------------------+---------+----------+----------+
| test_char_col.your_table_name | analyze | status   | OK       |
+-------------------------------+---------+----------+----------+
1 row in set (0.01 sec)
```

再看msyql的`information_schema.tables`表中信息
```shell
+-----------------+-----------+----------------+-----------------+
| Table           | Size (MB) | Data Size (MB) | Index Size (MB) |
+-----------------+-----------+----------------+-----------------+
| your_table_name |      6.52 |           6.52 |            0.00 |
+-----------------+-----------+----------------+-----------------+
1 row in set (0.00 sec)
```
可以看到信息已经同步成最新的了，索引数据为0了。

## 总结

除了删除索引，这种情况同样适用于`delete from table`语句删除数据。  
mysql的这种设计确实会让人产生一定的困惑，可能是为了提高删除数据的性能吧。  
最后`optimize`语法会锁表，**生产环境谨慎操作！！**



