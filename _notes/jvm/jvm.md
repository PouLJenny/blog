# java虚拟机

## 内存管理

### Run-Time Data Areas

![](./pic/run-time-data.svg)

#### PC Register
程序计数器是一块较小的内存空间，它可以看作是当前线程所执行的字节码的行号指示器。
每个线程都有一个自己的程序计数器，且是《Java虚拟机规范》中没有规定任何OutOfMemoryError情况的区域。

#### Java Virtual Machine Stacks

也是线程私有的，生命周期与线程相同。
每个方法被执行的时候，都会创建一个栈帧，用于存储局部变量表，操作数栈、动态连接、方法出口等信息。每一个方法调用从开始到结束，都对应着一次入栈和出栈的过程。

在《Java虚拟机规范》中对这个内存区域规定了两种异常。如果线程请求的栈深度大于虚拟机所允许的深度，将抛出**StackOverFlowError**异常，如果Java虚拟机栈容量可以动态扩展，当栈扩展时，无法申请到足够的内存会抛出**OutOfMemoryError**异常。

HotSpot虚拟机的栈容量是不可以动态扩展的，所以不会出现栈扩展的OOM，但是当线程无法申请栈空间的时候会出现OOM

#### Native Method Stacks

本地方法栈跟虚拟机栈所发挥的作用是一样的，不同的是后者为虚拟机执行java方法服务，前者是为本地方法服务。

Java虚拟机规范》对本地方法栈中方法使用的语言、使用方式与数据结构并没有任何强制规 定，因此具体的虚拟机可以根据需要自由实现它，甚至有的Java虚拟机(譬如Hot-Spot虚拟机)直接 就把本地方法栈和虚拟机栈合二为一。与虚拟机栈一样，本地方法栈也会在栈深度溢出或者栈扩展失败时分别抛出**StackOverflowError**和**OutOfMemoryError**异常。

#### Heap
对于Java应用程序来说，Java堆(Java Heap)是虚拟机所管理的内存中最大的一块。Java堆是被所有线程共享的一块内存区域，在虚拟机启动时创建。此内存区域的唯一目的就是存放对象实例，Java世界里“几乎”所有的对象实例都在这里分配内存。

又叫GC堆

如果在Java堆中没有内存完成实例分配，并且堆也无法再 扩展时，Java虚拟机将会抛出**OutOfMemoryError**异常。

#### Method Area
方法区(Method Area)与Java堆一样，是各个线程共享的内存区域，它用于存储已被虚拟机加载的类型信息、常量、静态变量、即时编译器编译后的代码缓存等数据。虽然《Java虚拟机规范》中把方法区描述为堆的一个逻辑部分，但是它却有一个别名叫作“非堆”(Non-Heap)，目的是与Java堆区分开来。

根据《Java虚拟机规范》的规定，如果方法区无法满足新的内存分配需求时，将抛出 **OutOfMemoryError**异常。

#### Run-Time Constant Pool

运行时常量池(Runtime Constant Pool)是方法区的一部分。Class文件中除了有类的版本、字段、方法、接口等描述信息外，还有一项信息是常量池表(Constant Pool Table)，用于存放编译期生 成的各种字面量与符号引用，这部分内容将在类加载后存放到方法区的运行时常量池中。

运行时常量池相对于Class文件常量池的另外一个重要特征是具备动态性，Java语言并不要求常量 一定只有编译期才能产生，也就是说，并非预置入Class文件中常量池的内容才能进入方法区运行时常 量池，运行期间也可以将新的常量放入池中，这种特性被开发人员利用得比较多的便是String类的intern()方法。

既然运行时常量池是方法区的一部分，自然受到方法区内存的限制，当常量池无法再申请到内存 时会抛出**OutOfMemoryError**异常。

#### Direct Memory
直接内存(Direct Memory)并不是虚拟机运行时数据区的一部分，也不是《Java虚拟机规范》中 定义的内存区域。但是这部分内存也被频繁地使用，而且也可能导致**OutOfMemoryError**异常出现.

在JDK 1.4中新加入了NIO(New Input/Output)类，引入了一种基于通道(Channel)与缓冲区 (Buffer)的I/O方式，它可以使用Native函数库直接分配堆外内存，然后通过一个存储在Java堆里面的 DirectByteBuffer对象作为这块内存的引用进行操作。这样能在一些场景中显著提高性能，因为避免了在Java堆和Native堆中来回复制数据。


