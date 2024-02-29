# ES优化记录


## 查询优化

### 优化手段-消除打分的性能消耗
优化前后对比 2021-08-26 20:13 上线


![优化前后对比-整体请求量](../static/images/elasticsearch/es_optmize_search0.png '优化前后对比-整体请求量')

![优化前后对比-load](../static/images/elasticsearch/es_optmize_search1.png 'load')

![优化前后对比-最大响应时间](../static/images/elasticsearch/es_optmize_search2.png '优化前后对比-最大响应时间')

![优化前后对比-TP999](../static/images/elasticsearch/es_optmize_search3.png '优化前后对比-TP999')



## 写入优化

### 优化手段-写入转异步批处理

优化前后对比 2021-09-01 18:29 上线

优化前
![优化前-索引QPS](../static/images/elasticsearch/es_optmize_index1.png '优化前-索引QPS')
![优化前-load](../static/images/elasticsearch/es_optmize_index2.png '优化前-load')

优化后
![优化后-索引QPS](../static/images/elasticsearch/es_optmize_index3.png '优化后-索引QPS')
![优化后-load](../static/images/elasticsearch/es_optmize_index4.png '优化后-load')

优化前后整体load对比
![优化前-整体load](../static/images/elasticsearch/es_optmize_index6.png '优化前-整体load')
![优化后-整体load](../static/images/elasticsearch/es_optmize_index5.png '优化后-整体load')
