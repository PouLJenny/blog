# Elastic
[官网]('https://www.elastic.co' '') 
## elastic stack
- Elasticsearch  
- Kibana         es的可视化界面控制台
- Logstash       集中，转换和存储数据
- Beats          轻量级数据收集器

通过Elastic提供的技术栈企业可以基于ELK架构或者ELKB架构轻松搭建自己的搜索服务

Elasticsearch

## 简介
Elasticsearch 是一个分布式可扩展的实时搜索和分析引擎,一个建立在全文搜索引擎 Apache Lucene(TM) 基础上的搜索引擎.
当然 Elasticsearch 并不仅仅是 Lucene 那么简单，它不仅包括了全文搜索功能，还可以进行以下工作:
- 分布式实时文件存储，并将每一个字段都编入索引，使其可以被搜索。
- 实时分析的分布式搜索引擎。
- 可以扩展到上百台服务器，处理PB级别的结构化或非结构化数据。
## 基本概念：

- near-realtime (NRT)
  - Elasticsearch是一个近实时搜索平台。这意味着从索引文档到可搜索文档的时间有一点延迟（通常是一秒）。
- Cluster
  - 集群是一个或多个节点（服务器）的集合，它们共同保存您的整个数据，并提供跨所有节点的联合索引和搜索功能。群集由唯一名称标识，默认情况下为“elasticsearch”。
  此名称很重要，因为如果节点设置为按名称加入群集，则该节点只能是群集的一部分。确保不要在不同的环境中重用相同的群集名称，
  否则最终会导致节点加入错误的群集。例如，您可以使用logging-dev，logging-stage以及logging-prod 用于开发，测试和生产集群。
  请注意，拥有一个只包含单个节点的集群是完全正常的。此外，您还可以拥有多个独立的集群，每个集群都有自己唯一的集群名称。
- Node
  - 节点是作为群集一部分的单个服务器，存储数据并参与群集的索引和搜索功能。与集群一样，节点由名称标识，默认情况下，该名称是在启动时
  分配给节点的随机通用唯一标识符（UUID）。如果不需要默认值，可以定义所需的任何节点名称。此名称对于管理目的非常重要，您可以在其中
  识别网络中的哪些服务器与Elasticsearch集群中的哪些节点相对应。可以将节点配置为按群集名称加入特定群集。默认情况下，每个节点都设置
  为加入一个名为cluster的集群elasticsearch，这意味着如果您在网络上启动了许多节点并且假设它们可以相互发现 - 它们将自动形成并加入一
  个名为的集群elasticsearch。
  在单个群集中，您可以拥有任意数量的节点。此外，如果您的网络上当前没有其他Elasticsearch节点正在运行，则默认情况下启动单个节点将形
  成一个名为的新单节点集群elasticsearch。
- Index
  - 索引是具有某些类似特征的文档集合。例如，您可以拥有客户数据的索引，产品目录的另一个索引以及订单数据的另一个索引。索引由名称标识（必须全部为小写），
  并且此名称用于在对其中的文档执行索引，搜索，更新和删除操作时引用索引。
  在单个群集中，您可以根据需要定义任意数量的索引。
- Type
  - 在6.0.0中弃用。
  一种类型，曾经是索引的逻辑类别/分区，允许您在同一索引中存储不同类型的文档，例如一种类型用于用户，另一种类型用于博客帖子。不
  再可能在索引中创建多个类型，并且将在更高版本中删除类型的整个概念。
- Document
  - 文档是可以编制索引的基本信息单元。例如，您可以为单个客户提供文档，为单个产品提供另一个文档，为单个订单提供另一个文档。
  该文档以JSON（JavaScript Object Notation）表示，JSON是一种普遍存在的互联网数据交换格式。
  在索引/类型中，您可以根据需要存储任意数量的文档。请注意，尽管文档实际上位于索引中，但实际上必须将文档编入索引/分配给索引中的类型。

  - Document是不可变的，如果更新的话，会创建一个新的document
