# Elasticsearch  基础使用


## Lucene

ES是基于Lucene之上，封装了开箱即用的分布式功能，可轻松搭建一套高可用的搜索集群。

[官网](http://lucene.apache.org '')

[GitHub](https://github.com/apache/lucene '')

## 倒排索引

![倒排索引数据结构](../static/images/lucene/lucene.png "倒排索引数据结构")

“倒排索引”Inverted index。一个未经处理的数据库中，一般是以文档ID作为索引，以文档内容作为记录。
而Inverted index 指的是将单词或记录作为索引，将文档ID作为记录，这样便可以方便地通过单词或记录查找到其所在的文档。

## Kibana

[官方文档](https://www.elastic.co/guide/en/kibana/7.3/introduction.html '')

dev tools

stack monitoring

## Elastic

[官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/7.3/elasticsearch-intro.html '官方文档')

### 概念

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
  为加入一个名为elasticsearch的集群，这意味着如果您在网络上启动了许多节点并且假设它们可以相互发现 - 它们将自动形成并加入一
  个名为elasticsearch的集群。
  在单个群集中，您可以拥有任意数量的节点。此外，如果您的网络上当前没有其他Elasticsearch节点正在运行，则默认情况下启动单个节点将形
  成一个名为elasticsearch的新单节点集群。
- Index
  - 索引是具有某些类似特征的文档集合。例如，您可以拥有客户数据的索引，产品目录的另一个索引以及订单数据的另一个索引。索引由名称标识（必须全部为小写），
  并且此名称用于在对其中的文档执行索引，搜索，更新和删除操作时引用索引。
  在单个群集中，您可以根据需要定义任意数量的索引。
- Type
  - 在7.0.0后弃用。
  一种类型，曾经是索引的逻辑类别/分区，允许您在同一索引中存储不同类型的文档，例如一种类型用于用户，另一种类型用于博客帖子。不
  再可能在索引中创建多个类型，并且将在更高版本中删除类型的整个概念。
- Mapping  
  - 定义Document包含哪些字段，以及字段的行为和属性
  - [mapping-types官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/7.3/mapping.html '')
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
  
  副本分片很重要，主要有两个原因：
    1. 它在碎片/节点出现故障时提供高可用性。因此，请务必注意，副本分片永远不会在与从中复制的原始/主分片相同的节点上分配。
    2. 它允许您扩展搜索量/吞吐量，因为可以在所有副本上并行执行搜索。

  总而言之，每个索引可以拆分为多个分片。索引也可以复制为零（表示没有副本）或更多次。复制后，每个索引都将具有主分片（从中复制的原始分片）
  和副本分片（主分片的副本）。可以在创建索引时为每个索引定义分片和副本的数量。创建索引后，您还可以随时动态更改副本数。
  您可以使用`_shrink`和`_split` API 更改现有索引的分片数，但这不是一项简单的任务，预先计划正确数量的分片是最佳方法。
  默认情况下，Elasticsearch中的每个索引都分配了5个主分片和1个副本，这意味着如果群集中至少有两个节点，
  则索引将包含5个主分片和另外5个副本分片（1个完整副本），总计为每个索引10个分片。
  

  **注意**：
    每个Elasticsearch分片都是Lucene索引。单个Lucene索引中可以包含最多文档数。
    限制是2,147,483,519（= Integer.MAX_VALUE - 128）文档。您可以使用`_cat/shards` API 监控分片大小。

    ![源码限制](../static/images/lucene/lucene_max_doc.png "源码限制") 


### Rest API

#### 创建一个index
```
PUT /test_index
{
  "settings": {
    "index":{
      "number_of_shards":5,
      "number_of_replicas":1,
      "refresh_interval":"1s",
      "mapping.nested_objects.limit":"10000000",
      "max_result_window":"10000000"
    }
  },
  "mappings": {
    "properties": {
      "id":{
        "type": "long",
        "index": true
      },
      "f_integer":{
        "type": "integer",
        "index": true
      },
      "f_keyword":{
        "type": "keyword",
        "index": true
      },
      "f_keyword_2":{
        "type": "keyword",
        "index": true
      },
      "f_text":{
        "type": "text",
        "index": true,
        "analyzer": "standard"
      },
      "f_date":{
        "type": "date",
        "index": true,
        "format": "yyyy-MM-dd HH:mm:ss"
      },
      "f_geo":{
        "type": "geo_point",
        "index": true
      },
      "f_nested":{
        "type": "nested", 
        "properties": {
          "id":{
            "type":"long"
          },
          "f_keyword":{
            "type":"keyword"
          }
        }
      }
    }
  }
}
```
#### 查询index的setting
```
GET /test_index/_settings
```

#### 修改inex的setting
```
PUT /test_index/_settings
{
  "index" : {
      "refresh_interval":"30s"
  }
}
```
#### 删除index

```
DELETE /test_index

# 查询index是否还存在
HEAD /test_index
```

#### 查询所有的index
```
GET _cat/indices?v&s=index
```

#### 更新mapping

添加新的字段，或者是更新已有字段的搜索设置
```
PUT /test_index/_mapping
{
  "properties":{
    "f_new":{
      "type":"byte",
      "index":true
    }
  }
}
```

#### 添加文档

替换文档内容
```
POST /test_index/_doc/1
{
  "id":1,
  "f_keyword":"keyword",
  "f_text":"BOSS直聘",
  "f_date":"2021-09-09 00:00:00",
  "f_geo":{
    "lat":37.1,
    "lon":110
  },
  "f_nested":{
    "id":11
  }
}
```

错误的日期格式
```
POST /test_index/_doc/2
{
  "id":2,
  "f_date":"2021-09-09"
}
```

#### 更新文档

```
POST /test_index/_update/1
{
  "doc": {
    "f_keyword":"f_keyword_update"
  }
}
```

文档不存在时创建
```
POST /test_index/_update/4
{
  "doc": {
    "f_keyword":"f_keyword_update"
  },
  "upsert": {
    "f_keyword":"f_keyword_update"
  }
}
```

#### 删除文档

```
DELETE /test_index/_doc/1
```

#### refresh_interval

手动刷新
```
POST /test_index/_refresh
```

#### 查询所有
[官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/7.3/query-dsl-range-query.html '')

```
GET /test_index/_search
{
  "query": {
    "match_all": {}
  },
  "from": 0,
  "size": 20
}
```

只查询某些字段

```
GET /test_index/_search
{
  "_source": ["id"], 
  "query": {
    "match_all": {}
  }
}
```

#### 搜索-term

类似数据库的等于操作
```
GET /test_index/_search
{
  "query": {
    "term": {
      "f_keyword": {
        "value": "f_keyword_update"
      }
    }
  }
}
```

#### 搜索-terms
类似数据库的in操作

```
GET /test_index/_search
{
  "query": {
    "terms": {
      "id": [
        "1",
        "2"
      ]
    }
  }
}
```

#### 范围查询

```
GET /test_index/_search
{
  "query": {
    "range": {
      "f_date": {
        "gte": "2021-09-09 00:00:00",
        "lte": "2021-09-10 00:00:00",
        "format": "yyyy-MM-dd HH:mm:ss"
      }
    }
  }
}
```

#### Geo查询

```
GET /test_index/_search
{
  "query": {
    "geo_distance":{
      "distance":"2km",
      "f_geo":"37.1001,110"
    }
  }
}
```

#### 全文搜索-match/multi match

```
GET /test_index/_search
{
  "query": {
    "match": {
      "f_text": "直"
    }
  }
}

GET /test_index/_search
{
  "query": {
    "multi_match": {
      "query": "聘直",
      "fields": ["f_text","f_keyword"]
    }
  }
}
```

#### match phrase

类似数据库的like操作

```
GET /test_index/_search
{
  "query": {
    "match": {
      "f_text": "聘直"
    }
  }
}

GET /test_index/_search
{
  "query": {
    "match_phrase": {
      "f_text": "聘直"
    }
  }
}
```

#### 分词器 standard

```
POST _analyze
{
  "tokenizer": "standard",
  "text":      "BOSS直聘"
}
```

#### 高亮查询

```
GET /test_index/_search
{
  "query": {
    "match": {
      "f_text": "聘直"
    }
  },
  "highlight": {
    "pre_tags" : ["<tag1>"],
    "post_tags" : ["</tag1>"],
    "fields":{
      "*":{}
    }
  }
}
```


#### exists查询

判断字段是否存在
```
GET /test_index/_search
{
  "query": {
    "exists": {
      "field": "id"
    }
  }
}
```
#### nested查询

```
GET /test_index/_search
{
  "query": {
   "nested": {
     "path": "f_nested",
     "query": {
       "term": {
         "f_nested.id": {
           "value": "11"
         }
       }
     }
   }
  }
}
```



#### 组合查询-BooleanQuery

must = &&
shuld = ||
must_not = !

```
GET /test_index/_search
{
  "query": {
   "bool": {
     "must": [
        {
          "term": {
            "id": {
              "value": "1"
            }
          }
        },
        {
          "range": {
            "id": {
              "gte": 1,
              "lte": 2
            }
          }
        }
     ]
   } 
  }
}
```


查询不存在某个字段
```
GET /test_index/_search
{
  "query": {
   "bool": {
     "must_not": [
       {
         "exists": {
           "field": "id"
         }
       }
     ]
   } 
  }
}
```

#### 排序

```
GET /test_index/_search
{
  "query": {
    "match_all": {}
  }
  ,"sort": [
    {
      "id": {
        "order": "desc"
      },
      "f_nested.id":{
        "order": "desc",
        "nested": {
           "path":"f_nested"
        }
      }
    }
  ]
}
```

## 写代码



### 添加配置

```conf
## es
spring.elasticsearch.cluster-nodes=192.168.20.57:9200,192.168.20.130:9200,192.168.20.233:9200
spring.elasticsearch.user-name=elastic
spring.elasticsearch.password=hSs5mMzNA0Y~
```

### 引入包

如果是zhipin-crm项目或者是boss-crm的这种spring-mvc项目 
pom.xml里面直接引入下面的依赖
```xml
<properties>
    <zhipin-crm-version>RELEASE</zhipin-crm-version>
</properties>
<dependencies>
    <dependency>
        <groupId>com.zhipin</groupId>
        <artifactId>zhipin-crm-base-elasticsearch</artifactId>
        <version>${zhipin-crm-version}</version>
    </dependency>
</dependencies>
```

如果是其它的spring-boot项目
```xml
<properties>
    <zhipin-crm-version>RELEASE</zhipin-crm-version>
    <elasticsearch-version>7.3.2</elasticsearch-version>
</properties>
<dependencies>
    <dependency>
        <groupId>com.zhipin</groupId>
        <artifactId>zhipin-crm-base-elasticsearch</artifactId>
        <version>${zhipin-crm-version}</version>
    </dependency>
    <dependency>
        <groupId>org.elasticsearch</groupId>
        <artifactId>elasticsearch</artifactId>
        <version>${elasticsearch-version}</version>
    </dependency>
    <dependency>
        <groupId>org.elasticsearch.client</groupId>
        <artifactId>elasticsearch-rest-high-level-client</artifactId>
        <version>${elasticsearch-version}</version>
    </dependency>
    <dependency>
        <groupId>org.elasticsearch.client</groupId>
        <artifactId>elasticsearch-rest-client</artifactId>
        <version>${elasticsearch-version}</version>
    </dependency>
    <dependency>
        <groupId>org.elasticsearch.client</groupId>
        <artifactId>elasticsearch-rest-client-sniffer</artifactId>
        <version>${elasticsearch-version}</version>
    </dependency>
</dependencies>
```

### 主要类

`com.zhipin.crm.base.elasticsearch.EsClientOldAdapter`

索引项目； boss-crm-pgreplication
查询。。

es和java之间的序列化用的是Jackson，es的索引对象尽量不要用DO
