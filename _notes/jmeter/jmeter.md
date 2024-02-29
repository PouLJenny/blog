# Jmeter

## 简介

[官网](https://jmeter.apache.org/ '')


### 压测dubbo接口

Jmeter自带的是没有dubbo协议的，需要写插件

Dubbo社区已经写好插件了[jmeter-plugins-for-apache-dubbo](https://github.com/thubbo/jmeter-plugins-for-apache-dubbo '')，我们直接拿来用就ok了。

#### 安装dubbo插件

1. `git clone https://github.com/thubbo/jmeter-plugins-for-apache-dubbo.git`
2. `mvn clean install`
3. 将插件copy到 `${JMETER_HOME}\lib\ext`

#### 编写Jmeter脚本
${__P(zk.address,192.168.20.35:2181\,192.168.20.230:2181\,192.168.20.157:2181)}


## 命令行运行

```shell
jmeter -n -t boss-crm-customer-info.jmx -l test_preon.jtl -Jloop.count=-1  -Jtqs=100 -JmaxId=14570720 -Jrequest.scheme=http  -Jrequest.host=127.0.0.1 -Jrequest.port=8580 -Jdb.env=boss_crm_prod -Jthreads.num=50 -Jduration=1200 -Jcookie.jsessionid=9F33DEC82A1410DCF75B5C2528101060 -Jcookie.t_crm=Qh9bYKmRzE6p9h  -Jcookie.t_zp_crm=wPdz9aRnfm2SD4  -e -o dashboard
```
