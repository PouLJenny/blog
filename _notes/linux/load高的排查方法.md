# Linux load过高的解决方式

## Load的定义
https://en.wikipedia.org/wiki/Load_(computing)


## 僵尸进程

在类UNIX系统中，僵尸进程是指完成执行（通过exit系统调用，或运行时发生致命错误或收到终止信号所致），但在操作系统的进程表中仍然存在其进程控制块，处于"终止状态"的进程。这发生于子进程需要保留表项以允许其父进程读取子进程的退出状态：一旦退出态通过wait系统调用读取，僵尸进程条目就从进程表中删除，称之为"回收"（reaped）。正常情况下，进程直接被其父进程wait并由系统回收。进程长时间保持僵尸状态一般是错误的并导致资源泄漏。

## 排查方式

1. 先定位出 CPU 使用率较高的进程，找到对应的进程 id
```shell
$top
# 进入交互界面后，按 P 使进程按照 CPU 使用率排序
```

2. 找到对应进程的使用 CPU 较高的线程
```shell
$top -Hp <pid>
# <pid> 就是第一步查出来的进程 id
```


3. 将第二步得到的进程 id 转换为十六进制
```shell
$printf "0x%x\n" <pid>
# <pid> 是第二步查出的进程 id
```


4. 将第三步得到的十六进制和 jstack 比较找到堆栈
```shell
$jstack <pid> > jstack.tmp
# 打印 JVM 进程堆栈到 jstack.tmp 文件
# 后续只需要在文件中搜索第三步的十六进制字符串，即可找到其对应的堆栈
```


## 工具

## top

## iostat
iostat -x 1 10

## vmstat
vmstat 

## dstat


## 博客
https://nickchenyx.github.io/2020/11/01/linux-load-high/
https://blog.csdn.net/gu_study/article/details/81942939


https://www.brendangregg.com/blog/2017-08-08/linux-load-averages.html