### 数据类型
Java中分成两大数据类型
1. **primitive** types 操作 primitive values
	- **numberic** types
		- **integral** types
			- **byte** 8-bit 默认值是0 from -128 to 127 (-2$^7$ to 2$^7$ - 1), inclusive
			- **short** 16-bit 默认值是0 ,from -32768 to 32767 (-2$^{15}$ to 2$^{15}$ - 1), inclusive
			- **int** 32-bit 默认值是0, rom -2147483648 to 2147483647 (-2$^{31}$ to 2$^{31}$ - 1), inclusive
			- **long** 64-bit 默认值是0 from -9223372036854775808 to 9223372036854775807 (-2$^{63}$ to -2$^{63}$ - 1), inclusive
			- **char** 16-bit无符号整型数字来表示Unicode 默认值是null code point ('\u0000'),from 0 to 65535 inclusive
		- **floating-point** types
			- **float** 32-bit 单精度浮点型
			- **double** 64-bit 双精度浮点型
	- **boolean** type true and false
	- **returnAddress** type pointers to the opcodes of Java Virtual Machine instructions
2. **reference** types 操作 reference values
	- **class** types 
	- **array** types 
	- **interface** types 

![](./pic/data-access-hotspot.png)


### OOM

实际模拟一下OOM的场景

#### Java堆溢出
```java
import java.util.ArrayList;

/**
 * jvm arg -verbose:gc -Xms20M -Xmx20M -Xmn10M -XX:+PrintGCDetails -XX:SurvivorRatio=8 -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/home/poul/data/test.hprof
 * 在java虚拟机规范的描述中，除了程序计数器外，
 * 虚拟机内存的其它几个区域都有发生OutOfMemoryError异常的可能
 * @author 杨霄鹏
 * @since 2017年11月13日 下午9:14:40
 */
public class TestOOM {


	static class OOMObject {

		private int id;

		private String name;

		private String other;

		@Override
		public String toString() {
			return "OOMObject{" +
					"id=" + id +
					", name='" + name + '\'' +
					", other='" + other + '\'' +
					'}';
		}

		public int getId() {
			return id;
		}

		public void setId(int id) {
			this.id = id;
		}

		public String getName() {
			return name;
		}

		public void setName(String name) {
			this.name = name;
		}

		public String getOther() {
			return other;
		}

		public void setOther(String other) {
			this.other = other;
		}
	}
	/**
	 * 测试java堆溢出
	 * @param args
	 */
	public static void main(String[] args) throws Exception{
		Thread thread = new Thread(() -> {
			ArrayList<OOMObject> list = new ArrayList<OOMObject> ();
			int i = 0;
			while (true) {
				OOMObject oomObject = new OOMObject();
				oomObject.setId(++i);
				oomObject.setName("测试");
				list.add(oomObject);
			}
		});

		Thread thread2 = new Thread(() -> {
			while (true) {
				try {
					Thread.sleep(500);
				} catch (Exception e) {
					e.printStackTrace();
				}
				System.out.println("I'm alive from thread2");
			}
		});

		thread.start();thread.join();
		thread2.start();thread2.join();
	}
}
```
```
Exception in thread "Thread-0" java.lang.OutOfMemoryError: Java heap space
	at java.base/java.util.Arrays.copyOf(Arrays.java:3512)
	at java.base/java.util.Arrays.copyOf(Arrays.java:3481)
	at java.base/java.util.ArrayList.grow(ArrayList.java:237)
	at java.base/java.util.ArrayList.grow(ArrayList.java:244)
	at java.base/java.util.ArrayList.add(ArrayList.java:454)
	at java.base/java.util.ArrayList.add(ArrayList.java:467)
	at TestOOM.lambda$main$0(TestOOM.java:66)
	at TestOOM$$Lambda$1/0x0000000800c00a08.run(Unknown Source)
	at java.base/java.lang.Thread.run(Thread.java:833)
```
其中很容易能看出来是哪里出问题了


**JVM会把发生OOM的线程给杀死，并释放相关的内存，如果线程不是main线程的话jvm进程会继续存在，且不影响其他线程。但是OOM之前肯定是要FULL GC的所以对与高并发的场景还是比较严重的**

