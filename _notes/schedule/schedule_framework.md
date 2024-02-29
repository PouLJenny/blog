任务平台技术调研 

平台目标： 解析cron表达式准时触发需要执行的任务
解析一个cron表达式

一站式分布式调度任务解决方案
它山之石可以攻玉



# 技术调研

## 单机表达式解析

### Spring 的任务解析流程

org.springframework.scheduling.annotation.ScheduledAnnotationBeanPostProcessor#processScheduled
org.springframework.scheduling.support.CronSequenceGenerator 解析cron表达式获取下次执行任务的时间 跟当前时间相差的毫秒值
交给 java.util.concurrent.ScheduledExecutorService 延迟执行任务

### quartz 的任务解析流程


### xxljob 的任务解析流程


### ElasticJob 的任务解析流程


### Antares 的任务解析流程


### SIA-TASK 的任务解析流程