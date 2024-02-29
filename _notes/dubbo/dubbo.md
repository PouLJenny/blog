# Dubbo

[官网](https://dubbo.apache.org/ )

[github](https://github.com/apache/dubbo )


## 集群容错机制

- failover 默认的方式
    失败自动切换，当出现失败，重试其它服务器。通常用于读操作，但重试会带来更长延迟。可通过 retries="2" 来设置重试次数(不含第一次)。
    ```xml
    <dubbo:reference cluster="failover" retries="2" id="greetingsService" check="true" interface="org.apache.dubbo.samples.api.GreetingsService"/>
    ```
- failfast
    快速失败，只发起一次调用失败立即报错。通常用于非幂等性的写操作，比如新增记录。
    ```xml
    <dubbo:reference cluster="failfast" id="greetingsService" check="true" interface="org.apache.dubbo.samples.api.GreetingsService" timeout="200"/>
    ```
- failsafe
    失败安全，出现异常时，直接忽略。通常用于写入审计日志等操作
    ```xml
    <dubbo:reference cluster="failsafe" id="greetingsService" check="true" interface="org.apache.dubbo.samples.api.GreetingsService" timeout="200"/>
    ```

    实际测试会打印warn的报错日志，线程继续执行
- failback
    失败自动恢复，后台记录失败请求，定时重发。通常用于消息通知操作
    ```xml
    <dubbo:reference cluster="failback" id="greetingsService" check="true" interface="org.apache.dubbo.samples.api.GreetingsService" timeout="200"/>
    ```
    实际测试会打印warn的报错日志，线程继续执行。而且会定时的重发请求。
    但是这个地方有个问题，定时重发，是定的多长时间？会一直重发吗？TODO
- forking
    并行调用多个服务器，只要一个成功即返回。通常用于实时性要求较高的读操作，但需要浪费更多服务资源。可通过`forks="2"`来设置并行的最大值
    ```xml
    <dubbo:reference cluster="forking" forks="2" id="greetingsService" check="true" interface="org.apache.dubbo.samples.api.GreetingsService" timeout="200"/>
    ```
- broadcast
    广播调用所有提供者，逐个调用，任意一台报错就报错。通常用于通知所有提供者更新缓存或日志等本地资源信息
    ```xml
    <dubbo:reference cluster="broadcast" id="greetingsService" check="true" interface="org.apache.dubbo.samples.api.GreetingsService" timeout="200"/>
    ```
- available
    调用目前可用的实例，如果没有可用的实例，则抛出异常。通常用于不需要负载均衡的场景
    ```xml
    <dubbo:reference cluster="available" id="greetingsService" check="true" interface="org.apache.dubbo.samples.api.GreetingsService" timeout="200"/> 
    ```

    实际测试中，不太清楚怎么定义`available`，需要看源码来确认一下？TODO
- mergeable
    将集群中的调用结果聚合起来返回结果，通常和group一起配合使用。通过分组对结果进行聚合并返回聚合后的结果，比如菜单服务，用group区分同一接口的多种实现，在消费方需从每种group中调用一次并返回结果，对结果进行合并之后返回，这样就可以实现聚合菜单项。
    ```xml
    <dubbo:reference cluster="mergeable" id="greetingsService" check="true" interface="org.apache.dubbo.samples.api.GreetingsService" timeout="200"/>
    ```

    实际测试并没有出现官方说的情况，group都区分了，相当于环境都是隔离的了，这个要怎么调用呢?TODO
- zoneaware cluster
    多注册中心订阅的场景，注册中心集群间的负载均衡。对于多注册中心间的选址策略有如下四种

    1. 指定优先级：preferred="true"注册中心的地址将被优先选择
    ```xml
    <dubbo:registry address="zookeeper://127.0.0.1:2181" preferred="true" />
    ```

    2. 同中心优先：检查当前请求所属的区域，优先选择具有相同区域的注册中心
    ```xml
    <dubbo:registry address="zookeeper://127.0.0.1:2181" zone="beijing" />
    ```

    3. 权重轮询：根据每个注册中心的权重分配流量
    ```xml
    <dubbo:registry id="beijing" address="zookeeper://127.0.0.1:2181" weight="100" />

    <dubbo:registry id="shanghai" address="zookeeper://127.0.0.1:2182" weight="10" />
    ```

    4. 缺省值：选择一个可用的注册中心


实际测试的时候，如果提供方的方法中直接抛出`RuntimeExeption`的话，上面的集群配置模式是直接不生效的，现象是调用方直接线程抛异常，线程结束。 这个需要研究下源码看看为啥。