#### 虚拟机栈和本地方法栈溢出
一般就是递归调用太多了导致的

```java
/**
* VM Args:-Xss136k
*/
public class JavaVMStackSOF {
   private int stackLength = 1; 
   public void stackLeak() {
    stackLength++;
    stackLeak(); 
}
public static void main(String[] args) throws Throwable {

Thread thread = new Thread(() -> {
	  JavaVMStackSOF oom = new JavaVMStackSOF();
    try {
        oom.stackLeak();
    } catch (Throwable e) {
        System.out.println("stack length:" + oom.stackLength);
        throw e; 
      }
  });

  Thread thread2 = new Thread(() -> {
    while (true) {
      try {
        Thread.sleep(500);
      } catch (Exception e) {
        e.printStackTrace();
      }
      System.out.println("I'm alive from thread2");
    }
  });

  thread.start();thread.join();
  thread2.start();thread2.join();
  }
}
```

```
stack length:368
Exception in thread "main" java.lang.StackOverflowError
	at JavaVMStackSOF.stackLeak(JavaVMStackSOF.java:5)
	at JavaVMStackSOF.stackLeak(JavaVMStackSOF.java:6)
  ...
```

**JVM会把发生StackOverflowError的线程给杀死，并释放相关的内存，如果线程不是main线程的话jvm进程会继续存在，且不影响其他线程。**


#### 方法区和运行时常量池溢出

这个没搞出来 TODO

猜测大概是元空间没有**触碰到进程可用内存的上限**就没事

#### 本机直接内存溢出
```java
import sun.misc.Unsafe;

import java.lang.reflect.Field;

/**
 * VM Args:-Xmx20M -XX:MaxDirectMemorySize=10M
 *
 * @author 杨霄鹏
 * @since 2023/5/9 06:47
 */
public class DirectMemoryOOM {

    private static final int _1MB = 1024 * 1024;

    public static void main(String[] args) throws Exception {
        Thread thread = new Thread(() -> {
            System.out.println("start test");
            try {
                Field unsafeField = Unsafe.class.getDeclaredFields()[0];
                unsafeField.setAccessible(true);
                Unsafe unsafe = (Unsafe) unsafeField.get(null);
                while (true) {
                    unsafe.allocateMemory(_1MB);
                }
            } catch (IllegalAccessException e) {
                e.printStackTrace();
            }
        });

        Thread thread2 = new Thread(() -> {
            while (true) {
                try {
                    Thread.sleep(2000L);
                } catch (Exception e) {
                    e.printStackTrace();
                }
                System.out.println("I'm alive from thread2 " + System.currentTimeMillis());
            }
        });

        thread2.start();
        thread.start();
        thread.join();
        thread2.join();
    }

}
```

这种代码很危险的，如果进程使用的内存过多的话，会直接被OS杀死

只能从linux的日志中找原因
`journalctl -ex`
会发现有一条比较醒目的日志。

kernel: Out of memory: Killed process 144109 (java) total-vm:888245248kB, anon-rss:3465312kB, file-rss:0kB, shmem-rss:32kB, UID:1000 pgtables:1732980kB oom_score_adj:0

### 对象是否存活？

#### 可达性分析算法（Reachability Analysis）

![](./pic/gc-roots.png)
在Java技术体系里面，固定可作为GC Roots的对象包括以下几种:
- 在虚拟机栈(栈帧中的本地变量表)中引用的对象，譬如各个线程被调用的方法堆栈中使用到的参数、局部变量、临时变量等。
- 在方法区中类静态属性引用的对象，譬如Java类的引用类型静态变量。
- 在方法区中常量引用的对象，譬如字符串常量池(String Table)里的引用。
- 在本地方法栈中JNI(即通常所说的Native方法)引用的对象。
- Java虚拟机内部的引用，如基本数据类型对应的Class对象，一些常驻的异常对象(比如
NullPointExcepiton、OutOfMemoryError)等，还有系统类加载器.
- 所有被同步锁(synchronized关键字)持有的对象。
- 反映Java虚拟机内部情况的JM XBean、JVM TI中注册的回调、本地代码缓存等。
- 根据用户所选用的垃圾收集器以及当前回收的内存区域不 同，还可以有其他对象“临时性”地加入


### GC算法

