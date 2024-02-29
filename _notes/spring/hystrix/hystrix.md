# Histrix

[github](https://github.com/Netflix/Hystrix '')
[netfix techblog](https://netflixtechblog.com/ '')

## 简介

隔离、熔断、限流、降级、运维监控

高可用： 在各种系统的各个地方有乱七八糟的异常和故障的情况下，整个服务还能继续健康的工作。理想状况下，软件的故障，就不应该导致整个系统的崩溃，服务器硬件的一些故障，服务的冗余可以解决

## 设计原则

![整体](../../static/images/hystrix/top1.png "顶级")
![](../../static/images/hystrix/top2.png "")
![](../../static/images/hystrix/top_follow_chart.png "")


## How do we respond to a user request when failure occurs?

Some approaches to fallbacks we use are, in order of their impact on the user experience:
- Cache: Retrieve data from local or remote caches if the realtime dependency is unavailable, even if the data ends up being stale
- Eventual Consistency: Queue writes (such as in SQS) to be persisted once the dependency is available again
- Stubbed Data: Revert to default values when personalized options can’t be retrieved
- Empty Response (“Fail Silent”): Return a null or empty list which UIs can then ignore


![](../../static/images/hystrix/example_use_case.png "")


## How Does Hystrix Accomplish Its Goals?
Hystrix does this by:

- Wrapping all calls to external systems (or “dependencies”) in a **HystrixCommand** or **HystrixObservableCommand** object which typically executes within a separate thread (this is an example of the command pattern).
- Timing-out calls that take longer than thresholds you define. There is a default, but for most dependencies you custom-set these timeouts by means of “properties” so that they are slightly higher than the measured 99.5th percentile performance for each dependency.
- Maintaining a small thread-pool (or semaphore) for each dependency; if it becomes full, requests destined for that dependency will be immediately rejected instead of queued up.
- Measuring successes, failures (exceptions thrown by client), timeouts, and thread rejections.
- Tripping a circuit-breaker to stop all requests to a particular service for a period of time, either manually or automatically if the error percentage for the service passes a threshold.
- Performing fallback logic when a request fails, is rejected, times-out, or short-circuits.
- Monitoring metrics and configuration changes in near real-time.


## How it works?

![](../../static/images/hystrix/hystrix-command-flow-chart.png "")


## Use

