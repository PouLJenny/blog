---
layout: post
title:  "离散数学"
date:   2023-03-02 10:00:00 +0800
categories: 数学
tags: 数学
permalink: /math/discrete
published: true
publish_file: 2023-03-02-math-discrete.md
toc: true
---
# 离散数学


## 定义和研究范围
https://zh.wikipedia.org/wiki/%E7%A6%BB%E6%95%A3%E6%95%B0%E5%AD%A6  
离散数学（英语：Discrete mathematics）是数学的几个分支的总称，研究基于离散空间而不是连续的数学结构。与连续变化的实数不同，离散数学的研究对象——例如整数、图和数学逻辑中的命题——不是连续变化的，而是拥有不等、分立的值。因此离散数学不包含微积分和分析等“连续数学”的内容。


- 离散数学的主题
    - 数理逻辑
    - 集合论
    - 信息论
    - 数论
    - 组合数学
    - 图论
    - 抽象代数
    - 理论计算机科学
    - 拓扑学
    - 运筹学
    - 博弈论、决策论、效用理论、社会选择理论
    - 离散化
    - 连续数学的离散近似
    - 离散和连续混合数学

## 参考书
《离散数学》耿素云 [答案](http://www.daanbar.com/detail/chapter/a4545298719e11e9b34900163e104190.html )

## 数理逻辑

### 逻辑

研究人的思维的科学

1. 辩证逻辑
    - 研究人的思维中的辩证法
1. 形式逻辑
    - 研究人的思维的形式和一般规律
    - 主要是研究推理（演绎推理）的

人的思维过程：  
概念 => 判断 => 推理

### 推理

由若干个已知的判断（前提），推出新的判断（结论）的思维过程。

### 推理方法

1. 演绎推理
    - 由一般规律，个别事实，推出个别结论
1. 归纳推理
    - 由若干个别事实，推出一般结论
1. 类比推理
    - 由个别事实，推出个别结论


### 数理逻辑

用数学的方法，研究形式逻辑。  
所谓数学方法，是建立一套有严格定义的符号，即建立一套形式语言，来研究形式逻辑。所以数理逻辑，又叫做“符号逻辑”


### 原子命题
由最简单的陈述句构成的命题

### 复合命题
由若干个原子命题构成的命题。  
复合命题=原子命题+联结词

### 合式公式/ well-formed formula/ WFF

1. 单个命题变元是合式公式
1. 若A是合式公式，则$\neg$A是合式公式。
1. 若A和B是合式公式，则(A∧B)，(A∨B)，(A$\rightarrow$B)和(A$\leftrightarrow$B)都是合式公式
1. 当且仅当有限次地应用(1)，(2)，(3)所得到的含有命题变元、联结词和括号的符号串是合式公式。

### 置换定律

A是一个命题公式，X是A中的一部分且也是合式公式，如果X $\iff$ Y，用Y代替A中的X得到公式B，则A $\iff$ B



## 集合论

### 集合

**集合/元素**
A *set* is an unordered collection of distinct objects, called *elements* or *members* of the set. A set is said to contain its elements. We write a $\in$ A to denote that a is an element of the set A. The notation a $\notin$ A denotes that a is not an element of the set A.

集合的表示方式
1. 列出集合中的所有元素
A = {a,b,c,d}
2. 用谓词概括该集合中元素的属性,下面的表示B 由使P($x$)为真的全体$x$构成
B={$x \mid$ P($x$)}

常见的集合

**N**= {0, 1, 2, 3, ...}, the set of all **natural numbers** 

**Z** = {...,−2,−1,0,1,2,...}, the set of all **integers**  

**Z$^+$** = {1, 2, 3, ...}, the set of all **positive integers**  

**Q** = {p $/$ q ∣ p $\in$ Z, q $\in$ Z, and q $\neq$ 0}, the set of all **rational numbers**  

**R**, the set of all **real numbers**

**R$^+$**, the set of all **positive real numbers**

**C**, the set of all **complex numbers**.

**Tips:**  
Note that some people do not **consider 0** a natural number, so be careful to check how the term natural numbers is used when you read other books.


**广义交/广义并** 如果集合A的所有元素都是集合，则把A中所有元素的元素组成的集合为A的广义并，记作$\cup$A,A的所有元素的公共元素为A的广义交，记作$\cap$A

**幂集** 若A是集合，则吧A的所有子集组成的集合称为A的幂集，记作P(A)  
P(A) = {x | x $\sube$ A}

**基数** 
表示集合中所含元素的个数，如果集合$A$的基数是$n$，可以记为$|A| = n$


### 关系

**有序对** 由两个元素x和y(允许x=y)按一定的顺序排列成的二元组称作一个**有序对**(也称**序偶**)，记作<z,y>(也可记作(z,y))。其中x是它的第一元素,y是它的第二元素。

**有序n元组** 一个有序n元组(n$\geq$3)是一个有序对,其中第一个元素是一个有序n-1元组，一个有序n元组记作<$x_1,x_2,...,x_n$>，即
    <$x_1,x_2,...,x_n$> = <<$x_1,x_2,...,x_{n-1}$>,$x_n$>

**笛卡儿积** 设A、B为集合，用A中元素为第一元素,B中元素为第二元素,构成有序对。所有这样的有序对组成的集合称作A和B的**笛卡儿积**，记作AXB.符号化表示为
    A X B = {<x,y> | x $\in$ A $\wedge$ y $\in$ B}
 
**n阶笛卡儿积** 设A$_1$, A$_2$，...，A$_n$是集合(n$\geq$2),它们的n阶笛卡儿积记作A$_1$ X  A$_2$ X ... X A$_n$, 其中
A$_1$ X  A$_2$ X ... X A$_n$ = {<$x_1,x_2,...,x_n$> | $x_1 \in A_1 \wedge x_2 \in A_2 \wedge ... \wedge x_n \in A_n$ }

**二元关系/关系** 对集合A和B。A×B的任一子集称为A到B的一个**二元关系**，一般记作R,若<x,y>$\in$R,可记作xRy,若<x,y>$\notin$R,可记作xR<span≯</span>y。
在A=B时AXA的任一子集称为**A上的二元关系**，二元关系可简称**关系**。  
$A$上的**恒等关系**$I_A$ = {<x,x> | x $\in A$}  
$A$上的**全域关系**$E_A$ = {<x,y> | x $\in A $  $\wedge$ y  $\in A$}  
$A$上的**空关系** $\varnothing$  

关系的表示方式有**关系矩阵**和**关系图**
**关系矩阵**的一般定义：
设$A=(x_1,x_2,...,x_n)$，R是A上的关系，令
\[ r_{ij} =
\begin{split}
    \begin{cases}
        1   & \quad 若x_iRx_j    \\
        0   & \quad 若x_i\cancel{R}x_j 
    \end{cases}
    \qquad (ij=1,2,...,n)
\end{split}
\]
则
$$
(r_{i,j}) = 
 \begin{bmatrix}
  r_{11} & r_{12} & \cdots & r_{1n} \\
  r_{21} & r_{22} & \cdots & r_{2n} \\
  \vdots  & \vdots  & \ddots & \vdots  \\
  r_{n1} & r_{n2} & \cdots & r_{nn} 
 \end{bmatrix}
$$

**关系图**
设$V$是项点的集合，E是有向边的集合，令$V=A=(x_1,x_2,\cdots,x_n)$。如果$x_iRx_j$，则$x_i$到$x_j$的有向边<$x_i,,x_j$> $\in$E, 那 么 G = <V,E> 就是R的关系图 。

关系*R*的**定义域**dom*R*，**值域**ran*R*，**域**fld*R*
    dom*R* = { $x$ | $\exists y(<x,y> \in$ *R*) }
    ran*R* = { $y$ | $\exists x(<x,y> \in$ *R*) }
    fld*R* = dom*R* $\cup$  ran*R*


设F,G 为任意的关系，A为集合,则
F的**逆**记作 F$^{-1}$ = {<x,y> | yFx}
F与G的**合成**记作 F $\circ$ G = {<x,y> | $\exists z$ ($xGz \wedge zFy$)}
F在A上的**限制**记作F $\upharpoonright$ A  = {<x,y> | xFy $\wedge$ x $\in$ A}
A在F下的**像**记作 F[A] = ran(F $\upharpoonright$ A)

设R为A上的关系，n为自然数，则R的**n次幂**规定如下：
（1） R$^0$ = {<x,x> | x $\in$ A}
（2） R$^n$ = R$^{n-1}$  $\circ$ R,n $\geq$ 1
求R$^n$的方式有3种
1. 集合运算
2. 关系矩阵
3. 关系图法

有定理 
$R^m \circ R^n = R^{m+n}$
$(R^m)^n = R^{mn}$

关系的性质
||自反性(reflexive)|反自反性(irreflexive)|对称性(symmetric)|反对称性(antisymmetric)|传递性(transitive)|
|--|--|--|--|--|--|
|定义|$\forall x \space \in \space A,$  有$<x,x> \in R$|$\forall x \space \in \space A,$  有$<x,x> \notin R$|如果<x,y>$\in$ R,则<y,x>$\in$ R|如果<x,y>$\in$ R，并且x$\ne$y,则<y,x>$\notin$ R|若<x,y>$\in$ R,且 <y,z> $\in$ R，则<x,z> $\in$ R|
|集合表达式|$I_A\sube R$|$I_A \cap R = \varnothing$|$R^{-1} = R$|$R \cap R^{-1} \sube I_A$|$R \circ R \sube R$|
|关系矩阵的特点|主对角线元素都是1|主对角线元素都是0|矩阵为对称矩阵|如果$r_{ij} = 1，$ 且$i \ne j$ ,则$r_{ij} = 0$|--|
|关系图的特点|每个顶点都有环|每个顶点都没有环|两个顶点之间有0个或两个方向相反的边|两个顶点之间有0个或1个方向相反的边|如果顶点$x_i$到顶点$x_j$有边,顶点$x_j$到顶点$x_k$有边，则顶点$x_i$到顶点$x_k$也有边|


**关系的闭包** 设R是非空集合A上的关系，R的自反闭包（对称闭包，传递闭包）R'是A上的关系,且满足以下条件
1. R'是自反的（对称的，传递的）
2. R $\sube$ R'
3. 对A上的任何包含R的自反关系（对称或传递关系）R'' 都有R' $\sube$ R'' (这句话就是说R'是满足条件最小的集合)
一般将R的自反闭包记作，r(R)，对称闭包记作s(R)，传递闭包记作比t(R)。
r(R) = R $\cup$ R$^{0}$
s(R) = R $\cup$ R$^{-1}$
t(R) = R $\cup$ R$^2$ $\cup$ R$^3$ ...

