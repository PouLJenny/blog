# JAVA并发集合包


## ArrayList

数组实现

扩容机制： 期望的数组大小 和 老数组大小 + 老数组大小/2 对比，取大值

## LinkedList

基于双向链表来实现的

默认在队列的尾部插入元素

优点： 插入元素效率高，可以当队列使用
缺点： 不太适合在随机的位置，操作元素


## Vector和 Stack

数组实现
扩容机制： 默认扩容至原数组大小的两倍，可自定义扩容大小

## HashMap

1.8之前hash冲突用单向链表解决，之后当单向链表的长度大于8之后（也就是说在在新增第9个节点的时候）会把链表转成红黑树，
有个细节就是，链表会先从单向链表转换成双向链表，再转换成红黑树

hash优化原理:
```java
// 算法逻辑 对象hashcode值的 高16位与低16位做异或运算，结果放到原hash值的低16位上
// 通过此算法可以降低hash碰撞的概率，// TODO
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

为了避免低性能的取模运算，1.8采用了位运算替代，`(n-1) & hash`,n必须是2的x次幂，必须保证`n-1`对应的值的低位是连续的1，这样做`&`运算的时候才跟取模的效果是一样的


resize原理
扩容的时候，`内部数组容量 * 2`，链表节点在做rehash的时候，比较特殊，会判断 `2 ^ n = oldCap`，`2 ^ (n + 1) - 1 = newCap`，从低位数第`n`位是否是1，
如果是0的话 节点所处的数组index不变，如果是1的话，节点所处的数组index为 `原index值 + oldCap`,这样就能批量处理节点中的链表，提高性能 

Hash冲突的时候
向链表的尾部添加结点，如果链表长度>8,再判断数组长度，如果数组长度<64，则进行扩容操作，相反则将链表转成红黑树

## LienkedHashMap

遍历元素的时候，跟插入的顺序是一样的


1. 维护插入元素的顺序的方法
   单向链表使用： `newNode(); `红黑树是：` newTreeNode();`
2. 覆盖元素时维护顺序的方法
   `afterNodeAccess();` `LinkedHashMap`有一个属性，`accessOrder`默认是`false`，作用是当覆盖元素/get元素时是否改变元素的顺序，构造时可以设置此参数
3. 删除元素时维护顺序的方法
   `afterNodeRemoval();` 将元素从双向链表中摘除


## TreeMap

基于红黑树做的， 默认按照key的字典顺序排序，还可以构造器中指定一个排序方式

## HashSet 

基于HashMap

## LinkedHashSet

基于 LinkedHashMap

## TreeSet

基于 TreeMap

java中整个Set的集合都是基于Map来实现的，操作的就是Map中的key

// TODO 红黑树


## Iterator

迭代器的`fail fast`机制 [比较好的文章](https://www.javatpoint.com/fail-fast-and-fail-safe-iterator-in-java '')

多线程操作集合的元素时，快速失败，
通过关键变量 `modCount` 来判断是否变动，确认是否别的线程已修改
