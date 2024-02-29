# B$^+$ Tree
[相对来说最早的提及到B$^+$ tree的文章](https://dl.acm.org/doi/pdf/10.1145/356770.356776 )

## 定义

下面取自[维基百科](https://en.wikipedia.org/wiki/B%2B_tree#cite_note-2 )中的定义：
- Individual nodes will have either record or children, but never both at the same time: this is the main distinction from a B-tree.
- The order or branching factor b of a B$^+$  tree measures the capacity of internal nodes, i.e. their maximum allowed number of direct child nodes. This value is constant over the entire tree.
- Internal nodes have no records, but will always have nonzero children. The actual number of children m for a given internal node is constrained such that $[b/2] \le m \le b $.Each child is then referred to as $p_i$ for $i \in [1,m]$,where $p_i$ represents the child node at natural number index $i \in$ **N**
- Leaf nodes have no children, and instead contain the elements of the B$^+$  tree as records. The number of records n contained in a given leaf node must satisfy the dual inequality $[b/2] \le n \le b $
- The root is typically considered to be a special type of internal node which may have as few as 2 children.This translates to $2 \le m \le b $,For example, if the order b of a B$^+$  tree is 7,each internal node may have between $[7/2] =4 $ and 7 children,while the root may have between 2 and 7.
- In the situation where a B$^+$  tree is empty or contains exactly 1 node, the root instead becomes the single leaf. In this case, the number of keys n must satisfy $0 \le n \le b - 1$


下面取自《数据结构（C语言版）》书(P238)中的定义: 
B$^+$树是应文件系统所需而出的一种B-树的变种，一棵m阶的B$^+$树和m阶的B-树的差异在于:
1. 有n棵子树的结点中含有n个关键字
2. 所有叶子结点中包含了全部关键字的信息，及指向包含这些关键字记录的指针
3. 所有的非叶子结点可以看成是索引部分，结点中仅含有其子树中的最大关键字


## 实现
[C版本的实现](http://www.amittai.com/prose/bplustree.html )