**等价关系** R为非空集合A上的关系，R满足自反性、对称性和传递性，则R为集合A的等价关系.
对任何<x,y> $\in$ 等价关系R, 则记作 x~y

**等价类** R是非空集合A上的等价关系，对任意的x $\in$ A，令
    $[x]_R$ = {y|y $\in$ A $\wedge$ xRy}
,则称集合$[x]_R$为x关于R的等价类，简称x的等价类，也可记作$[x]$ 或 $\overline{x}$

**商集** 设R是非空集合A上的等价关系，以R的不交的等价类为元素的集合称为A在R下的商集，记作 A/R。
即A/R = {$[x]_R$ |  $x \space \in$ A }

**划分/划分块** 对于非空集合A，如果存在集合$\pi$满足下列条件:
1. ($\forall x$)($x \in \pi \rightarrow x \sube A$)
2. $\varnothing \notin \pi$
3. $\cup \pi$ = A
4. ($\forall x$)($\forall y$)(($x \in \pi \wedge y \in \pi \wedge x \ne y$) $\rightarrow x \cap y = \varnothing$),则称$\pi$ 为A的一个划分，称$\pi$ 中的元素为A的划分块。
A的一个划分$\pi$,是A的非空子集集合（即$\pi \sube P(A)$ 且 $\varnothing \notin \pi$）,A的这些子集互不相交，且他们的并集为A

