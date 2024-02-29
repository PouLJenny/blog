# Linux load过高的解决方式

## Load的定义
https://en.wikipedia.org/wiki/Load_(computing)


## 僵尸进程

在类UNIX系统中，僵尸进程是指完成执行（通过exit系统调用，或运行时发生致命错误或收到终止信号所致），但在操作系统的进程表中仍然存在其进程控制块，处于"终止状态"的进程。这发生于子进程需要保留表项以允许其父进程读取子进程的退出状态：一旦退出态通过wait系统调用读取，僵尸进程条目就从进程表中删除，称之为"回收"（reaped）。正常情况下，进程直接被其父进程wait并由系统回收。进程长时间保持僵尸状态一般是错误的并导致资源泄漏。

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