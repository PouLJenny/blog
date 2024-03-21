# Linux 
[官网](https://www.kernel.org/ )
[官方文档](https://www.kernel.org/doc/html/latest/ )

## I/O

### Linux IO调度算法

https://www.cnblogs.com/cobbliu/p/5389556.html

#### Noop算法

Noop调度算法也叫作电梯调度算法，它将IO请求放入到一个FIFO队列中，然后逐个执行这些IO请求

#### Deadline算法

Deadline算法的核心在于保证每个IO请求在一定的时间内一定要被服务到，以此来避免某个请求饥饿

#### Anticipatory算法

Anticipatory算法的核心是局部性原理，它期望一个进程昨晚一次IO请求后还会继续在此处做IO请求。在IO操作中，有一种现象叫“假空闲”（Deceptive idleness），它的意思是一个进程在刚刚做完一波读操作后，看似是空闲了，不读了，但是实际上它是在处理这些数据，处理完这些数据之后，它还会接着读，这个时候如果IO调度器去处理另外一个进程的请求，那么当原来的假空闲进程的下一个请求来的时候，磁头又得seek到刚才的位置，这样大大增加了寻道时间和磁头旋转时间。所以，Anticipatory算法会在一个读请求做完后，再等待一定时间t（通常是6ms），如果6ms内，这个进程上还有读请求过来，那么我继续服务，否则，处理下一个进程的读写请求。

在一些场景下，Antocipatory算法会有非常有效的性能提升。这篇文章有说，这篇文章也有一份评测。
值得一提的是，Anticipatory算法从Linux 2.6.33版本后，就被移除了，因为CFQ通过配置也能达到Anticipatory算法的效果。

#### CFQ算法
CFQ（Completely Fair Queuing）算法，顾名思义，绝对公平算法。


### 操作磁盘

#### 查询磁盘具体信息
`sudo fdisk -l`

#### 查询磁盘的挂载点和使用率
`df -h`

#### 开机自动挂载磁盘
`blkid` 查看磁盘的
`lsblk -f`
`echo '/dev/vdb1 挂载的目录 ext4 defaults 0 0' >> /etc/fstab`

[fstab文件详解](https://blog.csdn.net/richerg85/article/details/17917129 )

#### 磁盘格式化

`mkfs`系列命令
比如：
- `mkfs.ext4`
- `mkfs.ntfs`

## 常用命令

### 查询发行版本
`uname -a && cat /etc/*release`

### 输出到指定文件
`nohup ./start.sh > output.out 2>&1 &`

### 查看物理CPU个数
`cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l`

### 查看每个物理CPU中core的个数(即核数)
`cat /proc/cpuinfo| grep "cpu cores"| uniq`

### 查看逻辑CPU的个数
`cat /proc/cpuinfo| grep "processor"| wc -l`

### 查看CPU信息（型号）
`cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c`

### 查询CPU信息
`lscpu` 

### [top](https://linux.cn/article-9937-1.html )
[man手册](https://man7.org/linux/man-pages/man1/top.1.html )
`PID`：进程 ID，一个用来定位进程的唯一标识符
`USER`：运行进程的用户
`PR`：任务的优先级
`NI`：Nice 值，优先级的一个更好的表现形式
`VIRT`：虚拟内存的大小，单位是 KiB（kibibytes）
`RES`：常驻内存大小，单位是 KiB（物理内存和虚拟内存的一部分）
`SHR`：共享内存大小，单位是 KiB（共享内存和虚拟内存的一部分）
`S`：进程状态，一般 I 代表空闲，R 代表运行，S 代表休眠，Z 代表僵尸进程，T 或 t 代表停止（还有其它更少见的选项）
`%CPU`：自从上次屏幕更新后的 CPU 使用率
`%MEM`：自从上次屏幕更新后的 RES 常驻内存使用率
`TIME+`：自从程序启动后总的 CPU 使用时间
`COMMAND`：启动命令，如之前描述那样

### 休眠/关机
命令	操作
systemctl reboot	重启机器
systemctl poweroff	关机
systemctl suspend	挂起-睡眠-保存在內存
systemctl hibernate	休眠-断电-保存在硬盘
systemctl hybrid-sleep	混合休眠模式（同时休眠到硬盘并挂起

`cat /sys/power/state` 查询系统支持的休眠级别

常⽤的休眠⽅式有freeze,standby, mem, disk
freeze: 冻结I/O设备,将它们置于低功耗状态,使处理器进⼊空闲状态,唤醒最快,耗电⽐其它standby, mem, disk⽅式⾼
standby: 除了冻结I/O设备外,还会暂停系统,唤醒较快,耗电⽐其它 mem, disk⽅式⾼
mem:     将运⾏状态数据存到内存,并关闭外设,进⼊等待模式,唤醒较慢,耗电⽐disk⽅式⾼
disk:    将运⾏状态数据存到硬盘,然后关机,唤醒最慢

## 修改Linux环境语言

### archlinux 

#### 最简洁的方式

本地化配置，其实就是设置locale。

1. 编辑/etc/locale.gen 文件，去掉zh_CN.UTF-8前面的#号

2. 你可以设置整个系统的locale,编辑/etc/locale.conf,写下如下内容
    LANG="zh_CN.UTF-8",但是不建议这样做，这样做在某些地方会产生乱码

3. 建议设置局部的locale,编辑~/.bashrc，添加：
    export LANGUAGE="zh_CN:UTF-8"

## 问题处理

### Linux下jdk中文方框乱码
#### 背景
我的电脑是Manjaro的，日常娱乐办公没啥问题，但是今天打开自己的idea，结果发现项目里面的中文都变成方框框了，也不像是编码的问题，像是无法显示。
我好像什么都没干啊！而且除了idea其它的软件都没有问题。
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019072012115221.png)

#### 解决
随后网上搜索确实是字体显示的问题。

## 常用工具

### 查看系统网卡的使用情况

https://www.baeldung.com/linux/monitor-network-usage#bd-iftop

查询本机网卡的实时网速
```shell
nload eth0
```

## EOF