#### 分代收集理论
1. 弱分代假说(Weak Generational Hypothesis):绝大多数对象都是朝生夕灭的。
2. 强分代假说(Strong Generational Hypothesis):熬过越多次垃圾收集过程的对象就越难以消亡


#### 标记-清除算法
最早出现也是最基础的垃圾收集算法是“标记-清除”(M ark-Sweep)算法，在1960年由Lisp之父 John McCarthy所提出。
如它的名字一样，算法分为“标记”和“清除”两个阶段:首先标记出所有需要回 收的对象，在标记完成后，统一回收掉所有被标记的对象，也可以反过来，标记存活的对象，统一回 收所有未被标记的对象。

它的主要缺点有两个:
- 第一个是执行效率不稳定，如果Java堆中包含大量对 象，而且其中大部分是需要被回收的，这时必须进行大量标记和清除的动作，导致标记和清除两个过 程的执行效率都随对象数量增长而降低;
- 第二个是内存空间的碎片化问题，标记、清除之后会产生大 量不连续的内存碎片，空间碎片太多可能会导致当以后在程序运行过程中需要分配较大对象时无法找 到足够的连续内存而不得不提前触发另一次垃圾收集动作

#### 标记-复制算法/复制算法
标记-复制算法常被简称为复制算法。为了解决标记-清除算法面对大量可回收对象时执行效率低 的问题，1969年Fenichel提出了一种称为“半区复制”(Semispace Copying)的垃圾收集算法，它将可用 内存按容量划分为大小相等的两块，每次只使用其中的一块。当这一块的内存用完了，就将还存活着 的对象复制到另外一块上面，然后再把已使用过的内存空间一次清理掉。

优点：
- 这样实现简单，运行高效，
缺点：
- 这种复制回收算法的代价是将可用内存缩小为了原来的一半，空间浪费未免太多了一 点。

在1989年，Andrew Appel针对具备“朝生夕灭”特点的对象，提出了一种更优化的半区复制分代策 略，现在称为“Appel式回收”。HotSpot虚拟机的Serial、ParNew等新生代收集器均采用了这种策略来设计新生代的内存布局。Appel式回收的具体做法是把新生代分为一块较大的Eden空间和两块较小的 Survivor空间，每次分配内存只使用Eden和其中一块Survivor。发生垃圾搜集时，将Eden和Survivor中仍 然存活的对象一次性复制到另外一块Survivor空间上，然后直接清理掉Eden和已用过的那块Survivor空间。HotSpot虚拟机默认Eden和Survivor的大小比例是8∶1

#### 标记整理算法
标记-复制算法在对象存活率较高时就要进行较多的复制操作，效率将会降低。更关键的是，如果 不想浪费50%的空间，就需要有额外的空间进行分配担保，以应对被使用的内存中所有对象都100%存 活的极端情况，所以在老年代一般不能直接选用这种算法。

针对老年代对象的存亡特征，1974年Edward Lueders提出了另外一种有针对性的“标记-整 理”(Mark-Compact)算法，其中的标记过程仍然与“标记-清除”算法一样，但后续步骤不是直接对可回收对象进行清理，而是让所有存活的对象都向内存空间一端移动，然后直接清理掉边界以外的内存

如果移动存活对象，尤其是在老年代这种每次回收都有大量对象存活区域，移动存活对象并更新
所有引用这些对象的地方将会是一种极为负重的操作，而且这种对象移动操作必须全程暂停用户应用 程序才能进行，这就更加让使用者不得不小心翼翼地权衡其弊端了，像这样的停顿被最初的虚拟机 设计者形象地描述为“Stop The World”

#### GC Roots

  通过可达性分析算法，对象是否有GC Roots的引用

#### 对象从新生代进入老年代的方式

-  躲过15次GC之后进入老年代 可以通过JVM参数`-XX:MaxTenuringThreshold`来设置，默认是15岁
-  动态对象年龄判断
   假如说当前放对象的Survivor区域里，一批对象的总大小大于了这块Survivor区域的内存大小的50%，那么此时大于等于这批对象年龄的对象，就可以直接进入老年代了。
-  大对象直接进入老年代
   `-XX:PretenureSizeThreshold`，可以把他的值设置为字节数，比如“1048576”字节，就是1MB。
-  Minor GC后的对象太多无法放入Survivor区 这些存活的对象会直接转入到老年代


