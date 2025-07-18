# 算法

动画html
https://www.cs.usfca.edu/~galles/visualization/Algorithms.html

## books
https://www.interviewbit.com/blog/data-structures-and-algorithms-books/


## 在线课程

## 刷题
https://codetop.cc/home
https://leetcode.cn/problemset/all/
https://www.nowcoder.com/exam/company?currentTab=hostest&jobId=100&selectStatus=0&tagIds=179


## 常用的缓存淘汰算法
缓存算法是指令的一个明细表，用于决定缓存系统中哪些数据应该被清理，常见的类型包括LFU/LRU/ARC/FIFO/MRU。

### 最不经常使用算法LFU Least Frequency Used
#### 基本思想
如果数据过去被访问次数很多，那么将来被访问的频率也会很高。
#### 命中率分析
一般情况下，LFU效率要优于LRU，且能够避免周期性或者偶发性的操作导致缓存命中率下降的问题，但LRU需要记录数据的历史访问记录。一旦数据访问模式发生变更，LRU需要更长时间来适应新的访问模式，即LFU存在历史数据影响将来数据的缓存污染问题。

### 最近使用算法LRU Least Recently Used
#### 基本思想
数据数据被访问，那么将来被访问的概率很高
#### 命中率分析
当存在热点数据时LRU的效率很好，但偶发性的、周期性的批量操作会导致LRU命中率急剧下降，缓存污染情况比较严重
#### MySql对LRU的改进
将链表拆分为两部分，热数据区和冷数据区
改进之后算法流程如下:
- 访问数据如果在热数据区，与之前的LRU淘汰算法一样，移动到热数据区的头结点
- 插入数据时，若冷数据缓存已满，淘汰尾结点的数据，然后将数据插入冷数据区的头结点
- 处于冷数据区的每次被访问需要做如下判断：
    1. 若改数据已在缓存中超过一定的时间，如 1s 则移动到热数据区的头节点
    2. 若该数据存在时间小于指定阈值，则位置保持不变，
- 若热数据区域的缓存满了，则会降级进入冷数据表头    
- 对于偶发的批量查询，数据仅仅只会落入到冷数据区，然后很快就会被淘汰，热数据区的不会受到影响，这样就解决了LRU算法缓存命中率下降的问题，其他改进方法还有 LRU-K,2Q,LIRS算法

### 自适应缓存替换算法 ARC
在IBM Almaden研究中心开发，这个缓存算法同时跟踪记录LFU和LRU，以及驱逐缓存条目，来获得可用缓存的最佳使用。

### 先进先出算法 FIFO First in First out
#### 基本思想
如果一个数据最先进入缓存，则应该最早被淘汰掉


### 最近最常使用算法MRU
MRU算法最先移除最近最常使用的条目，MRU算法擅长处理条目越久，越容易被访问的情况。

### LRU-K

LRU-K中的K代表最近使用的次数，因此LRU可以认为是LRU-1。LRU-K的主要目的是为了解决LRU算法"缓存污染"的问题，其核心思想是将"最近使用过1次"的判断标准扩展为"最近使用过K次"，常用实现如下：

- 数据第一次被访问，加入到访问历史列表
- 如果数据在访问历史列表里后没有达到K次访问，则按照一定规则(FIFO，LRU)淘汰；
- 当访问历史队列中的数据访问次数达到K次后，将数据索引从历史队列删除，将数据移到缓存队列中，并缓存此数据，缓存队列重新按照时间排序；
- 缓存数据队列中被再次访问后，重新排序；
- 需要淘汰数据时，淘汰缓存队列中排在末尾的数据，即淘汰"倒数第K次访问离现在最久"的数据。

#### 命中率分析
LRU-K具有LRU的优点，同时能够避免LRU的缺点，实际应用中LRU-2是综合各种因素后最优的选择，LRU-3或者更大的K值命中率会高，但适应性差，需要大量的数据访问才能将历史访问记录清除掉。LRU-K降低了"缓存污染"带来的问题，命中率比LRU要高。

### 2Q: two queues
算法类似于LRU-2，不同点在于2Q将LRU-2算法中的访问历史队列(注意不是缓存数据的)改为一个FIFO队列，即2Q有两个缓存队列：FIFO队列和LRU队列。

当数据第一次访问时，2Q算法将数据缓存在FIFO队列里面，当数据第二次被访问时，则将数据从FIFO队列移到LRU队列里面，两个队列各自按照自己的方法淘汰数据

算法流程：

1. 新访问的数据插入FIFO队列中
2. 如果数据在FIFO中一直没有再被访问 最终按照FIFO的规则淘汰
3. 如果数据在FIFO队列中被再次访问，则将数据移入LRU队列头部
4. 如果数据在LRU队列再次被访问 则将数据移到LRU队列头部
5. LRU队列淘汰末尾的数据

### 参考链接
[博客](https://melonshell.github.io/2020/02/07/ds_cache_eli/ "")


## Papers 算法的相关论文

### SkipList
[Skip Lists: A Probabilistic Alternative to Balanced Trees](https://epaperpress.com/sortsearch/download/skiplist.pdf)

### Self‑adjusting trees
[Self‑Adjusting Binary Search Trees](https://www.cs.cmu.edu/~sleator/papers/self-adjusting.pdf)

### LSM-tree
[The Log-Structured Merge-Tree (LSM-Tree)](https://www.cs.umb.edu/~poneil/lsmtree.pdf)

### B-tree
[ORGANIZATION AND MAINTENANCE OF LARGE ORDERED INDICES ](https://dl.acm.org/doi/pdf/10.1145/1734663.1734671)

### AVL Tree
[An algorithm for the organization of information](https://zhjwpku.com/assets/pdf/AED2-10-avl-paper.pdf)

# EOF


