# Sharding Sphere

[官网](https://shardingsphere.apache.org/index_zh.html )
[github](https://github.com/apache/shardingsphere )

## ShardingSphere-JDBC

其实本质上的原理是把具体执行的**sql转换成抽象语法树**，然后把表名替换成分库分表后的表名、库名

转换成抽象语法树这一步骤用的是 ANTLR的开源组件

### 源码阅读

