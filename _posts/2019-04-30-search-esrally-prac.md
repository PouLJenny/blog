---
layout: post
title:  "Elasticsearch压测工具-esrally"
date:   2019-04-30 10:00:00 +0800
categories: elasticsearch esrally
tags: elasticsearch esrally
permalink: /search/esrally-prac
published: true
publish_file: 2019-04-30-search-esrally-prac.md
toc: true
---

# Elasticsearch压测工具-esrally

在搭建ES集群的时候，如果你想知道自己的ES集群的性能是怎么样的，到底能经受多大的请求压力。esrally可以满足你的愿望。

1. 环境要求
	Python 3.4+ including pip3
	git 1.9+
	jdk 并且已配置JAVA_HOME环境变量
2. 安装
	
	```shell
	pip3 install esrally
	```
3. 运行前的简单配置
	```shell
	esrally configure --advanced-config
	```
   
	|  配置项| 描述 |
	|--|--|
	|  Benchmark root directory|rally将所有基准相关数据存储在此目录中，最多可能需要几十GB。如果要使用专用分区，可以在此处指定其他根目录  |
	|  Elasticsearch project directory| 这是Elasticsearch源码所在的目录 |

4. 运行一个简单的基准测试

	```shell
	esrally --distribution-version=6.5.3
	```
5. 概念
	rally是拉力赛的意思，其中很多的概念也是来自于拉力赛
	跑道（Tracks），查看所有的跑到
	

	```shell
	esrally list tracks	
	```
	
	下面是结果

	

	```
	Available tracks:
	
	Name           Description                                                                                                                                                                        Documents    Compressed Size    Uncompressed Size    Default Challenge        All Challenges
	-------------  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  -----------  -----------------  -------------------  -----------------------  ---------------------------------------------------------------------------------------------------------------------------
	metricbeat     Metricbeat data                                                                                                                                                                    1,079,600    87.6 MB            1.2 GB               append-no-conflicts      append-no-conflicts
	percolator     Percolator benchmark based on AOL queries                                                                                                                                          2,000,000    102.7 kB           104.9 MB             append-no-conflicts      append-no-conflicts
	pmc            Full text benchmark with academic papers from PMC                                                                                                                                  574,199      5.5 GB             21.7 GB              append-no-conflicts      append-no-conflicts,append-no-conflicts-index-only,append-sorted-no-conflicts,append-fast-with-conflicts
	nyc_taxis      Taxi rides in New York in 2015                                                                                                                                                     165,346,692  4.5 GB             74.3 GB              append-no-conflicts      append-no-conflicts,append-no-conflicts-index-only,append-sorted-no-conflicts-index-only,update,append-ml
	geopoint       Point coordinates from PlanetOSM                                                                                                                                                   60,844,404   481.9 MB           2.3 GB               append-no-conflicts      append-no-conflicts,append-no-conflicts-index-only,append-fast-with-conflicts
	noaa           Global daily weather measurements from NOAA                                                                                                                                        33,659,481   947.3 MB           9.0 GB               append-no-conflicts      append-no-conflicts,append-no-conflicts-index-only
	so             Indexing benchmark using up to questions and answers from StackOverflow                                                                                                            36,062,278   8.9 GB             33.1 GB              append-no-conflicts      append-no-conflicts
	geoshape       Shapes from PlanetOSM                                                                                                                                                              60,523,283   13.4 GB            45.4 GB              append-no-conflicts      append-no-conflicts
	http_logs      HTTP server log data                                                                                                                                                               247,249,096  1.2 GB             31.1 GB              append-no-conflicts      append-no-conflicts,append-no-conflicts-index-only,append-sorted-no-conflicts,append-index-only-with-ingest-pipeline,update
	nested         StackOverflow Q&A stored as nested docs                                                                                                                                            11,203,029   663.1 MB           3.4 GB               nested-search-challenge  nested-search-challenge,index-only
	geopointshape  Point coordinates from PlanetOSM indexed as geoshapes                                                                                                                              60,844,404   470.5 MB           2.6 GB               append-no-conflicts      append-no-conflicts,append-no-conflicts-index-only,append-fast-with-conflicts
	geonames       POIs from Geonames                                                                                                                                                                 11,396,505   252.4 MB           3.3 GB               append-no-conflicts      append-no-conflicts,append-no-conflicts-index-only,append-sorted-no-conflicts,append-fast-with-conflicts
	eventdata      This benchmark indexes HTTP access logs generated based sample logs from the elastic.co website using the generator available in https://github.com/elastic/rally-eventdata-track  20,000,000   755.1 MB           15.3 GB              append-no-conflicts      append-no-conflicts
	```
		
	
	你可以指定赛道和挑战
	

	```shell
	esrally --distribution-version=6.0.0 --track=geopoint --challenge=append-fast-with-conflicts
	```
	
	由于生成的基准测试比较大屏幕显示不了，可以将报告指定到一个目录，追加参数
	

	```shell
	--report-file=/path/to/your/report.md
	```
	报告文件默认是md格式的，也可以指定为csv格式的，追加参数
	```shell
	--report-format=csv
	```

	如果你想测试已经存在的ES集群
	

	```shell
	esrally  race  --track=geonames  --target-hosts=10.5.5.10:9200,10.5.5.11:9200,10.5.5.12:9200 --pipeline=benchmark-only
	```
	
	如果您 启用了X-Pack安全性，那么您还需要指定另一个参数来使用https并传递凭据：
	

	```shell
	esrally  --target-hosts=10.5.5.10:9243,10.5.5.11:9243,10.5.5.12:9243 --pipeline=benchmark-only --client-options="use_ssl:true,verify_certs:true,basic_auth_user:'elastic',basic_auth_password:'changeme'"
	```
	
	下面是我自己电脑得到的报告，报告篇幅比较长这里只截取了一小段：
	
	![](/assets/notes/elasticsearch/esrally-prac-01.png)


友情链接：

[esrally github](https://github.com/elastic/rally)

[esrally 官方文档地址](https://esrally.readthedocs.io/en/stable/)