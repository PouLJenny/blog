# Spark

[官网](https://spark.apache.org/)
[github](https://github.com/apache/spark)



## 论文

- [Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2011/EECS-2011-82.pdf)
- [Apache Spark: A Unified Engine for Big Data Processing](https://people.eecs.berkeley.edu/~matei/papers/2016/cacm_apache_spark.pdf)



## 源码下载
[下载网页](https://spark.apache.org/downloads.html)
[learning-spark书籍源码](https://github.com/databricks/LearningSparkV2)


## 编译
[编译](https://spark.apache.org/docs/3.5.5/building-spark.html)
[github](https://github.com/apache/spark/tree/v3.5.5)

`./build/mvn -DskipTests clean package`

## 启动

### Standalone模式

```shell
./sbin/start-master.sh -h 0.0.0.0 -p 7077 --webui-port 8080
./sbin/start-worker.sh spark://127.0.0.1:7077
```


## 设计哲学

Spark's design philosophy centers around four key characteristics:
- Speed
    - 代码实现，高效利用了当今计算机的硬件条件
    - Spark将其查询计算构建为有向无环图(DAG)
    - 所有中间结果都是缓存在内存中的，限制了磁盘I/O的使用
- Ease of use
    - 统一数据抽象类型， Resilient Distributed Dataset (RDD)
- Modularity 
    - 有个统一的引擎，来处理所有的workload
- Extensibility
    - Spark专注于计算，不涉及存储，并将两者分离。所以可以读取任何地方的数据，也可以把结果数据写入到任何地方


## 一些概念

- Application
  - 一个使用Spark API构建的用户程序
- SparkSession
  - 提供与底层Spark功能交互的入口点，并允许使用其API编程Spark的对象
- Job
  - 并行计算，由多个任务组成，
- Stage
  - 每个Job都被分为更小的Stage集合，并且stage之间相互依赖
- Task
  - A single unit of work or execution that will be sent to a Spark executor.
  


## 连接Clickhouse

[Spark Connector](https://clickhouse.com/docs/integrations/apache-spark/spark-native-connector)
[Spark Connector Github](https://github.com/ClickHouse/spark-clickhouse-connector)


```shell
/home/poul/workspace/src/spark/spark-3.5.5/bin/spark-submit \
--master spark://poul-work:7077 \
--packages com.clickhouse.spark:clickhouse-spark-runtime-3.5_2.12:0.8.0,com.clickhouse:clickhouse-client:0.7.0,com.clickhouse:clickhouse-http-client:0.7.0,org.apache.httpcomponents.client5:httpclient5:5.2.1 \
/home/poul/workspace/src/Connan/all_test_py/spark/ck_connector_test.py
```

