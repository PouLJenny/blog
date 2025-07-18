# StarRocks



[官网](https://www.starrocks.io/)
[github](https://github.com/StarRocks/StarRocks)



## 基准测试/benchmarks

[官方文档](https://docs.starrocks.io/docs/3.3/introduction/StarRocks_intro/)

### SSB Star Schema Benchmark

[相关论文 Star Schema Benchmark 2009](https://www.cs.umb.edu/~poneil/StarSchemaB.PDF)
[Variations of the Star Schema Benchmark to Test the Effects of Data Skew on Query Performance 2013](https://research.spec.org/icpe_proceedings/2013/p361.pdf)

1. 数据准备
```shell
wget https://starrocks-public.oss-cn-zhangjiakou.aliyuncs.com/ssb-poc-1.0.zip
unzip ssb-poc-1.0.zip
cd ssb-poc-1.0/
make && make install
cd output/
```

2. 修改数据库配置`conf/starrocks.conf`,主要是修改里面的`mysql_host`和`mysql_port`


3. 生成数据
```shell
# 命令内部调用的其实就是python，需要创建一个虚拟的python环境，并install相关的包
sh bin/gen-ssb.sh 100 data_dir
```

4. 数据导入
```shell
# 创建表结构
sh bin/create_db_table.sh ddl_100
# 导入表数据
sh bin/flat_insert.sh data_dir
```

5. 执行测试
```shell
sh bin/benchmark.sh ssb-flat
```

#### 对clickhouse做相同的测试

[官方文档](https://clickhouse.com/docs/getting-started/example-datasets/star-schema)

1. 数据导入到clickhouse中
```shell
clickhouse-client --query="INSERT INTO ssb.customer FORMAT CSV" --format_csv_delimiter="|" < customer.tbl
clickhouse-client --query="INSERT INTO ssb.date FORMAT CSV" --format_csv_delimiter="|" < dates.tbl
clickhouse-client --query="INSERT INTO ssb.lineorder FORMAT CSV" --format_csv_delimiter="|" < lineorder.tbl
clickhouse-client --query="INSERT INTO ssb.part FORMAT CSV" --format_csv_delimiter="|" < part.tbl
clickhouse-client --query="INSERT INTO ssb.supplier FORMAT CSV" --format_csv_delimiter="|" < supplier.tbl
```

2. 生成表`lineorder_flat`
```sql
SET max_memory_usage = 20000000000;

CREATE TABLE lineorder_flat
ENGINE = MergeTree ORDER BY (LO_ORDERDATE, LO_ORDERKEY)
AS SELECT
    l.LO_ORDERKEY AS LO_ORDERKEY,
    l.LO_LINENUMBER AS LO_LINENUMBER,
    l.LO_CUSTKEY AS LO_CUSTKEY,
    l.LO_PARTKEY AS LO_PARTKEY,
    l.LO_SUPPKEY AS LO_SUPPKEY,
    l.LO_ORDERDATE AS LO_ORDERDATE,
    l.LO_ORDERPRIORITY AS LO_ORDERPRIORITY,
    l.LO_SHIPPRIORITY AS LO_SHIPPRIORITY,
    l.LO_QUANTITY AS LO_QUANTITY,
    l.LO_EXTENDEDPRICE AS LO_EXTENDEDPRICE,
    l.LO_ORDTOTALPRICE AS LO_ORDTOTALPRICE,
    l.LO_DISCOUNT AS LO_DISCOUNT,
    l.LO_REVENUE AS LO_REVENUE,
    l.LO_SUPPLYCOST AS LO_SUPPLYCOST,
    l.LO_TAX AS LO_TAX,
    l.LO_COMMITDATE AS LO_COMMITDATE,
    l.LO_SHIPMODE AS LO_SHIPMODE,
    c.C_NAME AS C_NAME,
    c.C_ADDRESS AS C_ADDRESS,
    c.C_CITY AS C_CITY,
    c.C_NATION AS C_NATION,
    c.C_REGION AS C_REGION,
    c.C_PHONE AS C_PHONE,
    c.C_MKTSEGMENT AS C_MKTSEGMENT,
    s.S_NAME AS S_NAME,
    s.S_ADDRESS AS S_ADDRESS,
    s.S_CITY AS S_CITY,
    s.S_NATION AS S_NATION,
    s.S_REGION AS S_REGION,
    s.S_PHONE AS S_PHONE,
    p.P_NAME AS P_NAME,
    p.P_MFGR AS P_MFGR,
    p.P_CATEGORY AS P_CATEGORY,
    p.P_BRAND AS P_BRAND,
    p.P_COLOR AS P_COLOR,
    p.P_TYPE AS P_TYPE,
    p.P_SIZE AS P_SIZE,
    p.P_CONTAINER AS P_CONTAINER
FROM lineorder AS l
INNER JOIN customer AS c ON c.C_CUSTKEY = l.LO_CUSTKEY
INNER JOIN supplier AS s ON s.S_SUPPKEY = l.LO_SUPPKEY
INNER JOIN part AS p ON p.P_PARTKEY = l.LO_PARTKEY;
```

#### 使用jmeter分别对clickhouse和starrocks执行ssb压力测试
机器配置
```txt
Cpu Info:
    Model: AMD Ryzen 9 7950X 16-Core Processor
    Cores: 32
    CPU max MHz:  5883
    Caches (sum of all):
        L1d:  512 KiB (16 instances)
        L1i:  512 KiB (16 instances)
        L2:   16 MiB (16 instances)
        L3:   64 MiB (2 instances)

Mem Info: 64 GB

Disk: SSD 1T
```

[jmeter测试脚本](/assets/notes/starrocks/ssb-clickhouse-starrtocks.jmx)

##### 5x10 测试

首先用5个线程，轮询10次进行测试

clickhouse load最高66
starrocks  load最高30


| Label     | # Samples | Average  | Median  | 90% Line | 95% Line | 99% Line | Min | Max  | Error % | Throughput | Received KB/sec | Sent KB/sec |
| --------- | --------- | -------- | ------- | -------- | -------- | -------- | --- | ---- | ------- | ---------- | --------------- | ----------- |
| CK-Q1.1   | 50        | 225      | 204     | 276      | 286      | 1194     | 52  | 1194 | 0.000%  | 15.56663   | 0.35            | 0.00        |
| CK-Q1.2   | 50        | 16       | 17      | 19       | 21       | 26       | 14  | 26   | 0.000%  | 28.40909   | 0.61            | 0.00        |
| CK-Q1.3   | 50        | 15       | 14      | 17       | 20       | 34       | 12  | 34   | 0.000%  | 29.08668   | 0.62            | 0.00        |
| CK-Q2.1   | 50        | 1975     | 2133    | 2493     | 2613     | 3059     | 257 | 3059 | 0.000%  | 2.31664    | 17.03           | 0.00        |
| CK-Q2.2   | 50        | 1298     | 1418    | 1742     | 1781     | 1891     | 191 | 1891 | 0.000%  | 3.40483    | 5.12            | 0.00        |
| CK-Q2.3   | 50        | 1104     | 1175    | 1533     | 1563     | 1739     | 159 | 1739 | 0.000%  | 3.90076    | 0.83            | 0.00        |
| CK-Q3.1   | 50        | 2051     | 2259    | 2541     | 2664     | 2872     | 361 | 2872 | 0.000%  | 2.23015    | 10.65           | 0.00        |
| CK-Q3.2   | 50        | 1894     | 2089    | 2394     | 2484     | 2811     | 221 | 2811 | 0.000%  | 2.41231    | 53.78           | 0.00        |
| CK-Q3.3   | 50        | 739      | 824     | 1069     | 1088     | 1135     | 153 | 1135 | 0.000%  | 5.50964    | 5.05            | 0.00        |
| CK-Q3.4   | 50        | 16       | 16      | 20       | 22       | 31       | 13  | 31   | 0.000%  | 28.39296   | 4.85            | 0.00        |
| CK-Q4.1   | 50        | 3419     | 3706    | 4090     | 4158     | 4390     | 477 | 4390 | 0.000%  | 1.38045    | 1.32            | 0.00        |
| CK-Q4.2   | 50        | 907      | 982     | 1240     | 1270     | 1326     | 150 | 1326 | 0.000%  | 4.63177    | 15.57           | 0.00        |
| CK-Q4.3   | 50        | 868      | 921     | 1204     | 1249     | 1443     | 120 | 1443 | 0.000%  | 4.70633    | 133.50          | 0.00        |
| **TOTAL** | **650**   | **1117** | **945** | **2470** | **3310** | **4081** | 12  | 4390 | 0.000%  | 3.87334    | 20.85           | 0.00        |


| Label     | # Samples | Average | Median  | 90% Line | 95% Line | 99% Line | Min  | Max  | Error % | Throughput | Received KB/sec | Sent KB/sec |
| --------- | --------- | ------- | ------- | -------- | -------- | -------- | ---- | ---- | ------- | ---------- | --------------- | ----------- |
| SR-Q1.1   | 50        | 393     | 138     | 159      | 2304     | 3444     | 130  | 3444 | 0.000%  | 10.55966   | 0.24            | 0.00        |
| SR-Q1.2   | 50        | 14      | 14      | 17       | 20       | 36       | 11   | 36   | 0.000%  | 29.00232   | 0.62            | 0.00        |
| SR-Q1.3   | 50        | 26      | 25      | 33       | 33       | 43       | 22   | 43   | 0.000%  | 27.23312   | 0.59            | 0.00        |
| SR-Q2.1   | 50        | 1236    | 1231    | 1343     | 1437     | 1842     | 766  | 1842 | 0.000%  | 3.68786    | 27.10           | 0.00        |
| SR-Q2.2   | 50        | 819     | 869     | 919      | 921      | 922      | 383  | 922  | 0.000%  | 5.30898    | 7.99            | 0.00        |
| SR-Q2.3   | 50        | 716     | 756     | 789      | 801      | 804      | 355  | 804  | 0.000%  | 6.00889    | 1.28            | 0.00        |
| SR-Q3.1   | 50        | 1901    | 1918    | 2075     | 2075     | 2509     | 1192 | 2509 | 0.000%  | 2.48213    | 11.86           | 0.00        |
| SR-Q3.2   | 50        | 1317    | 1277    | 1392     | 1796     | 2136     | 799  | 2136 | 0.000%  | 3.46021    | 77.13           | 0.00        |
| SR-Q3.3   | 50        | 527     | 623     | 653      | 657      | 662      | 206  | 662  | 0.000%  | 7.51654    | 6.89            | 0.00        |
| SR-Q3.4   | 50        | 17      | 17      | 21       | 22       | 31       | 15   | 31   | 0.000%  | 28.65330   | 4.90            | 0.00        |
| SR-Q4.1   | 50        | 2299    | 2314    | 2383     | 2386     | 3025     | 1454 | 3025 | 0.000%  | 2.10146    | 2.02            | 0.00        |
| SR-Q4.2   | 50        | 352     | 375     | 497      | 501      | 570      | 110  | 570  | 0.000%  | 10.05227   | 33.79           | 0.00        |
| SR-Q4.3   | 50        | 85      | 86      | 113      | 118      | 134      | 52   | 134  | 0.000%  | 21.33106   | 605.08          | 0.00        |
| **TOTAL** | **650**   | **746** | **566** | **1971** | **2290** | **2386** | 11   | 3444 | 0.000%  | 5.69636    | 30.66           | 0.00        |

![上图展示了 ClickHouse（CK）与 StarRocks（SR）在每个查询上的平均响应时间对比：](/assets/notes/starrocks/sr-ck-5x10.png)
上图展示了 ClickHouse（CK）与 StarRocks（SR）在每个查询上的平均响应时间对比：

结论：
1. 在大多数查询（如 Q2.1、Q2.2、Q4.1）中，StarRocks 明显优于 ClickHouse，响应时间更短。
2. 个别简单查询（如 Q1.1）中，ClickHouse 响应更快，但差距不大。
3. ClickHouse 在某些复杂查询上（Q4.1、Q3.1、Q2.1）响应时间大幅拉高，而 StarRocks 控制得较平稳。
4. clickhouse load最高66，starrocks  load最高30，稳定性方面starrocks更优秀

##### 20x10 测试

模拟高并发情况下服务的表现，所以线程数调整为20,轮询10次进行测试

clickhouse load最高248
starrocks  load最高45

| Label     | # Samples | Average | Median | 90% Line | 95% Line | 99% Line | Min | Max   | Error % | Throughput | Received KB/sec | Sent KB/sec |
|-----------|-----------|---------|--------|----------|----------|----------|-----|--------|----------|-------------|------------------|--------------|
| CK-Q1.1   | 200       | 1268    | 1236   | 1749     | 1902     | 2076     | 138 | 3049   | 0.000%   | 14.33589    | 0.32             | 0.00         |
| CK-Q1.2   | 200       | 21      | 20     | 27       | 30       | 46       | 14  | 61     | 0.000%   | 98.61933    | 2.12             | 0.00         |
| CK-Q1.3   | 200       | 14      | 14     | 17       | 19       | 25       | 11  | 31     | 0.000%   | 100.55304   | 2.16             | 0.00         |
| CK-Q2.1   | 200       | 10966   | 11162  | 12274    | 12558    | 12786    | 2689| 13406  | 0.000%   | 1.77593     | 13.05            | 0.00         |
| CK-Q2.2   | 200       | 7854    | 8128   | 9102     | 9294     | 9626     | 397 | 10375  | 0.000%   | 2.46710     | 3.71             | 0.00         |
| CK-Q2.3   | 200       | 6664    | 6870   | 7597     | 7907     | 8198     | 213 | 8800   | 0.000%   | 2.88759     | 0.61             | 0.00         |
| CK-Q3.1   | 200       | 10941   | 11097  | 12152    | 12472    | 12902    | 4321| 13063  | 0.000%   | 1.77751     | 8.49             | 0.00         |
| CK-Q3.2   | 200       | 10232   | 10524  | 11474    | 11763    | 12096    | 2138| 12887  | 0.000%   | 1.89962     | 42.35            | 0.00         |
| CK-Q3.3   | 200       | 4847    | 5055   | 5784     | 6068     | 6389     | 461 | 6512   | 0.000%   | 3.93283     | 3.61             | 0.00         |
| CK-Q3.4   | 200       | 20      | 20     | 25       | 27       | 30       | 14  | 36     | 0.000%   | 99.10803    | 16.94            | 0.00         |
| CK-Q4.1   | 200       | 16839   | 17036  | 18601    | 18831    | 19473    | 8431| 19673  | 0.000%   | 1.16410     | 1.12             | 0.00         |
| CK-Q4.2   | 200       | 5091    | 5237   | 5924     | 6064     | 6262     | 446 | 6726   | 0.000%   | 3.74125     | 12.58            | 0.00         |
| CK-Q4.3   | 200       | 5185    | 5444   | 6048     | 6267     | 7070     | 260 | 7209   | 0.000%   | 3.69269     | 104.75           | 0.00         |
| TOTAL     | 2600      | 6150    | 5713   | 12049    | 16592    | 18361    | 11  | 19673  | 0.000%   | 3.12530     | 16.82            | 0.00         |




| Label     | # Samples | Average | Median | 90% Line | 95% Line | 99% Line | Min | Max   | Error % | Throughput | Received KB/sec | Sent KB/sec |
|-----------|-----------|---------|--------|----------|----------|----------|-----|--------|----------|-------------|------------------|--------------|
| SR-Q1.1   | 200       | 709     | 512    | 617      | 2557     | 3369     | 60  | 3513   | 0.000%   | 24.71577    | 0.56             | 0.00         |
| SR-Q1.2   | 200       | 20      | 18     | 32       | 37       | 47       | 12  | 49     | 0.000%   | 95.96929    | 2.06             | 0.00         |
| SR-Q1.3   | 200       | 88      | 76     | 149      | 174      | 208      | 26  | 216    | 0.000%   | 77.07129    | 1.66             | 0.00         |
| SR-Q2.1   | 200       | 7013    | 7416   | 7980     | 8080     | 8554     | 2564| 8582   | 0.000%   | 2.78917     | 20.50            | 0.00         |
| SR-Q2.2   | 200       | 2883    | 2972   | 3210     | 3266     | 3435     | 897 | 3539   | 0.000%   | 6.57095     | 9.89             | 0.00         |
| SR-Q2.3   | 200       | 2373    | 2462   | 2656     | 2718     | 2833     | 848 | 2888   | 0.000%   | 7.94313     | 1.69             | 0.00         |
| SR-Q3.1   | 200       | 8098    | 8218   | 9049     | 9345     | 10269    | 3925| 10921  | 0.000%   | 2.41812     | 11.55            | 0.00         |
| SR-Q3.2   | 200       | 6269    | 6329   | 7417     | 7876     | 8414     | 1961| 8534   | 0.000%   | 3.10227     | 69.16            | 0.00         |
| SR-Q3.3   | 200       | 2391    | 2466   | 2689     | 2710     | 2731     | 756 | 2806   | 0.000%   | 7.86256     | 7.21             | 0.00         |
| SR-Q3.4   | 200       | 24      | 23     | 34       | 36       | 49       | 14  | 52     | 0.000%   | 94.47331    | 16.15            | 0.00         |
| SR-Q4.1   | 200       | 10289   | 10446  | 11599    | 11864    | 12597    | 3723| 13047  | 0.000%   | 1.89816     | 1.82             | 0.00         |
| SR-Q4.2   | 200       | 1708    | 1826   | 1972     | 2050     | 2140     | 292 | 2188   | 0.000%   | 10.65303    | 35.81            | 0.00         |
| SR-Q4.3   | 200       | 487     | 523    | 665      | 674      | 696      | 84  | 713    | 0.000%   | 30.39514    | 862.19           | 0.00         |
| TOTAL     | 2600      | 3258    | 2315   | 8453     | 10131    | 11410    | 12  | 13047  | 0.000%   | 5.82486     | 31.35            | 0.00         |


![上图展示了 ClickHouse（CK）与 StarRocks（SR）在每个查询上的平均响应时间对比：](/assets/notes/starrocks/sr-ck-20x10.png)
上图展示了 ClickHouse（CK）与 StarRocks（SR）在每个查询上的平均响应时间对比：

1. StarRocks 在 Q1.1 和 Q1.3 上更快（尤其 Q1.1 差距明显），但 Q1.3 例外，ClickHouse 更快。
2. ClickHouse 在所有中重型查询上（如 Q2.1、Q2.2、Q3.1、Q4.1）都明显慢于 StarRocks，差距从几百毫秒到数千毫秒不等。
3. StarRocks 在这些查询上的平均响应时间普遍只有 ClickHouse 的一半甚至更低。
4. StarRocks 更擅长处理复杂查询，性能更优。
5. clickhouse load最高248,starrocks  load最高45,starrocks在高并发情况下稳定性更为显著

#### 与clickhouse存储空间占用的对比

测试数据原始文件大小
```shell
-rw-r--r-- 1 poul poul 274M  7月14日 16:23 customer.tbl
-rw-r--r-- 1 poul poul 223K  7月14日 16:23 dates.tbl
-rw-r--r-- 1 poul poul  59G  7月14日 16:23 lineorder.tbl
-rw-r--r-- 1 poul poul 115M  7月14日 16:23 part.tbl
-rw-r--r-- 1 poul poul  17M  7月14日 16:23 supplier.tbl
```

clickhouse存储文件大小
```shell
   ┌─database─┬─table──────────┬─uncompressed_size─┬─compressed_size─┬─compression_ratio_percent─┐
1. │ ssb      │ lineorder_flat │ 96.47 GiB         │ 53.22 GiB       │                     55.16 │
2. │ ssb      │ lineorder      │ 23.48 GiB         │ 16.66 GiB       │                     70.97 │
3. │ ssb      │ customer       │ 168.74 MiB        │ 114.64 MiB      │                     67.94 │
4. │ ssb      │ part           │ 34.76 MiB         │ 24.33 MiB       │                        70 │
5. │ ssb      │ supplier       │ 11.06 MiB         │ 7.52 MiB        │                     68.02 │
6. │ ssb      │ date           │ 113.70 KiB        │ 22.85 KiB       │                     20.09 │
   └──────────┴────────────────┴───────────────────┴─────────────────┴───────────────────────────┘
```

starrocks存储文件大小
```shell
StarRocks > show data;
+----------------+----------------+---------------------+
| TableName      | Size           | ReplicaCount        |
+----------------+----------------+---------------------+
| customer       | 138.408 MB     | 12                  |
| dates          | 33.679 KB      | 1                   |
| lineorder      | 14.612 GB      | 336                 |
| lineorder_flat | 58.827 GB      | 336                 |
| part           | 12.946 MB      | 12                  |
| supplier       | 9.182 MB       | 12                  |
| Total          | 73.596 GB      | 709                 |
| Quota          | 8388608.000 TB | 9223372036854775807 |
| Left           | 8388607.928 TB | 9223372036854775098 |
+----------------+----------------+---------------------+
```

对比下来两者的存储成本差不太多
### TPC-H Benchmark

### TPC-DS Benchmarking

