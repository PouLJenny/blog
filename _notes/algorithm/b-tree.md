# B tree

[wiki](https://en.wikipedia.org/wiki/B-tree '')
发明B-Tree的paper
[paper Organization and maintenance of large ordered indices](https://infolab.usc.edu/csci585/Spring2010/den_ar/indexing.pdf '')

https://www.cpp.edu/~ftang/courses/CS241/notes/b-tree.htm


模拟过程的网页 
https://www.cs.usfca.edu/~galles/visualization/BTree.html

Node,Element

## 定义

下面取自《数据结构（C语言版）》书(P238)中的定义: 
一棵m阶的B-树，或为空树，或为满足下列特性的m叉树
1. 树中每个节点最多含有m棵子树
2. 若根结点不是叶子结点则至少有两棵子树
3. 除根之外的所有非叶子结点至少有$\lceil m/2 \rceil$棵子树 
4. 所有的非叶子结点中包含下列信息数据
$(n,A_0,K_1,A_1,K_2,A_2,\dots,k_n,A_n)$
其中$k_i$为关键字,且$K_i < K_{i+1}(i=i,\dots,n-1)$.
$A_i$为指向子树根结点的指针，且指针$A_{i-1}$所指子树中所有结点的关键字都小于$K_i$,
$A_n$所指子树中所有结点的关键字都大于$K_n$
$n(\lceil m/2 \rceil - 1 \le n \le m-1)$为关键字的个数
5. 所有叶子结点都出现在同一层次上，并且不携带信息（可以看作是外部结点或者是查找失败的结点,实际上这些结点不存在，指向这些结点的指针为空）


## reference
《数据结构（C语言版）》-严蔚敏 ISBN=978-7-302-02368-5