**偏序关系** 设R为非空集合A上的关系，R满足自反性，反对称性和传递性，则称R为A上的偏序关系，简称偏序，记作 $\preccurlyeq$

**偏序集** 一个集合A与A上的偏序关系R一起称作偏序集，记作<A,R>

**盖住** 设<A,$\preccurlyeq$>为偏序集，对于任意的x,y $\in$ A,如果x $\preccurlyeq$ y或者y$\preccurlyeq$x成立则称x和y是可比的，如果x $\prec$ y (x $\preccurlyeq$ y $\wedge x \ne y$ ),且不存在z $\in$ A，使得 x $\prec$ z $\prec$ y ，则称y盖住x

**全序关系/全序集** 设<A,$\preccurlyeq$>为偏序集,对于任意的x,y $\in$ A,x和y都可比，则称$\preccurlyeq$为A上的全序关系，且称<A,$\preccurlyeq$>为全序集，由于在哈斯图上是一条直线所以也叫线序集

**哈斯图** 对于有穷的偏序集<A,$\preccurlyeq$>可以用哈斯图来表示，实际上哈斯图就是简化的关系图。在哈斯图中每个节点表示A中的一个元素，节点位置按他们在偏序中的次序从底向上排列。如果y盖住x，则在x和y之间连一条线。
 