#### JVM优化的最终目的

 其实大家如果透彻理解了最近的几篇文章涵盖的JVM的运行原理，就会知道，所谓JVM优化，就是尽可能让对象都在新生代里分配和回收，尽量别让太多对象频繁进入老年代，避免频繁对老年代进行垃圾回收，同时给系统充足的内存大小，避免新生代频繁的进行垃圾回收。


### 垃圾收集器

#### Serial

#### Serial Old

#### ParNew 

`-XX:+UseParNewGC` jvm参数指定使用ParNew收集器

当Eden区域内存填满时，会触发minor gc，使用标记 复制算法，先把Eden和正在使用的suvivor中存活的对象标记出来，并复制到另个一个空闲的suvivor中去，
接下来清空Eden和之前使用的那个suvivor的内存
此过程会stop the world，由于此算法效率很高，执行速度很快，应用感知不是很强烈

[GC日志执行时间分析](https://blog.csdn.net/yiyihuazi/article/details/112321614 '')

#### CMS

Concurrent Mark Sweep

`-XX:+CMSParallelInitialMarkEnabled` 这个参数会在CMS垃圾回收器的“初始标记”阶段开启多线程并发执行。

`-XX:+CMSParallelRemarkEnabled` 这个参数会在CMS垃圾回收器的“重新标记”阶段开启多线程并发执行。

`-XX:+CMSScavengeBeforeRemark` 这个参数会在CMS的重新标记阶段之前，先尽量执行一次Young GC

`-XX:+UseConcMarkSweepGC` jvm参数指定开启CMS收集器 此时 `-XX：UseParNewGC` 会自动开启

`-XX:+UseCMSCompactAtFullCollection` 默认就打开了他意思是在Full GC之后要再次进行“Stop the World”，停止工作线程，然后进行碎片整理，就是把存活对象挪到一起，空出来大片连续内存空间，避免内存碎片

`-XX:CMSFullGCsBeforeCompaction` 这个意思是执行多少次Full GC之后再执行一次内存碎片整理的工作，默认是0，意思就是每次Full GC之后都会进行一次内存整理。

CMS垃圾回收器采取的是 垃圾回收线程和系统工作线程尽量同时执行的模式来处理的。

CMS在执行一次垃圾回收的过程一共分为4个阶段：
1. initial-mark 初始标记  STW 标记出来所有GC Roots直接引用的对象 
1. concurrent-mark 并发标记 由第一阶段标记过的对象出发  所有可达的对象都在本阶段标记 进行GC Roots追踪
1. concurrent-preclean 并发预清理阶段，也是一个并发执行的阶段。在本阶段，会查找前一阶段执行过程中,从新生代晋升或新分配或被更新的对象。通过并发地重新扫描这些对象，预清理阶段可以减少下一个stop-the-world 重新标记阶段的工作量。
1. concurrent-abortable-preclean 并发可中止的预清理阶段 这个阶段其实跟上一个阶段做的东西一样，也是为了减少下一个STW重新标记阶段的工作量。增加这一阶段是为了让我们可以控制这个阶段的结束时机，比如扫描多长时间（默认5秒）或者Eden区使用占比达到期望比例（默认50%）就结束本阶段。
1. remark(CMS Final Remark) 重新标记  STW 暂停所有用户线程，从GC Root开始重新扫描整堆，标记存活的对象。需要注意的是，虽然CMS只回收老年代的垃圾对象，但是这个阶段依然需要扫描新生代，因为很多GC Root都在新生代，而这些GC Root指向的对象又在老年代，这称为“跨代引用”。
1. concurrent-sweep  并发清理  清理掉之前标记为垃圾的对象

CMS垃圾回收的触发时机，其中有一个就是当老年代内存占用达到一定比例了，就自动执行GC。

#### ParallelGC

#### ParallelOldGC

#### G1

`-XX:+UseG1GC` 启用G1
`-XX:G1HeapRegionSize` 指定Region大小
`-XX:G1NewSizePercent` 设置新生代初始占比
`-XX:G1MaxNewSizePercent` 设置新生代最大占比  最多新生代的占比不会超过60%
`-XX:MaxGCPauseMillis` G1执行GC的时候最多可以让系统停顿多长时间 默认值是200ms
`-XX:G1MixedGCCountTarget` 最后一个阶段执行几次混合回收，默认值是8次
`-XX:G1HeapWastePercent` 默认5% 回收过程一旦空闲出来的Region数量达到了堆内存的5%，此时就会 立即停止混合回收
`-XX:G1MixedGCLiveThresholdPercent` 默认值是85% 确定要回收的Region的时候，必须是存活对象低于85%的Region才可以进行回收
他最大的一个特点，就是把Java堆内存拆分为多个大小相等的Region
然后G1也会有新生代和老年代的概念，但是只不过是逻辑上的概念,也就是说，新生代可能包含了某些Region，老年代可能包含了某些Reigon
最多可以有2048个Region
大对象的判定规则就是一个大对象超过了一个Region大小的50%
一个大对象如果太大，可能会横跨多个Region来存放 单独的region来存放大对象

老年代占堆内存45%的时候触发的Mixed垃圾回收
##### 过程

1. 初始标记 STW
2. 并发标记
3. 最终标记 STW
4. 混合回收 STW

##### 设置HeapRegion的大小 
1. 手动设置HeapRegion的大小，范围是2的0～5次方MB，如果指定的不是此范围的指，G1会自动调整
2. 启发式推断 G1本身通过算法（与堆大小和分区数量相关）自动计算出region大小

##### 分区数量

分区数量 默认是2048

G1 不能手动指定分区数量

#### ZGC

#### Shenandoah


#### 总结
自JDK 9开始，ParNew(新生代)加CMS收集器(老年代)的组合就不再是官方 推荐的服务端模式下的收集器解决方案了



### 其它JVM参数
- `-XX:+TraceClassLoading` Enables tracing of classes as they are loaded. By default, this option is disabled and classes are not traced.
- `-XX:+TraceClassUnloading`  Enables tracing of classes as they are unloaded. By default, this option is disabled and classes are not traced.
- `-XX:+DisableExplicitGC` 禁止显式执行GC，不允许你来通过代码触发GC
- `-XX:SurvivorRatio=6` 
  sets the ratio between each survivor space and eden to be 1:6, each survivor space will be one eighth of the young generation. The default for Solaris is 32. If survivor spaces are too small, copying collection overflows **directly into the old generation**. If survivor spaces are too large, they will be empty. At each GC, the JVM determines the number of times an object can be copied before it is tenured, called the tenure threshold. This threshold is chosen to keep the survivor space half full.
  Use the option `-XX:+PrintTenuringDistribution` to show the threshold and ages of the objects in the new generation. It is useful for observing the lifetime distribution of an application.

### JVM 参数模版

8G内存的模版 
```
-Xms4G -Xmx4G -Xmn3G -Xss1M  -XX:MetaspaceSize=256M -XX:MaxMetaspaceSize=256M -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=92 -XX:+UseCMSCompactAtFullCollection -XX:CMSFullGCsBeforeCompaction=0 -XX:+CMSParallelInitialMarkEnabled -XX:+CMSScavengeBeforeRemark -XX:+DisableExplicitGC  -XX:+PrintGCDetails -Xloggc:gc.log -XX:+HeapDumpOnOutOfMemoryError  -XX:HeapDumpPath=/usr/local/app/oom
```

### 名词

1. Minor GC   指目标只是新生代的垃圾收集。
2. Young GC   指目标只是新生代的垃圾收集。
3. Full GC    收集整个Java堆和方法区的垃圾收集。
4. Old GC     指目标只是老年代的垃圾收集。目前只有CMS收集器会有单 独收集老年代的行为
5. Major GC   指目标只是老年代的垃圾收集。目前只有CMS收集器会有单 独收集老年代的行为。另外请注意“Major GC”这个说法现在有点混淆，在不同资料上常有不同所指， 需按上下文区分到底是指老年代的收集还是整堆收集。
6. Mixed GC   指目标是收集整个新生代以及部分老年代的垃圾收集。目前只有G1收 集器会有这种行为。

### 注意事项
  
JVM默认使用 `AdaptiveSizePolicy` 策略自动分配Eden和Survivor空间大小。 
`-XX:-UseAdaptiveSizePolicy` 使用此命令禁用自动分配

使用CMS的话默认是禁用自动分配

### JVM 监控系统 

Zabbix、OpenFalcon、Ganglia 

### 你应该如何在面试中回答JVM生产优化问题
 
就是把之前学习过的知识，归纳总结出来一套通用的方法付论，然后面试的时候就聊这套通用方法论即可
频繁full GC的原因
- 一个对象在年轻代里躲过15次垃圾回收，年龄太大了，寿终正寝，进入老年代
- 系统流量激增 导致每次YoungGC的存活对象 suvivor无法容纳 直接进入老年代
- 系统频繁生成大对象，直接进入老年代
- YongGC后的存活对象大于suvivor的50% 此时会判断如果年龄1+年龄2+年龄N的对象总和超过了Survivor区域的50%，此时年龄N以及之上的对象都进入老年代，这是动态年龄判定规则
- 系统代码层面有显示的调用`System.gc();`




### 其它STW的原因

除了GC可能会导致STW的以外，还有有其它的原因STW，比如一些确定的 [VM operations](http://hg.openjdk.java.net/jdk9/jdk9/hotspot/file/0e31ab6e8375/src/share/vm/runtime/vm_operations.hpp ''), [JVMTI operations](http://docs.oracle.com/javase/8/docs/platform/jvmti/jvmti.html#FollowReferences ''), [JIT actions](https://github.com/gvsmirnov/java-perv/blob/master/labs-8/src/main/java/ru/gvsmirnov/perv/labs/safepoints/Deoptimization.java '')

[其它好的文章](https://www.zhihu.com/question/57722838 '')
[CMS-美团的博客](https://tech.meituan.com/2020/11/12/java-9-cms-gc.html '')
[metaspace GC](https://zhuanlan.51cto.com/art/201706/541920.htm '')
[CMS GC 触发条件](https://cloud.tencent.com/developer/article/1445735 '')



### 分析工具

- jmap    堆内存分析工具
	- jmap -heap pid该命令用于：展示pid的整体堆信息，
	- jmap -dump:live,format=b,file=sif.hprof pid
- jps     java进程查询
- jinfo   
- jstat   
- jstack  
- [gcviewer](https://github.com/chewiebug/GCViewer '')
### 参考文档

- https://docs.oracle.com/javase/8/docs/technotes/guides/vm/gctuning/ 
- https://docs.oracle.com/javase/8/docs/index.html
- https://docs.oracle.com/javase/8/docs/technotes/tools/windows/java.html man手册
- https://docs.oracle.com/javase/8/docs/technotes/tools/windows/jps.html man手册


## 类加载&执行子系统


#### 类加载器 ClassLoader
Java虚拟机设计团队有意把类加载阶段中的“通过一个类的**全限定名**来获取描述该类的二进制字节流”这个动作放到Java虚拟机外部去实现，以便让应用程序自己决定如何去获取所需的类。实现这个动作的代码被称为“类加载器”(Class Loader)。


比较两个类是否“相等”，只有在这两个类是由同一个类加载器加载的前提下才有意义，否则，即使这两个类来源于同一个Class文件，被同一个Java虚拟机加载，只要加载它们的类加载器不同，那这两个类就必定不相等。

这里所指的“相等”，包括代表类的Class对象的`equals()`方法、`isAssignableFrom()`方法、`isInstance()`方法的返回结果，也包括了使用`instanceof`关键字做对象所属关系判定等各种情况。



#### 双亲委派模型

JDK8及之前版本的三层类加载器

1. **Bootstrap Class Loader**
	HotSpot中由C++语言实现，是虚拟机自身的一部分。这个类加载器负责加载存放在 `<JAVA_HOME>\lib`目录，或者被`-Xbootclasspath`参数所指定的路径中存放的，而且是Java虚拟机能够 识别的(按照文件名识别，如`rt.jar`、`tools.jar`，名字不符合的类库即使放在lib目录中也不会被加载)类 库加载到虚拟机的内存中。通过这个类加载的，在java代码中获取`classloader`的时候返回的是`null`

1. **扩展类加载器(Extension Class Loader)**
	这个类加载器是在类`sun.misc.Launcher$ExtClassLoader`中以Java代码的形式实现的。它负责加载`<JAVA_HOME>\lib\ext`目录中，或者被`java.ext.dirs`系统变量所指定的路径中所有的类库。
	JDK9之后，引入了模块化的机制，这个类就退出了历史舞台了。

1. **应用程序类加载器(Application Class Loader)**
	这个类加载器由`sun.misc.Launcher$AppClassLoader`来实现。由于应用程序类加载器是`ClassLoader`类中的`getSystemClassLoader()`方法的返回值，所以有些场合中也称它为“系统类加载器”。它负责加载用户类路径 (ClassPath)上所有的类库，开发者同样可以直接在代码中使用这个类加载器。如果应用程序中没有自定义过自己的类加载器，一般情况下这个就是程序中默认的类加载器。

1. **自定义类加载器**
	用户可以自己在java代码中声明一个类加载器，但是父加载器只能是“Application Class Loader”，这样就可能会出现，因为自定义的类加载器不同，导致的`ClassNotFoundException`


Parents Delegation Model，双亲委派模型要求除了顶层的启动类加载器外，其余的类加载器都应有自己的父类加载器。不过这里类加载器之间的父子关系一般不是以继承(Inheritance)的关系来实现的，而是通常使用组合(Composition)关系来复用父加载器的代码。

![](./pic/class-loader-%E5%8F%8C%E4%BA%B2.svg)

双亲委派模型的工作过程是:如果一个类加载器收到了类加载的请求，它首先不会自己去尝试加载这个类，而是把这个请求委派给父类加载器去完成，每一个层次的类加载器都是如此，因此所有的加载请求最终都应该传送到最顶层的启动类加载器中，只有当父加载器反馈自己无法完成这个加载请求(它的搜索范围中没有找到所需的类)时，子加载器才会尝试自己去完成加载。



#### ClassLoader加载类的流程

Java代码中具体的类加载是通过,`Class`类中的`loadClass`方法来完成的
```java
    protected Class<?> loadClass(String name, boolean resolve)
        throws ClassNotFoundException
    {
        synchronized (getClassLoadingLock(name)) {
            // First, check if the class has already been loaded
			// 从jvm缓存中查找类是否存在，这个地方应该是线程内部的缓存
            Class<?> c = findLoadedClass(name);
            if (c == null) {
                try {
                    if (parent != null) {
                        c = parent.loadClass(name, false);
                    } else {
                        c = findBootstrapClassOrNull(name);
                    }
                } catch (ClassNotFoundException e) {
                    // ClassNotFoundException thrown if class not found
                    // from the non-null parent class loader
                }
                // 一些不相关的代码
				if (c == null) {
					// 此方法在ClassLoder类中是空的，需要子类来具体实现，也就是
                    c = findClass(name);
                }
            }
            if (resolve) {
				// jdk11这个方法已经没用了。
                resolveClass(c);
            }
            return c;
        }
    }
```

1. 从vm缓存中查找
1. 从父类加载器中查找，如果父类加载器为空，则从`Bootstrap Class Loader`中查找
1. 从自己的`findClass`重载方法中查找
1. 抛出异常

#### 破坏双亲委派模型

一些开源组件，为了达到一定的目的，破坏了tomcat的双亲委派模型，
比如 [tomcat](../javaee/tomcat/tomcat.md)


## 市面上的一些JVM实现
- Sun Classic/Exact VM: 世界上第一款商用Java虚拟机
- Hotspot： 目前使用的最多的 Java 虚拟机。
- Mobile/Embedded VM: 
- BEA JRockit： 原来属于BEA 公司，曾号称世界上最快的 JVM，后被 Oracle 公司收购，合并于 Hotspot
- J9:  IBM 有自己的 java 虚拟机实现，它的名字叫做 J9. 主要是用在 IBM 产品（IBM WebSphere 和 IBM 的 AIX 平台上）
- TaobaoVM: 只有一定体量、一定规模的厂商才会开发自己的虚拟机，比如淘宝有自己的 VM,它实际上是 Hotspot 的定制版，专门为淘宝准备的，阿里、天 猫都是用的这款虚拟机。
- LiquidVM: 它是一个针对硬件的虚拟机，它下面是没有操作系统的（不是 Linux 也不是 windows）,下面直接就是硬件，运行效率比较高。随着JRockit虚拟机终止开发，Liquid VM 项目也已经停止了。
- zing: 它属于 zual 这家公司，非常牛，是一个商业产品，很贵！它的垃圾回收速度非常快（1 毫秒之内），是业界标杆。它的一个垃圾回收的算法后来被 Hotspot 吸收才有了现在的 ZGC。
- Apache Harmony/Google Android Dalvik VM