- Shards&Replicas
  - 索引可能存储大量可能超过单个节点的硬件限制的数据。例如，占用1TB磁盘空间的十亿个文档的单个索引可能不适合单个节点的磁盘，或者可能
  太慢而无法单独从单个节点提供搜索请求。
  为了解决这个问题，Elasticsearch提供了将索引细分为多个称为分片的功能。创建索引时，只需定义所需的分片数即可。每个分片本身都是一个
  功能齐全且独立的“索引”，可以托管在集群中的任何节点上。
  分片很重要，主要有两个原因：
    1. 它允许您水平分割/缩放内容量
    2. 它允许您跨分片（可能在多个节点上）分布和并行化操作，从而提高性能/吞吐量
  分片的分布方式以及如何将文档聚合回搜索请求的机制完全由Elasticsearch管理，对用户来说是透明的。
  在任何时候都可以预期出现故障的网络/云环境中，非常有用，强烈建议使用故障转移机制，以防分片/节点以某种方式脱机或因任何原因消失。
  为此，Elasticsearch允许您将索引的分片的一个或多个副本制作成所谓的副本分片或简称副本。
  
  复制很重要，主要有两个原因：
    1. 它在碎片/节点出现故障时提供高可用性。因此，请务必注意，副本分片永远不会在与从中复制的原始/主分片相同的节点上分配。
    2. 它允许您扩展搜索量/吞吐量，因为可以在所有副本上并行执行搜索。

  总而言之，每个索引可以拆分为多个分片。索引也可以复制为零（表示没有副本）或更多次。复制后，每个索引都将具有主分片（从中复制的原始分片）
  和副本分片（主分片的副本）。可以在创建索引时为每个索引定义分片和副本的数量。创建索引后，您还可以随时动态更改副本数。
  您可以使用_shrink和_splitAPI 更改现有索引的分片数，但这不是一项简单的任务，预先计划正确数量的分片是最佳方法。
  默认情况下，Elasticsearch中的每个索引都分配了5个主分片和1个副本，这意味着如果群集中至少有两个节点，
  则索引将包含5个主分片和另外5个副本分片（1个完整副本），总计为每个索引10个分片。
  
- Segment

  Lucene里面的一个数据集概念

  一个Index会由一个或多个sub-index构成，sub-index被称为Segment。Lucene的Segment设计思想，与LSM类似但又有些不同，继承了LSM中数据写入的优点，
  但是在查询上只能提供近实时而非实时查询。

  Lucene中的数据写入会先写内存的一个Buffer（类似LSM的MemTable，但是不可读），当Buffer内数据到一定量后会被flush成一个Segment，每个Segment有自己独立的索引，
  可独立被查询，但数据永远不能被更改。这种模式避免了随机写，数据写入都是Batch和Append，能达到很高的吞吐量。Segment中写入的文档不可被修改，但可被删除，
  删除的方式也不是在文件内部原地更改，而是会由另外一个文件保存需要被删除的文档的DocID，保证数据文件不可被修改。Index的查询需要对多个Segment进行查询并对结果进行合并，
  还需要处理被删除的文档，为了对查询进行优化，Lucene会有策略对多个Segment进行合并，这点与LSM对SSTable的Merge类似。

  Segment在被flush或commit之前，数据保存在内存中，是不可被搜索的，这也就是为什么Lucene被称为提供近实时而非实时查询的原因。读了它的代码后，发现它并不是不能实现数据写入即可查，
  只是实现起来比较复杂。原因是Lucene中数据搜索依赖构建的索引（例如倒排依赖Term Dictionary），Lucene中对数据索引的构建会在Segment flush时，而非实时构建，目的是为了构建最高效索引。
  当然它可引入另外一套索引机制，在数据实时写入时即构建，但这套索引实现会与当前Segment内索引不同，需要引入额外的写入时索引以及另外一套查询机制，有一定复杂度。

