# ES安装

## docker

compose文件(`es-kibana-compose.yml`)如下
```yml
version: '2.2'
services:
  es01:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.9
    container_name: es01
    hostname: es01
    environment:
      node.name: es01
      cluster.name: es-cluster
      discovery.type: single-node
    networks:
      - elastic
    ports:
      - "9200:9200"
      - "9300:9300"
  kibana01:
    image: docker.elastic.co/kibana/kibana:7.17.9
    container_name: kibana01
    hostname: kibana01
    networks:
      - elastic
    ports:
      - "5601:5601"
    links:
      - es01
    environment:
      ELASTICSEARCH_HOSTS: http://es01:9200

networks:
  elastic:
    driver: bridge
```



启动
```shell
docker-compose -f es-kibana-compose.yml up
```
加上参数`-d`可以后台执行
```shell
docker-compose -f es-kibana-compose.yml up -d
```

停止
```shell
docker-compose -f es-kibana-compose.yml down
```