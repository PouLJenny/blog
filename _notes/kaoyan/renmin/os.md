# 高级操作系统

## 非题库考试

### 名词解释
- I/O重定向 
  ```允许用户将磁盘文件和标准输入输出联系起来```
- Inode
  ```文件的元数据，每个文件对应一个inode。```
- 线程
  ```运行在进程上下文中的逻辑流```
- 进程
  ```一个执行中程序的实例```
- 死锁
  `指的是一组线程被阻塞了，等一个永远也不会为真的条件。 Semaphores introduce the potential for a nasty kind of run-time error, called deadlock, where a collection of threads is blocked, waiting for a condition that will never be true.`
- 无锁化
  ```无锁化编程特指在多线程编程的时候，对线程间共享数据的并发修改不使用锁， 而采用基于硬件提供的原子操作能力来修改共享数据，进而提升性能，减少使用锁带来的互斥开销。```
- 文件系统
  ```文件系统是用于明确存储设备或分区上的文件的方法和数据结构；即在存储设备上组织文件的方法。操作系统中负责管理和存储文件信息的软件机构称为文件管理系统，简称文件系统。由三部分组成：文件系统的接口，对对象操纵和管理的软件集合，对象及属性。```
- 内部碎片
  ```内部碎片是处于区域内部或页面内部的存储块。占有这些区域或页面的进程并不能使用这个存储块。而在进程占有这块存储块时，系统无法利用它。直到进程释放它，或进程结束时，系统才有可能利用这个存储块。```
- 外部碎片
  ```外部碎片是出于任何已分配区域或页面外部的空闲存储块。这些存储块的总和可以满足当前申请的长度要求，但是由于它们的地址不连续或其他原因，使得系统无法满足当前申请。```
- 碎片
  ```堆里的虽然有未使用的内存但不能用来满足分配请求，这些不能分配的块叫做碎片```
- 虚拟内存
  ```virtual memory，虚拟内存是硬件异常、硬件地址翻译、主存、磁盘文件和内核软件的完美交互，它为每个进程提供了一个大的、一致的和私有的地址空间```
- 互斥
  ```每个线程在执行它的临界区中的指令时，拥有对共享变量的互斥的访问。```
- 竞争
  ```竞争是当一个程序的正确性依赖于一个线程要在另一个线程达到y点之前到达它的控制流中的x点时发生的。通常发生竞争是因为程序员假定线程将按照某种特殊的轨迹线穿过执行状态空间，而忘记了另一种准则规定：多线程的程序必须对任何可行的轨迹线都正确工作。```
- 并发
  ```一个逻辑控制流在时间上与另一个逻辑控制流重叠称为并发 concurency```
- 并行
  ```两个逻辑控制流并发地运行在不同的处理器或者计算机上称这两个流为并行 ```
- 异常
  ```exception，异常就是控制流中的突变，用来响应处理器状态中的某些变化。```
- 信号量
  ```信号量s是具有非负整数值的全局变量，只能由两种特殊的操作来处理，这两种操作称为P和V。是解决同步不同执行线程问题的方法。```
- 线程安全方法
  `
  A function is thread-safe iff it will always produce correct results when called repeatedly from multiple concurrent threads. 

  `
- reentrant
 `A function is reentrant iff it accesses NO shared variables when called from multiple threads.`
### 问答题

1. 典型的磁盘调度算法有哪些，请至少说出三种以上，并简单介绍其优缺点？
    ```
    1. First Come First Serve
    谁先来处理谁

    优点： 公平
    缺点： 两次请求间磁道间隔比较远的话对性能影响比较大

    2. SSTF: Shortest Seek Time First
    SSTF orders the queue of
    I/O requests by track, picking requests on the nearest track to complete
    first.
    优点： 降低了一定的seek时间
    缺点： 
        1. 饥饿问题，极限情况下track比较远的请求会一直无法处理
        2. 陷入局部最优，达不到全局最优

    3. F-SCAN/Freeze SCAN (Elevator)
    从内->外，再从外->内,再从内->外。。。这么循环扫描，过程中
    freezes the queue to be serviced
    优点： 避免饥饿问题
    缺点： 
        1. 效率问题，刚被扫过的磁道附近来请求的话，需要等到下次再扫过来的时候才能处理，不能立即响应
        2. 磁道处理不平衡，中间的访问机会更多
        3. 没有考虑旋转的问题，也就是rotation time

    4. C-SCAN/Circular SCAN (Elevator)
    Instead of sweeping in both directions across the disk, the algorithm only
    sweeps from outer-to-inner, and then resets at the outer track to begin
    again。 只是从外到内扫描，完了再重制到外道

    优点： 解决了磁道处理不平衡问题
    缺点： 
        1. 跟F-SCAN一样，也是有效率问题。
        2. 没有考虑旋转的问题，也就是rotation time

    5. SPTF: Shortest Positioning Time First
    What it depends on here is the relative time of seeking as compared to rotation.

    优点： 因为磁盘的seek time和rotation time效率差不多，所以对性能提升比较明显
    缺点： 需要操作系统和磁盘协同处理，实现起来比较困难
    ```
    