注意：
    每个Elasticsearch分片都是Lucene索引。单个Lucene索引中可以包含最多文档数。截止LUCENE-5843，
    限制是2,147,483,519（= Integer.MAX_VALUE - 128）文档。您可以使用_cat/shards API 监控分片大小。

### Mapping parameters

- store
  - true或者是false，一般默认false，开启后可以使用stored_fields查询，个人感觉没啥用，使用_source完全可以替代，不用开启
- index
  - true或者false，一般默认true，控制是否可以被索引
- doc_values
  - Sorting, aggregations, and access to field values in scripts requires a different data access pattern
  - 翻译过来就是用于排序，聚合，脚本中，true或false 大部分字段默认true
- norms
  - 字段评分使用 true或者false 常用于keyword（默认false）和text（默认true）字段
  - 开启的字段，可以手动动态的设定为false，但不能从false设置成true,设置方式 :
    ```
    PUT my_index/_mapping
    {
      "properties": {
        "title": {
          "type": "text",
          "norms": false
        }
      }
    }
    ```



## API示例
    GET /_cat/health?v 查看集群的状态
        示例结果：
        epoch      timestamp cluster status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
        1552976356 06:19:16  es-dev  yellow          1         1     11  11    0    0        5             0                  -                 68.8%
        集群状态：
            绿色 - 一切都很好（集群功能齐全）
            黄色 - 所有数据都可用，但尚未分配一些副本（群集功能齐全）
            红色 - 某些数据由于某种原因不可用（群集部分功能）
    GET /_cat/nodes?v 查看集群节点列表
        示例结果：
        ip        heap.percent ram.percent cpu load_1m load_5m load_15m node.role master name
        127.0.0.1           44          81  69                          mdi       *      node-1
    GET /_cat/indices?v  列出所有的索引List All Indices
        结果示例：
            health status index                           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
            green  open   kibana_sample_data_ecommerce    mf04HLmHRzuu6lMblA9viw   1   0       4675            0      4.8mb          4.8mb
            green  open   .monitoring-kibana-6-2019.03.18 n4uUxG-_QRyXWlj7uWJmcg   1   0       1763            0    573.2kb        573.2kb
            green  open   .monitoring-kibana-6-2019.03.19 oVfmPrZDTW-eWExhufQhgQ   1   0       1633            0    978.3kb        978.3kb
            yellow open   twitter                         CngqWKrdT9CG692ZCk1mYg   5   1          2            0     13.4kb         13.4kb
            green  open   .kibana_1                       d9Qy17UFR2yGPIVrBA30iQ   1   0         18            0    897.1kb        897.1kb
            green  open   .monitoring-es-6-2019.03.18     g18YAvFqSJyZvfYb2o5bwA   1   0      15893          112      7.2mb          7.2mb
            green  open   .monitoring-es-6-2019.03.19     uCn08XYPQKKEq_lUcGLt8g   1   0      18104          112     15.7mb         15.7mb
    创建一个索引：
        PUT /customer?pretty
    索引一个文档
        PUT /customer/_doc/1?pretty
        {
          "name": "John Doe"
        }
        ES可以自动生成id，长度20个字符，URL安全，base64编码，GUID，分布式系统并行生成时不可能发生冲突    
    删除一个索引
        DELETE /customer?pretty
    更新一个文档
        POST /customer/_doc/1/_update?pretty
        {
          "doc": { "name": "Jane Doe", "age": 20 }
        }
        
        POST /customer/_doc/1/_update?pretty
        {
          "script" : "ctx._source.age += 5"
        }
        在上面的示例中，ctx._source指的是即将更新的当前源文档
    删除一个文档
        DELETE /customer/_doc/2?pretty

        不会立即物理删除，只会标记为deleted。当数据越来越多的时候，会在后台自动删除
    批量操作
        POST /customer/_doc/_bulk?pretty
        {"index":{"_id":"1"}}
        {"name": "John Doe" }
        {"index":{"_id":"2"}}
        {"name": "Jane Doe" }
        
        POST /customer/_doc/_bulk?pretty
        {"update":{"_id":"1"}}
        {"doc": { "name": "John Doe becomes Jane Doe" } }
        {"delete":{"_id":"2"}}
    查询操作
        GET /bank/_search?q=*&sort=account_number:asc&pretty
        结果示例：
            {
              "took" : 63,
              "timed_out" : false,
              "_shards" : {
                "total" : 5,
                "successful" : 5,
                "skipped" : 0,
                "failed" : 0
              },
              "hits" : {
                "total" : 1000,
                "max_score" : null,
                "hits" : [ {
                  "_index" : "bank",
                  "_type" : "_doc",
                  "_id" : "0",
                  "sort": [0],
                  "_score" : null,
                  "_source" : {"account_number":0,"balance":16623,"firstname":"Bradshaw","lastname":"Mckenzie","age":29,"gender":"F","address":"244 Columbus Place","employer":"Euron","email":"bradshawmckenzie@euron.com","city":"Hobucken","state":"CO"}
                }, {
                  "_index" : "bank",
                  "_type" : "_doc",
                  "_id" : "1",
                  "sort": [1],
                  "_score" : null,
                  "_source" : {"account_number":1,"balance":39225,"firstname":"Amber","lastname":"Duke","age":32,"gender":"M","address":"880 Holmes Lane","employer":"Pyrami","email":"amberduke@pyrami.com","city":"Brogan","state":"IL"}
                }, ...
                ]
              }
            }
        在上面的结果中：
            took - Elasticsearch执行搜索的时间（以毫秒为单位）
            timed_out - 告诉我们搜索是否超时
            _shards - 告诉我们搜索了多少个分片，以及搜索成功/失败分片的计数
            hits - 搜索结果
            hits.total - 符合我们搜索条件的文档总数
            hits.hits - 实际的搜索结果数组（默认为前10个文档）
            hits.sort - 对结果进行排序键（如果按分数排序则丢失）
            hits._score和max_score- 暂时忽略这些字段
        GET /bank/_search   替代请求正文方法的上述完全相同的搜索：
        {
          "query": { "match_all": {} },
          "sort": [
            { "account_number": "asc" }
          ]
        }
        Elasticsearch提供了一种JSON样式的特定于域的语言，可用于执行查询。这被称为 Query DSL。查询语言非常全面，乍一看可能令人生畏
        
        GET /bank/_search   可以指定接受某些字段，其余的不要
        {
          "query": { "match_all": {} },
          "_source": ["account_number", "balance"]
        }
        
        Aggregations 聚合操作
        GET /bank/_search
        {
          "size": 0,
          "aggs": {
            "group_by_state": {
              "terms": {
                "field": "state.keyword"
              }
            }
          }
        }
        在SQL中，上述聚合在概念上类似于：
        SELECT state, COUNT(*) FROM bank GROUP BY state ORDER BY COUNT(*) DESC LIMIT 10;
