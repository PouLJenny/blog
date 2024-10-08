# Arthas

## 简介

[官网](https://arthas.aliyun.com/ '')


## 获取某个类的实例

```shell
vmtool --action getInstances -c 31cefde0 --className org.apache.http.impl.conn.PoolingHttpClientConnectionManager
```

## 执行某个实例的方法

```shell
vmtool --action getInstances -c 31cefde0 --className org.apache.http.impl.conn.PoolingHttpClientConnectionManager  --express '#val=instances[0],#val.getTotalStats()'
```