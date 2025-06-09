# Spark


[官网](https://spark.apache.org/)
[github](https://github.com/apache/spark)

## 源码下载

[下载网页](https://spark.apache.org/downloads.html)


## 编译
[编译](https://spark.apache.org/docs/3.5.5/building-spark.html)



## 连接Clickhouse

[Spark Connector](https://clickhouse.com/docs/integrations/apache-spark/spark-native-connector)
[Spark Connector Github](https://github.com/ClickHouse/spark-clickhouse-connector)


```shell
/home/poul/workspace/src/spark/spark-3.5.5/bin/spark-submit \
--master spark://poul-work:7077 \
--packages com.clickhouse.spark:clickhouse-spark-runtime-3.5_2.12:0.8.0,com.clickhouse:clickhouse-jdbc:0.6.3 \
/home/poul/workspace/src/Connan/all_test_py/spark/ck_connector_test.py
```