基本的写模型
    主分片遵循以下基本流程：
        1.验证传入操作并在结构无效时拒绝它（例如：有一个对象字段，其中包含一个数字）
        2. 在本地执行操作，即索引或删除相关文档。这也将验证字段的内容并在需要时拒绝（例如：关键字值太长，无法在Lucene中进行索引）。
        3. 将操作转发到当前同步副本集中的每个副本。如果有多个副本，则这是并行完成的。
        4. 一旦所有副本成功执行了操作并响应主服务器，主服务器就会确认成功完成对客户端的请求。
基本读模型
    1.将读取请求解析为相关分片。请注意，由于大多数搜索将被发送到一个或多个索引，因此它们通常需要从多个分片中读取，每个分片代表数据的不同子集。
    2.从分片复制组中选择每个相关分片的活动副本。这可以是主要副本或副本。默认情况下，Elasticsearch将简单地在分片副本之间循环。
    3.将分片级读取请求发送到所选副本。
    4.结合结果并做出回应。请注意，在通过ID查找的情况下，只有一个分片是相关的，可以跳过此步骤。

集群能力
	Elasticsearch 尽可能地屏蔽了分布式系统的复杂性。这里列举了一些在后台自动执行的操作：
		-分配文档到不同的容器或分片中，文档可以储存在一个或多个节点中
		-按集群节点来均衡分配这些分片，从而对索引和搜索过程进行负载均衡
		-复制每个分片以支持数据冗余，从而防止硬件故障导致的数据丢失
		-将集群中任一节点的请求路由到存有相关数据的节点
		-集群扩容时无缝整合新节点，重新分配分片以便从离群节点恢复
	服务器扩容：
		可以通过购买性能更强大（ 垂直扩容 ，或 纵向扩容 ） 或者数量更多的服务器（ 水平扩容 ，或 横向扩容 ）来实现。
