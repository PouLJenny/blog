# Operating Systems

https://en.wikipedia.org/wiki/Operating_system

![](./pic/Unix_history-simple.svg)

## Process 

### Process States 

- Running: In the running state, a process is running on a processor.
This means it is executing instructions.
- Ready: In the ready state, a process is ready to run but for some
reason the OS has chosen not to run it at this given moment.
- Blocked: In the blocked state, a process has performed some kind
of operation that makes it not ready to run until some other event
takes place. A common example: when a process initiates an I/O
request to a disk, it becomes blocked and thus some other process
can use the processor

## Scheduling

### MLFQ(Multi-Level Feedback Queue)
- Rule 1: If Priority(A) > Priority(B), A runs (B doesn’t).
- Rule 2: If Priority(A) = Priority(B), A & B run in RR.
- Rule 3: When a job enters the system, it is placed at the highest
priority (the topmost queue).
- Rule 4: Once a job uses up its time allotment at a given level (re-
gardless of how many times it has given up the CPU), its priority is
reduced (i.e., it moves down one queue).
- Rule 5: After some time period S, move all the jobs in the system
to the topmost queue.


## 异常控制流


### 名词

**抢占（preempted）**: 暂时挂起

**物理控制流**
**逻辑控制流**
**并发流**
**并发**
**时间片**
**时间分片**
**并行流**
**并行**

**模式位（mode bit）**

### /proc文件系统

/proc文件目录下，将许多内核数据结构的内容输出为一个用户程序可以读的文本文件的层次结构，比如
/proc/cpuinfo, cpu的信息
/proc/\<process-id>/maps, 进程的内存段

/sys文件系统，输出系统总线和设备的额外的低层信息

## 虚拟内存

###  查看操作系统内存页大小

`getconf PAGESIZE`


## 系统级I/O

### /dev/null

/dev/null 是一个特殊的设备文件，在许多类 Unix 操作系统中都存在。它被称为“黑洞”设备，可以用于丢弃数据。当将数据写入 /dev/null 或从中读取数据时，数据会被永久丢弃，不会保存到任何地方。

在类 Unix 操作系统中，一切都是文件，包括硬件设备。/dev/null 就是一个虚拟的文件，用于丢弃数据。例如，如果您希望运行一个命令但不关心其输出，您可以将输出重定向到 /dev/null。同样地，如果您希望将某个文件内容清空，您可以将文件内容重定向到 /dev/null。

例如，以下命令将 stdout（标准输出）和 stderr（标准错误输出）都重定向到 /dev/null，从而抑制了命令的输出和错误信息：

```shell
## 2>&1 表示将 stderr 重定向到 stdout，因此错误信息也会被送到 /dev/null。
command > /dev/null 2>&1
```

## Tools
[操作系统性能测试工具LMbench](http://lmbench.sourceforge.net/ )