1. 操作系统一般可以分为哪三个主要模块？（Three Easy Pieces）
    ```
    虚拟化  Virtualization
      - 进程
      - 虚拟内存
    并发 	Concurrency 
    持久化 	Persistence
    ```

1.  操作系统对上提供的抽象（Abstract）有什么优点？请给出 3 个或更多经典抽象的例子。
    ```
    优点： 
    1. 保护硬件免受应用程序的错误使用
    2. 给应用程序提供简单、统一的操作硬件设备的机制
    
    例子：
    计算资源的抽象 进程
    IO设备的抽象  文件
    物理内存的抽象 虚拟内存
    ```

1. 线程相对于进程的优点
    ```
    1. 进程之间可以并发、共享
    2. 但是开销会比较大
    进程切换需要保持和恢复的内容更多，意味着更多内存访问
    每个进程有自己独立的虚拟内存空间，无法按照虚拟地址共享内存；需要用IPC（进程间通信）机制，但开销更高
    ```

1. 线程不安全的函数有哪些类型，以及相应的解决办法
    ```
    1. 不能保护共享变量
    使用信号量的P和V函数
    2. 多次函数调用之间依赖同样的持久状态
    把原来来的全局/静态变量变为参数不断传递来记录状态
    3. 返回一个指向静态变量的指针
    3.1 重写函数，调用者传递存放结果的地址
    3.2 “Lock-and-copy”
    4. 调用其他线程不安全的函数
    只调用线程安全函数
    ```

### 线程安全
请判断下面每个函数的类型是线程安全函数、线程不安全函数，还是是可重入函数。
```c
int t;
void f(int *x, int *y) {
    t = *x + *y;
}
void g(int*x, int *y) {
    static int m = *x;
    *y = *x;
    *x = m;
}
void h(int *x, int *y) {
    P(&mutex);
    t = *x;
    *x = *y;
    *y = t;
    V(&mutex);
}
void k(int *x, int *y) {
    P(&mutex);
    t = *x;
    V(&mutex);
    *x = *y;
    P(&mutex);
    *y = t;
    V(&mutex);
}
void m(int *x, int *y) {
    int t = *x;
    *x = *y;
    *y = t;
}
void n(int *x, int *y) {
    *x = *x ^ *y;
    *y = *x ^ *y;
    *x = *x ^ *y;
}
```

```
f: 线程不安全函数
g: 线程不安全函数
h: 线程安全函数
k: 线程安全函数
m: 可重入函数
n: 可重入函数
```

m和n函数的区别
这两个函数的区别是：第一个函数 n 是通过异或操作实现交换，而第二个函数 m 是通过临时变量实现交换。

函数 n 是线程安全的，因为异或操作本身是具有原子性的，不会出现多个线程同时修改同一内存区域的情况，因此不需要使用同步机制。

而函数 m 则是线程不安全的，因为它使用了临时变量 t 来交换 x 和 y 的值，因此会存在多线程竞争的情况，导致出现意外结果。例如，当一个线程在执行 *x = *y 的时候，另外一个线程可能同时修改了 *y 的值，导致结果不一致。

因此，在多线程环境下，为了保证函数的正确性，需要使用同步机制来确保同时只有一个线程能够执行该函数，并保证内存的一致性和正确性

### Deadlock
如下表所示，有两个线程 Thread 1 和 Thread 2 同时工作，a, b, c 为信号量，初始值均为 1。请问
Thread 1 和 Thread 2 是否会发生死锁？请画出进程图，并作出解释。

|Thread| Thread 1 |Thread 2|
|--|--|--|
|step1| P(a)| P(b)|
|step2| P(b)| P(c)|
|step3| V(a)| V(c)|
|step4| P(c)| P(a)|
|step5| V(b)| V(b)|
|step6| V(c)| V(a)|

### I/O 调度
计算机每个扇区为 512B。以下 I/O 请求几乎同时、但按照顺序到达 I/O 调度层，其中的数字为扇区

编号。当前磁头正处于 100 号扇区处，并向扇区编号较大的方向移动。
I/O 请求序列为{120，90，45，170，50，75，125，30，20}
假设计算机只有一块磁盘，没有进行 RAID 配置，所使用的磁盘调度策略分别为 First Come First

Serve (FCFS)、Shortest Seek Time First (SSTF)、F-SCAN(磁头任意移动方向都可以服务 I/O 请求)、CSCAN 调度策略(只有磁头从小编号扇区向大编号扇区移动的过程中可以服务 I/O 请求)。

请分别给出四种策略的实际I/O请求服务序列，以及完成这些I/O请求的总寻道时间（假设每移动一
个扇区，寻道时间加 1）。对于 SSTF，如果遇到寻道时间相同的请求，尽可能不改变磁头移动方向。