聚合查询
	- Bucketing
	
	- Metric
	- Matrix
	- Pipeline

--------------------------------------------------------------------------------	

## Es分布式架构

### master节点

- 管理es集群的元数据：比如索引的创建和删除，维护索引元数据，节点的增加和移除，维护集群的元数据
- 默认情况下会自动选择出一台机器作为master节点
- master节点不承载所有的请求，所以不会是一个单点的瓶颈

### 节点对等的分布式架构

- 节点对等，去中心化，请求发给哪个节点都能处理

### 容错机制

#### master node宕机情况的容错
- master选举，自动选举另外一个node成为新的master，承担起master的责任来
- 新master，将丢失的primary shard的某个replica shard提升为primary shard，此时cluster status会变成yellow，因为primary shard全部都变成active了，但是少了一个replica shard，所以不是所有的replica shard都是active了
- 重启故障的node，new master ，会将缺失的副本都copy一份到该node上，而且该node会使用之前已有的shard数据，只是同步一下宕机之后发生过的修改

	
--------------------------------------------------------------------------------	
## Elastic客户端
- Java REST Client
  - Java Low Level REST Client:   
	  Elasticsearch的官方低级客户端。它允许通过http与Elasticsearch集群通信。Leaves请求编组并响应用户的编组。它与所有Elasticsearch版本兼容。
  - Java Hight Level REST Client:  
    Elasticsearch的官方高级客户端。它基于低级客户端，公开API特定方法，并负责编组请求编组和响应非编组。
- Java API
- JavaScript API
- GO API
- .NET API 
- PHP API 
- Perl API
- Python API
- Ruby API
- Community Contributed Clients
	
		
------------------------------------------------------------------------------
## 数据同步到ES

### Mysql数据同步到Elasticsearch方案
    https://www.itcodemonkey.com/article/4786.html
    1. 以同步mysql binlog的方式实时同步数据到ES的思路，要通过mysql binlog将数据同步到ES集群，只能使用ROW模式，因为只有ROW模式才能知道mysql中的数据的更改。
        https://cloud.tencent.com/developer/article/1145942
        1.1 mysqldump工具
        1.2 使用go-mysql-elasticsearch开源工具同步数据到ES
            go-mysql-elasticsearch 是国内作者开发的一款插件
            其由go语言开发，编译及使用非常简单。go-mysql-elasticsearch的原理很简单，
            首先使用mysqldump获取当前MySQL的数据，然后在通过此时binlog的name和position获取增量数据，再根据binlog构建restful api写入数据到ES中
            优点
                能实现mysql数据增加,删除,修改操作的实时数据同步
            缺点
                无法实现数据全量同步Elasticsearch
                仍处理开发、相对不稳定阶段
        1.3 使用mypipe同步数据到ES集群
        1.4 使用canal+kafka同步数据到ES集群
    2. 以定时抓取数据库变动的数据同步的ES的思路，这个方式的通病是不能同步删除的数据
        2.1 logstash-input-jdbc
            logstash官方插件,集成在logstash中,下载logstash即可,通过配置文件实现mysql与elasticsearch数据同步
            优点
                能实现mysql数据全量和增量的数据同步,且能实现定时同步.
                版本更新迭代快,相对稳定.
                作为ES固有插件logstash一部分,易用
            缺点
                不能实现同步删除操作,MySQL数据删除后Elasticsearch中数据仍存在.
                同步最短时间差为一分钟,一分钟数据同步一次,无法做到实时同步.
        2.2 elasticsearch-jdbc
            目前最新的版本是2.3.4，支持的ElasticSearch的版本为2.3.4, 未实践
            优点
                能实现mysql数据全量和增量的数据同步.
            缺点
                目前最新的版本是2.3.4，支持的ElasticSearch的版本为2.3.4
                不能实现同步删除操作,MySQL数据删除后Elasticsearch中数据仍存在.
        2.3 Apache-NiFi实现mysql数据与elasticsearch同步
            NiFi之前是在美国国家安全局（NSA）开发和使用了8年的一个可视化、可定制的数据集成产品。2014年NSA将其贡献给了Apache开源社区，2015年7月成功成为Apache顶级项目。
        2.4 程序定时器定时抓取一定时间内修改的数据
		
