## 分布式系统的熔断和限流 

### 限流算法

#### 固定窗口
操作步骤
- 时间划分为n个独立且固定大小的窗口，
- 每个窗口维护一个计数器，设置阈值上限
- 落在每一个时间窗口内的请求，来一个 计数器+1 ，当计数器超过阈值时 驳回落在当前时间窗口内的请求

redis实现
每个时间窗口维护一个key 做incr操作
#### 滑动窗口
操作步骤
- 将单位时间划分为
#### 漏桶算法

#### 令牌桶算法


### 怎么做限流？？

### 开源框架

- hystrix 
    - [github][hystrix-github] 好几年没更新了
- resilience4j
    - [github][resilience4j-github]
- sentinel
    - [github][sentinelv-github] 



[hystrix-github]: https://github.com/Netflix/Hystrix ""
[resilience4j-github]: https://github.com/resilience4j/resilience4j ""
[sentinelv-github]: https://github.com/alibaba/Sentinel ""


### 相关文章

- [令牌桶算法][blog1] 页面无法访问的[替代地址][blog1_back]
- [限流算法-石衫的架构笔记][blog2]


[blog1]: https://www.jianshu.com/p/a3d068f2586d ""
[blog1_back]: https://web.archive.org/web/20200923012957/https://www.jianshu.com/p/a3d068f2586d ""
[blog2]: https://mp.weixin.qq.com/s/icXd55HR2GiVr95d44V34w ""