---
layout: post
title:  "HashMap中的Hash冲突是怎么解决的？"
date:   2023-05-22 21:58:48 +0800
categories: hashmap
tags: hashmap
permalink: /java/collection/hashmap-conflict
published: true
publish_file: 2023-05-22-java-collection-hashmap-conflict.md
toc: true
---

# HashMap中的Hash冲突是怎么解决的？

HashMap在使用过程中，不可避免的会发生Hash冲突，那Java中是怎么解决这个问题的呢？

下面直接看源码

```java
    final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
                   boolean evict) {
        Node<K,V>[] tab; Node<K,V> p; int n, i;
        if ((tab = table) == null || (n = tab.length) == 0)
            n = (tab = resize()).length;// 第一次初始化
        if ((p = tab[i = (n - 1) & hash]) == null)
            tab[i] = newNode(hash, key, value, null);
        else { // 下面的分支是Hash冲突的时候走的
            Node<K,V> e; K k;
            if (p.hash == hash &&
                ((k = p.key) == key || (key != null && key.equals(k))))
                e = p;
            else if (p instanceof TreeNode)
                e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
            else {
                for (int binCount = 0; ; ++binCount) {
                    if ((e = p.next) == null) {
                        p.next = newNode(hash, key, value, null); // 生成一个新的node结点，挂在链表的尾部
                        if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                            treeifyBin(tab, hash);
                        break;
                    }
                    if (e.hash == hash &&
                        ((k = e.key) == key || (key != null && key.equals(k))))
                        break;
                    p = e;
                }
            }
            if (e != null) { // existing mapping for key
                V oldValue = e.value;
                if (!onlyIfAbsent || oldValue == null)
                    e.value = value;
                afterNodeAccess(e);
                return oldValue;
            }
        }
        ++modCount;
        if (++size > threshold)
            resize();
        afterNodeInsertion(evict);
        return null;
    }
```

 通过第18行代码能知道，当出现Hash冲突且key的`equals`方法不相等的时候,会生成一个新的`Node`结点，挂在链表的尾部。结点的数据结构长这个样子:
```java
    static class Node<K,V> implements Map.Entry<K,V> {
        final int hash;
        final K key;
        V value;
        Node<K,V> next;

        Node(int hash, K key, V value, Node<K,V> next) {
            this.hash = hash;
            this.key = key;
            this.value = value;
            this.next = next;
        }
        ...
}
```

这里能看到是个单向链表,每次有新的冲突结点，都会在放在链表**尾部**，那为什么在尾部而不是在首部呢？这样做貌似还要遍历一边链表？

玄机在下面两行代码：
```java
if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
       treeifyBin(tab, hash);
```

这里主要是实现了两个机制：
1. 遍历到尾部是为了获得链表的总长度
2. 当总长度超过某个阈值的时候，会把单向链表转成红黑树（一种平衡二叉树）来提高查询性能。

**上面提到的第二点也是面试中经常被问到的一点**。其中的阈值就是变量`TREEIFY_THRESHOLD` 
```java
    static final int TREEIFY_THRESHOLD = 8;
```

能看到Java中是设置的8，也就是说当Hash冲突的时候链表长度**大于等于8**的时候就是转成**红黑树**！红黑树的数据结构长下面这个样子：
```java
    static final class TreeNode<K,V> extends LinkedHashMap.Entry<K,V> {
        TreeNode<K,V> parent;  // red-black tree links
        TreeNode<K,V> left;
        TreeNode<K,V> right;
        TreeNode<K,V> prev;    // needed to unlink next upon deletion
        boolean red; // 当前结点的红黑属性
        TreeNode(int hash, K key, V val, Node<K,V> next) {
            super(hash, key, val, next);
        }
        ...
}
```
红黑树的查询效率是$O(log_2n)$，比单向链表的$O(n)$性能提升特别大，尤其是数据量大的时候。

但是！但是！但是！你以为这就结束了？
有个隐藏的比较深的逻辑
```java
    final void treeifyBin(Node<K,V>[] tab, int hash) {
        int n, index; Node<K,V> e;
        if (tab == null || (n = tab.length) < MIN_TREEIFY_CAPACITY)
            resize(); // 这个地方如果HashMap中的数组长度如果小于某个阈值的时候，是直接扩容的，并不会链表转红黑树
        else if ((e = tab[index = (n - 1) & hash]) != null) {
            TreeNode<K,V> hd = null, tl = null;
            do {
                TreeNode<K,V> p = replacementTreeNode(e, null);
                if (tl == null)
                    hd = p;
                else {
                    p.prev = tl;
                    tl.next = p;
                }
                tl = p;
            } while ((e = e.next) != null);
            if ((tab[index] = hd) != null)
                hd.treeify(tab);
        }
    }
```

上面代码中的第3-4行有个关键的逻辑判断,如果HashMap中的数组长度如果小于某个阈值的时候，是直接扩容的，并不会链表转红黑树。这个阈值是多少呢：
```java
   /**
     * The smallest table capacity for which bins may be treeified.
     * (Otherwise the table is resized if too many nodes in a bin.)
     * Should be at least 4 * TREEIFY_THRESHOLD to avoid conflicts
     * between resizing and treeification thresholds.
     */
    static final int MIN_TREEIFY_CAPACITY = 64;
```

也就是说只有当链表长度大于等于8并且数组长度大于等于64的时候才会执行链表转红黑树的逻辑！