-------------------------------------------------------------		
## elasticsearch实际开发过程中遇到的问题

1. 【版本5.6】相同的index下，虽然可以建立不同的mapping但是，各个mapping里面如果相同的filed的话，filed的类型也必须一样，
	个人感觉mapping只是在index的filed上做了一层封装而已，实际是用的同一个filed


## ES常用优化手段

- 批量导入大量数据的时候 暂时关闭refresh， 关闭副本， refresh_interval=-1,index.number_of_replicas=0
- 多线程写入写入线程数一般和机器数相当
- 用bulk比单条的PUT/DELETE操作索引的效率更高
- 增加索引刷新间隔 refresh_interval，默认1s，建议改成30s
- 禁用linux机器的swapping
- 尽量不使用脚本 性能很差
- 磁盘使用ssd
- Lucene需要使用JVM的堆外内存，官方建议，留给Lucene一半的系统内存
- 不需要排序、聚合、脚本中使用的字段禁用doc_values
- 不需要打分的keyword或text字段 禁用norms
- 评分消耗资源，如果不需要可使用filter过滤来达到关闭评分功能，score则为0，如果使用constantScoreQuery则score为1。个人通过压测后发现性能提升很大
- 关闭不需要查询字段的_source功能，不将此存储在ES中以节省磁盘空间. 个人感觉这种优化不是太好，到时候不知道字段对应的值，没法排查问题
- 关于合并被标记删除的记录，设置为0表示在合并时一定删除被标记记录，默认应大于10%才删除："index.merge.policy.expunge_deletes_allowed":"0"。
- 合并线程数默认是：Math.max(1, Math.min(4, Runtime.getRuntime().availableProcessors()/2))，若是机械磁盘，可设置为1：index.merge.scheduler.max_thread_count: 1. 
- 尽量使用keyword替代一些long或者int之类，term查询总比range查询好 (参考lucene说明：http://lucene.apache.org/core/7_4_0/core/org/apache/lucene/index/PointValues.html)。(待验证)
- 分页：
  - from + size: 每分片检索结果数最大为 from + size，假设from = 20, size = 20，则每个分片需要获取20 * 20 = 400条数据，多个分片的结果在协调节点合并(假设请求的分配数为5，则结果数最大为 400*5 = 2000条) 再在内存中排序后然后20条给用户。这种机制导致越往后分页获取的代价越高，达到50000条将面临沉重的代价，默认from + size默认如下：index.max_result_window ：10000。
  - search_after:  使用前一个分页记录的最后一条来检索下一个分页记录，在我们的案例中，首先使用from+size，检索出结果后再使用search_after，有个条件是search_after的值必须是唯一的
  - scroll 用于大结果集查询，缺陷是需要维护scroll_id。