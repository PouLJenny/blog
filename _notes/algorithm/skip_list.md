---
layout: post
title:  "跳表"
date:   2023-06-19 13:16:00 +0800
categories: 算法
tags: 算法
permalink: /algorithm/skip-list
published: true
publish_file: 2023-06-19-algorithm-skip-list.md
toc: true
---

# Skip List / 跳表

[非常牛逼的一个博客](https://www.jianshu.com/p/9d8296562806 )
[论文 Skip Lists: A Probabilistic Alternative to Balanced Trees](https://epaperpress.com/sortsearch/download/skiplist.pdf)



## 介绍

跳表基于原始的有序链表

![](/assets/notes/algorithm/skip-list.svg)


转化成跳跃表的结构就长下面这个样子

![](/assets/notes/algorithm/skip-list-2.svg)


跳表的索引高度  h = log$_2$n,且每层索引最多遍历 3 个元素。所以跳表中查找一个元素的时间复杂度为 O(3*logn)，省略常数即：O(logn)。

假如原始链表包含 n 个元素，则一级索引元素个数为 n/2、二级索引元素个数为 n/4、三级索引元素个数为 n/8 以此类推。所以，索引节点的总和是：n/2 + n/4 + n/8 + … + 8 + 4 + 2 = n-2，空间复杂度是 O(n)。


查询相对来说比较简单。比较复杂的是怎么新增、更新和删除跳表元素


当每次有数据要插入时，先通过**概率算法**告诉我们这个元素需要插入到几级索引中

我们可以实现一个 `randomLevel()` 方法，该方法会随机生成 1~MAX_LEVEL 之间的数（MAX_LEVEL表示索引的最高层数），且该方法有 1/2 的概率返回 1、1/4 的概率返回 2、1/8的概率返回 3，以此类推。


- `randomLevel()` 方法返回 1 表示当前插入的该元素不需要建索引，只需要存储数据到原始链表即可（概率 1/2）
- `randomLevel()` 方法返回 2 表示当前插入的该元素需要建一级索引（概率 1/4）
- `randomLevel()` 方法返回 3 表示当前插入的该元素需要建二级索引（概率 1/8）
- `randomLevel()` 方法返回 4 表示当前插入的该元素需要建三级索引（概率 1/16）
- 。。。以此类推





