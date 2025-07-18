# Spark

[官网](https://spark.apache.org/)
[github](https://github.com/apache/spark)



## 论文

- [Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2011/EECS-2011-82.pdf)
- [Apache Spark: A Unified Engine for Big Data Processing](https://people.eecs.berkeley.edu/~matei/papers/2016/cacm_apache_spark.pdf)

## 参考文档

- [Spark SQL内置函数手册](https://spark.apache.org/docs/3.5.5/api/sql/index.html)
- 

## 源码下载
[下载网页](https://spark.apache.org/downloads.html)
[learning-spark书籍源码](https://github.com/databricks/LearningSparkV2)


## 编译
[编译](https://spark.apache.org/docs/3.5.5/building-spark.html)
[github](https://github.com/apache/spark/tree/v3.5.5)

`./build/mvn -DskipTests clean package`

上面的方式编译出来的没办法执行`spark-sql`

需要通过下面的方式来处理
`build/mvn -Phive -Phive-thriftserver -DskipTests clean package`

## 启动

### Standalone模式

```shell
# 指定一下当前的ip，选择一个合适的ip
export SPARK_LOCAL_IP=192.168.31.27
./sbin/start-master.sh -h 0.0.0.0 -p 7077 --webui-port 8080
./sbin/start-worker.sh spark://127.0.0.1:7077

# 关闭所有的spark服务
./sbin/stop-all.sh
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
  
## SparkSQL

####  Catalyst optimizer 

优化器会把计算查询转换为执行计划
1. analysis
2. logical optimization
3. physical planning
4. code generation  

- Project Tungsten


## 连接Clickhouse

[Spark Connector](https://clickhouse.com/docs/integrations/apache-spark/spark-native-connector)

[Spark Connector Github](https://github.com/ClickHouse/spark-clickhouse-connector)


## 提交一个任务
```shell
/home/poul/workspace/src/spark/spark-3.5.5/bin/spark-submit \
--executor-memory 8g \
--master spark://poul-work:7077 \
--packages com.clickhouse.spark:clickhouse-spark-runtime-3.5_2.12:0.8.0,com.clickhouse:clickhouse-client:0.7.0,com.clickhouse:clickhouse-http-client:0.7.0,org.apache.httpcomponents.client5:httpclient5:5.2.1,com.clickhouse:clickhouse-jdbc:0.8.0 \
/home/poul/workspace/src/Connan/all_test_py/spark/batch_test.py

```

阿里云的spark serverless提交

```shell
--conf spark.jars.packages=com.clickhouse.spark:clickhouse-spark-runtime-3.5_2.12:0.8.0,com.clickhouse:clickhouse-client:0.7.0,com.clickhouse:clickhouse-http-client:0.7.0,org.apache.httpcomponents.client5:httpclient5:5.2.1,com.clickhouse:clickhouse-jdbc:0.8.0 \
oss://spark-workspace/batch_test.py
```


```shell
--conf spark.jars=oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/com.clickhouse_clickhouse-client-0.8.0.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/com.clickhouse_clickhouse-data-0.8.0.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/com.clickhouse_clickhouse-http-client-0.8.0.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/com.clickhouse_clickhouse-jdbc-0.8.0.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/com.clickhouse_client-v2-0.8.0.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/com.clickhouse_jdbc-v2-0.8.0.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/com.clickhouse.spark_clickhouse-spark-runtime-3.5_2.12-0.8.0.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/com.fasterxml.jackson.core_jackson-core-2.17.2.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/commons-codec_commons-codec-1.17.1.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/commons-io_commons-io-2.16.1.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/commons-io_commons-io-2.16.1.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/org.apache.commons_commons-lang3-3.16.0.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/org.apache.httpcomponents.client5_httpclient5-5.2.1.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/org.apache.
httpcomponents.core5_httpcore5-5.2.1.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/org.apache.httpcomponents.core5_httpcore5-h2-5.2.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/org.lz4_lz4-pure-java-1.8.0.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/org.ow2.asm_asm-9.5.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/org.roaringbitmap_RoaringBitmap-0.9.47.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/org.roaringbitmap_shims-0.9.47.jar,oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/2175e3200add48e580582379192f3cb8/org.slf4j_slf4j-api-2.0.7.jar \
oss://workflow-ide-cn-shenzhen/spark_artifact/w-04c835df4a505ae3/batch_test.py
```

从clickhouse查询spark发起的sql请求
```sql
select 
query,max(event_time),min(event_time)
from system.query_log
where event_time >= '2025-07-11 15:25:09' and event_time <= '2025-07-11 16:25:09' and lower(http_user_agent) like '%spark%'
group by query order by max(event_time) desc;

select
query,exception
from system.query_log
where event_time >= '2025-07-11 15:25:09' and event_time <= '2025-07-11 16:25:09' and lower(http_user_agent) like '%spark%'
and exception is not null and exception != '' order by event_time desc;
```