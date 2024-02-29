# Spring Cloud Alibaba


## 特性

- 服务限流降级
    默认支持 WebServlet、WebFlux、OpenFeign、RestTemplate、Spring Cloud Gateway、Dubbo 和 RocketMQ 限流降级功能的接入，可以在运行时通过控制台实时修改限流降级规则，还支持查看限流降级 Metrics 监控。
- 服务注册与发现
    适配 Spring Cloud 服务注册与发现标准，默认集成对应 Spring Cloud 版本所支持的负载均衡组件的适配。
- 分布式配置管理
    支持分布式系统中的外部化配置，配置更改时自动刷新。
- 消息驱动能力
    基于 Spring Cloud Stream 为微服务应用构建消息驱动能力。
- 分布式事务
    使用 @GlobalTransactional 注解， 高效并且对业务零侵入地解决分布式事务问题。


## 组件

- Sentinel
    把流量作为切入点，从流量控制、熔断降级、系统负载保护等多个维度保护服务的稳定性。
- Nacos
    一个更易于构建云原生应用的动态服务发现、配置管理和服务管理平台。
- Seata
    阿里巴巴开源产品，一个易于使用的高性能微服务分布式事务解决方案。
- Alibaba Cloud SchedulerX
    阿里中间件团队开发的一款分布式任务调度产品，提供秒级、精准、高可靠、高可用的定时（基于 Cron 表达式）任务调度服务。
- RocketMQ
    一款开源的分布式消息系统，基于高可用分布式集群技术，提供低延时的、高可靠的消息发布与订阅服务。