设<A,$\preccurlyeq$>为偏序集，$B\sube A$
1. 若$\exists y \in B$使得$\forall x $($x \in B \rightarrow y \preccurlyeq$ x),则y是B的**最小元**
2. 若$\exists y \in B$使得$\forall x $($x \in B \rightarrow x \preccurlyeq$ y),则y是B的**最大元**
3. 若$\exists y \in B$使得$\neg \exists x $($x \in B \wedge x \prec$ y),则y是B的**极小元**
4. 若$\exists y \in B$使得$\neg \exists x $($x \in B \wedge y \prec$ x),则y是B的**极大元**
5. 若$\exists y \in A$使得$\forall x $($x \in B \rightarrow x \preccurlyeq$ y),则y是B的**上界**
6. 若$\exists y \in A$使得$\forall x $($x \in B \rightarrow y \preccurlyeq$ x),则y是B的**下界**
7. 令C = {y|y为B的上界}，则称C的最小元为B的**最小上界**或者是**上确界**
8. 令D = {y|y为B的下界}，则称D的最大元为B的**最大下界**或者是**下确界**

### 函数
**函数** 设F为二元关系，若对任意的x $\in$ domF,都存在唯一的y $\in$ ranF，使得xFy成立，则称F为函数.
 函数一般用大写或小写英文字母来表示，如果<x，y> $\in$函数F,则记作F(x)=y,称y是F在x的**函数值**

设A,B是集合，如果函数$f$满足以下条件
1. dom$f$ = A
2. ran$f \sube$ B

则称$f$是从A到B的函数，记作$f:A \rightarrow B$

设A,B是集合,所有从A到B的函数构成集合$B^A$,读作"**B上A**"即：
$B^A$ = {$f$ | $f:A \rightarrow B$},
一般来说如果|A| = m,|B| = n,且m、n不全是0，则|B$^A$| = n$^m$

