# Feign

## 核心组件

- 编码器（Encoder）
    - 调用接口时，将传递的对象编码，序列化
- 解码器（Decoder）
    - 接收请求时，将接收到的数据进行解码，转换成对象
- Logger 
    - 打印日志的，Feign是负责调用Http接口的，可以打印请求日志
- Contract
    - 契约组件，可用来解释Spring MVC的一些注解 @RequestParam
- Feign.Builder 
    - Feign客户端的一个实例构造器
- FeignClient
    - 就是我们使用Feign最最核心的入口    


## 源码阅读

### 入口

1. Application启动类上的注解 @EnableFeignClients
2. 接口上的注解 @FeignClient


![feign client入口图示](../../static/images/feign/feign-client-start.png 'feign client入口图示')


### 超时时间和重试的配置

微服务的架构中需要配置服务间调用的超时时间，


超时、重试、隔离、熔断、限流、降级