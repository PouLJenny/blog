# EsRally

elasticsearch 官方压测工具

[github]('https://github.com/elastic/rally' '')

[官方文档]('https://esrally.readthedocs.io/' '')

[REST Client和Transport Client官方性能对比]('https://www.elastic.co/cn/blog/benchmarking-rest-client-transport-client' '')

[Elasticsearch nightly benchmarks]('https://elasticsearch-benchmarks.elastic.co/index.html' '')

[Lucene nightly benchmarks]('https://people.apache.org/~mikemccand/lucenebench/' '')
s
## 概念

### Race（竞赛）

A “race” in Rally is the execution of a benchmarking experiment. You can choose different benchmarking scenarios (called tracks) for your benchmarks.

### Track（赛道）

A track is a specification of one or more benchmarking scenarios with a specific document corpus. It defines for example the involved indices or data streams, data files and the operations that are invoked. Its most important attributes are:

- One or more indices or data streams, with the former potentially each having one or more types.
- The queries to issue.
- Source URL of the benchmark data.
- A list of steps to run, which we’ll call “challenge”, for example indexing data with a specific number of documents per bulk request or running searches for a defined number of iterations.

### Challenge

 is the specification on what benchmarks should be run and its configuration (e.g. index, then run a search benchmark with 1000 iterations)

### Car（选手）


### Driver

drives the race, i.e. it is executing the benchmark according to the track specification.

### Reporter

A reporter tells us how the race went (currently only after the fact).

## 默认压测tracks

- Geonames: for evaluating the performance of structured data.
- Geopoint: for evaluating the performance of geopoint queries.
- Geopointshape: for evaluating the performance of geopointshape queries.
- Percolator: for evaluating the performance of percolation queries.
- PMC: for evaluating the performance of full text search.
- NYC taxis: for evaluating the performance for highly structured data.
- Nested: for evaluating the performance for nested documents.
- HTTP Logs: for evaluating the performance of (Web) server logs.
- noaa: for evaluating the performance of range fields.
- EQL: for evaluating the performance of EQL.
- Logging: for evaluating the performance of observability logging.


## 常用命令

- 查询所有的赛道 
    `esrally list tracks`

- 压测外部es集群 
    `esrally race --track=geonames --pipeline=benchmark-only --target-hosts=172.21.12.72:9200 --report-file=/home/work/.rally/benchmarks/reports/6.2.1-benchmark-only.md`


- 从外部es集群导出压测数据
    `esrally create-track --target-hosts=172.21.7.120:9200 --indices="zp_crm_customer" --output-path=~/.rally/benchmarks/tracks/private/ --track=zp_crm_customer --client-options="basic_auth_user:'elastic',basic_auth_password:'111'"`

- 指定自定义的track目录
    `esrally race --track=geonames --pipeline=benchmark-only --target-hosts=172.21.12.72:9200 --track-path=~/.rally/benchmarks/tracks/private`    

## TODO
两个问题
- 怎么压测？

- 走什么协议压测（能否trasport和http都支持）？
- 压测报告怎么看？
    csv 或者是 md
    压测指标
- 怎么自定义压测
