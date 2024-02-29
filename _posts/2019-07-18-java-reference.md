---
layout: post
title:  "java中的引用类型"
date:   2023-06-24 20:07:07 +0800
categories: java
tags: java
permalink: /java/reference
published: true
publish_file: 2019-07-18-java-reference.md
toc: true
---

# java中的引用类型

在包`java.lang.ref`下面声明了一系列的java引用类型，作用主要是跟GC相关

## 强引用 StongReference
最常用的、默认的引用类型
```java
Object o = new Object();
```
## 软引用 SoftReference
软引用的强度是仅次于强引用的，如果一个对象只具有软引用，则内存空间足够，垃圾回收器就不会回收它； 如果内存空间不足了，就会回收这些对象的内存。只要垃圾回收器没有回收它，该对象就可以被程序使用。 软引用可用来实现**内存敏感的高速缓存**

```java
String str=new String("abc");                                 
SoftReference<String> softRef = new SoftReference<>(str);
str = null;
System.out.println(softRef.get());
System.gc();
System.out.println(softRef.get());
```

## 弱引用 WeakReference
弱引用的强度比软引用更次，也就是说只具有弱引用的对象拥有更短暂的生命周期。 在垃圾回收器线程扫描它所管辖的内存区域的过程中，一旦发现了**只具有弱引用**的对象，不管当前内存空间足够与否，都会回收它的内存。 不过，由于垃圾回收器是一个优先级很低的线程，因此不一定会很快发现那些只具有弱引用的对象。 如果这个对象是偶尔的使用，并且希望在使用时随时就能获取到，但又不想影响此对象的垃圾收集，那么你应该用 `WeakReference` 来标记此对象。

```java
@Test
public void weakReference2() {
    int size = 3;  
    LinkedList<WeakReference<VeryBig>> weakList = new LinkedList<WeakReference<VeryBig>>();  
    for (int i = 0; i < size; i++) {  
        weakList.add(new VeryBigWeakReference(new VeryBig("Weak " + i), rq));  
        System.out.println("Just created weak: " + weakList.getLast());    
    } 
    System.gc();   
    try { // 下面休息几分钟，让上面的垃圾回收线程运行完成  
        Thread.sleep(6000);  
    } catch (InterruptedException e) {  
        e.printStackTrace();  
    }
    System.out.println(weakList.size());
    System.out.println(weakList);
    checkQueue();
}

private static ReferenceQueue<VeryBig> rq = new ReferenceQueue<VeryBig>();  

public static void checkQueue() {  
    Reference<? extends VeryBig> ref = null;  
    while ((ref = rq.poll()) != null) {  
        if (ref != null) {  
            System.out.println("In queue: " + ((VeryBigWeakReference) (ref)).id);  
        }  
    }  
}
@ToString(callSuper = false)
class VeryBig {  
    public String id;  
    // 占用空间,让线程进行回收
    @ToString.Exclude
    byte[] b = new byte[1 << 10 << 10];
  
    public VeryBig(String id) {  
        this.id = id;  
    }  
  
    protected void finalize() {  
        System.out.println("Finalizing VeryBig " + id);  
    }

}

class VeryBigWeakReference extends WeakReference<VeryBig> {
    public String id;  
  
    public VeryBigWeakReference(VeryBig big, ReferenceQueue<VeryBig> rq) {  
        super(big, rq);  
        this.id = big.id;  
    }  
  
    protected void finalize() {  
        System.out.println("Finalizing VeryBigWeakReference " + id);  
    }

    @Override
    public VeryBig get() {
        return super.get();
    }

    @Override
    public String toString() {
        return "VeryBigWeakReference{" +
                "id='" + id + '\'' + ", VeryBig=" + get() +
                '}';
    }
}
```

上面的代码执行完了之后有个非常神奇的效果，`WeakReference`引用的对象还在,但是`Value`却是null，被GC了。 所以被GC的判断条件应该是**只要引用链上存在弱引用就会被GC，除非有一个强引用指向这个对象**。

## 虚引用 PhantomReference
```java
// JDK源码注释
/**
 * Returns this reference object's referent.  Because the referent of a
 * phantom reference is always inaccessible, this method always returns
 * {@code null}.
 *
 * @return {@code null}
 */
public T get() {
    return null;
}
```
虚引用相对来说比较怪异，因为你不管怎么`get`都是`null`,而且必须关联引用队列。

虚引用主要用来跟踪对象被垃圾回收的活动。

当垃圾回收器准备回收一个对象时，如果发现它还有虚引用，就会在回收对象之前，把这个虚引用加入到与之关联的引用队列中。

程序如果发现某个虚引用已经被加入到引用队列，那么就可以在所引用的对象的内存被回收之前采取必要的行动。


https://cloud.tencent.com/developer/article/1843330