设$f:A \rightarrow B, A' \sube A则A‘在f下的像是$:
$f(A') = \lbrace f(x) | x \in A' \rbrace = f[A']$
当A' = A时，称$f(A') = f(A) =ranf$是**函数的象**

设$f:A \rightarrow B$
1. 若ran$f=B$,则称f是**满射**的（或**到上**的）
2. 若对于任何的$x_1,x_2 \in A,x_1 \not = x_2$,都有$f(x_1)\not = f(x_2) $,则称f是**单射**的（或1对1的）
3. 若$f$既是单射又是满射的则称f是**双射**的(或**一一到上**的)

特殊的函数
1. 设$f:A \rightarrow B$,如果存在$c\in B$使得对所有的$x\in A$都有$f(x) = c$则称f是**常函数** 
2. A上的恒等关系$I_A$就是A上的**恒等函数**，对于所有的$x \in A 都有f(x) = x$
3. 设$f: R \rightarrow R$, 对于任意的$x_1,x_2 \in R$,如果$x_1 < x_2$则有，$f(x_1) \leq f(x_2)$,就称f为**单调递增**的，如果$x_1 < x_2$则有，$f(x_1) < f(x_2)$,就称f为**严格单调递增**的,类似的可以定义**单调递减函数**，**严格单调递减函数**，他们统称为**单调函数**
4. 设A为集合，对于任意的$A' \sube A,A'$的**特征函数**$\chi_{A'}:A\rightarrow \lbrace 0,1 \rbrace$,定义为:
$$
\chi_{A'} = \begin{cases}
   1 & a \in A' \\
   0 & a \in A - A'
\end{cases}
$$

5. 设R时A上的等价关系，定义一个从A到A/R的函数g:$A \rightarrow A/R$且$g(a) = [a]$.
他把A中的元素a映到a的等价类[a],称g时从A到商集A/R的**自然映射**

## 图论
### 简单图
每个边都连接两个不同的顶点且没有两条不同的边连接一对相同顶点的图
### 多重图
可能会有多重边连接同一对顶点的图
### 伪图
包含环或存在多重边连接同一对顶点或同一个顶点的图

### 有向图
一个有向图（V,E）由一个非空顶点集V和一个有向边（或弧）集E组成。每条有向边与一个顶点有序对相关联。与有序对（u,v）相关联的有向边开始与u，结束于v

### 简单有向图
当一个有向图不包含环和多重有向边，每个有序对
### 有向多重图

### 混合图
即包含有向边又包含无向边的图

**握手定理(Handshaking)**
设无向图 G=<V,E> 有n个顶点，m条边，则G中所有顶点的度之和等于m的两倍

\[
\sum_{i=1}^{n} d(v_i) = 2m
\]

**推论**
无向图中度数为奇数的顶点个数恰有偶数个

**定理**
设有向图 G=<V,E> 有n个顶点，m条边，则G中所有顶点的入度之和等于所有顶点的出度之和，也等于m。

**欧拉定理**
设G为一平面连通图，v为其顶点数，e为其边数，r为其面数则

v - e + r = 2


## 组合数学

组合数学是算法的理论基础

### 参考书
1. 《组合数学》5 卢开澄  中国人写的书就是直接说定理，自学的话相对比较费劲
1. 《Introductory Combinatorics》 by Richard A. Brualdi

### 排列与组合

1. 排列/Permutation/Arrangement
    从n中取r个排列的模型： 可以看作 r个不同的盒子，n个不同的球，放入盒子中且盒子不能为空 n >= r
    $P(n,r) = \frac {n!}{(n-r)!}$

1. 不可重复组合/Combination
    从n中取r个组合的模型： 可以看作 r个相同的盒子，n个不同的球，放入盒子中且盒子不能为空 n >= r
    $C(n,r) = \dbinom{n}{r} = \frac {P(n,r)}{P(r,r)} = \frac {n!}{(n-r)!r!}$
1. 圆桌排列
将排列排列成一个圆周，在n个中取r个在圆周上排列数以$Q(n,r) = \frac{P(n,r)}{r}$表示

1. 可重复的组合
允许重复的组合的模型是r个相同的球，n个不同的盒子，取r个球，每个盒子允许多于一个球
定理：
在n个不同元素中取r个作允许重复的组合，其组合数为$C(n+r-1,r)$

1. 不相邻的组合
从$A=\{1,2,3,...,n\}$中取r个不相邻的数组合，数量为$C(n-r+1,r)$
个人认为： 如果r > n/2 则一定有相邻的数所以 n - r + 1 > r

1. 线性方程的整数解个数
线性方程 $x_1 + x_2 + ... + x_n = b$,n和b都是整数，n >= 1 的非负整数解的个数是$C(n+b-1,b)$

1. $\dbinom{n}{r} = \dbinom{n}{n-r}$

1. $\dbinom{n}{r} = \dbinom{n-1}{r} + \dbinom{n-1}{r-1}$

1. $C(n+r+1,r)=C(n+r,r) + C(n+r-1,r-1) + C(n+r-2,r-2) + ... + C(n + 1,1) + C(n,0)$

1. $\dbinom{n}{l}\dbinom{l}{r} = \dbinom{n}{r}\dbinom{n-r}{l-r},(l \ge r)$

1. $C(m,0) + C(m,1) + C(m,2) + ... + C(m,m) = 2^m$

1. $\dbinom{n}{0} - \dbinom{n}{1} + \dbinom{n}{2} - ... \pm \dbinom{n}{n}= 0$

1. Stirling公式
近似求n!
$n! \thicksim \sqrt{\smash{2n\pi}}(\frac{n}{e})^n$

1. $\binom{m}{k_1,k_2,\dots,k_n} = \frac{m!}{k_1!k_2!\dots k_n!}$ 其中 $m> 0, k_1 + k_2 + \dots + k_n = m$
    证明：
    $\binom{m}{k_1,k_2,\dots,k_n} $ 
    $= \binom{m}{k_1} \times \binom{m - k_1}{k_2} \times \dots \times \binom{m - k_1 - k_2 - \dots - k_{n-1}}{k_n}$
    $= \frac{m!}{(m-k_1)!k_1!} \times \frac{(m-k_1)!}{(m-k_1-k_2)!(k_2)!} \times \dots \times \frac{(m - k_1 - k_2 - \dots - k_{n-1})!}{(m - k_1 - k_2 - \dots - k_{n-1} - k_n)!(k_n)!}$
    $= \frac{m!}{k_1!k_2!\dots k_n!}$

### 递推关系与母函数

1. 河内塔问题
1. Fibonacci序列
1. 母函数
    对于序列 $C_0,C_1,C_2$,... 构造一个函数
    $G(x) = C_0 + C_1x + C_2x^2 + ...$
    称G(x)为序列$C_0,C_1,C_2$,...的母函数
    序列长度可能是**有限**的，也可能是**无限**的。


### 容斥原理


$|A \cup B  \cup C| = |A| + |B| + |C|  - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C| $

同理：
$|A \cup B  \cup C \cup D| = |A| + |B| + |C| + |D|  - |A \cap B| - |A \cap C| - |A \cap D| - |B \cap C| - |B \cap D| - |C \cap D| + |A \cap B \cap C| + |A \cap B \cap D| + |A \cap C \cap D| + |B \cap C \cap D| - |A \cap B \cap C \cap D|$

同理再推广到一般情况
$|A_1 \cup A_2 \cup ... \cup A_n|$
= $$

由于$ \overline{A_1 \cup A_2 \cup ... \cup A_n}  = \overline{A_1} \cap \overline{A_2} \cap ... \cap \overline{A_n} $
所以：
$ ｜\overline{A_1} \cap \overline{A_2} \cap ... \cap \overline{A_n}｜  = ｜\overline{A_1 \cup A_2 \cup ... \cup A_n}｜$
= $N - |A_1 \cup A_2 \cup ... \cup A_n|$


### 鸽巢原理/抽屉原理

有$n + 1$只鸽子,只有n个巢，则至少有一鸽巢有两只鸽子


### n对夫妻问题


## EOF