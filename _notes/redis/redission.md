# Redisson

## Locks


###  问题

1. 假设客户端刚刚在master写入一个锁，此时发生了master的宕机，但是master还没来得及将那个锁key异步同步到slave，
slave就切换成了新的master。此时别的客户端在新的master上也尝试获取同一个。
2. 


## 公平锁和非公平锁


## 看门狗是怎么实现的?

