# 论文

## 初步想法是DDD

## 其他方向

非常棒的选择！**大规模图算法（Large-Scale Graph Algorithms）** 是一个兼具**理论挑战**与**工程落地性**的研究方向，广泛应用于：

* 社交网络分析（Facebook、微博）
* 推荐系统（抖音、淘宝）
* 金融风控（反欺诈图）
* 搜索引擎（网页链接图）
* 知识图谱、图神经网络（GNN）

你在这个方向上写硕士论文非常有前途，而且**容易拿到实用结果 + 有投稿潜力**。

---

## ✅ 一、什么是大规模图算法？

研究**如何在**以下约束下\*\*高效处理图结构数据：

* 节点/边数量巨大（百万\~十亿级）
* 图动态变化频繁（动态图）
* 图不全装入内存（分布式/外存处理）
* 实时性要求高（社交网络分析、推荐）

---

## 🧭 二、适合硕士研究的热门子方向 + 示例选题

我给你整理了 5 个 **非常适合硕士论文的子方向和题目**，可理论+实践结合：

---

### 1. **动态图算法（Dynamic Graph Algorithms）**

> 图结构在不断变化（加边/删边/更新），如何快速维护重要属性？

#### 📌 可研究问题：

* 实时维护社群结构 / 连通性 / PageRank / 最短路径
* 更新成本 vs 准确度的权衡

#### 🧪 示例论文题目：

* **《一种用于动态社交网络的高效近似影响力传播算法》**
* **《支持边权更新的快速 PageRank 近似算法研究》**

#### ✅ 实际数据来源：

* SNAP 数据集：Facebook、Twitter、Email 网络

---

### 2. **分布式图计算优化（Distributed Graph Algorithms）**

> 图太大装不下单机 → 拆成多个节点并行计算

#### 📌 可研究问题：

* 图划分算法：如何把图分到多个节点，通信最小？
* Pregel / GraphX 框架下优化 PageRank、SSSP 算法

#### 🧪 示例论文题目：

* **《基于边裁剪的高效图划分算法在Pregel系统中的应用研究》**
* **《一种用于社交推荐的分布式近似个性化 PageRank 设计》**

#### ✅ 工具推荐：

* GraphX（Spark）、GraphScope、Giraph、SNAP

---

### 3. **图压缩与近似计算（Graph Sketching & Approximation）**

> 在大图中如何用较少资源得到“足够好的”近似答案？

#### 📌 可研究问题：

* 稀疏子图抽取（Spanners）
* 用 Sampling / Sketching 来估计连通度/中心性

#### 🧪 示例论文题目：

* **《结合稀疏化与采样的高效社交网络中心性近似算法》**
* **《用于边采样的误差可控图Sketch结构研究》**

---

### 4. **图在推荐系统中的应用（Graph-based Recommendation）**

> 利用用户-物品图结构优化推荐流程

#### 📌 可研究问题：

* 个性化 PageRank 推荐算法优化
* 基于图的冷启动推荐策略

#### 🧪 示例论文题目：

* **《结合图扩散与路径过滤的用户冷启动推荐算法》**
* **《用于大规模图推荐的可扩展多阶近似采样方法》**

#### ✅ 数据集参考：

* Amazon Reviews、MovieLens、Yelp、Douban

---

### 5. **图神经网络预处理中的算法优化（GNN Preprocessing）**

> GNN在训练前需要对图做子图采样、稀疏化等预处理

#### 📌 可研究问题：

* 优化采样算法效率（如GraphSAINT、FastGCN）
* 大图子图选择策略与精度影响分析

#### 🧪 示例论文题目：

* **《稀疏邻居采样算法对图神经网络训练效果的影响研究》**
* **《结合跳跃连接与路径压缩的图神经采样优化》**

#### ✅ 工具推荐：

* PyG（PyTorch Geometric）、DGL、GraphSAINT

---

## 🧩 三、研究生论文写作建议（按阶段划分）

| 阶段             | 建议任务                                        | 工具推荐                      |
| -------------- | ------------------------------------------- | ------------------------- |
| **前期：选题+文献**   | 阅读近3年 SODA, WWW, KDD, ICDM, NeurIPS 图算法相关论文 | Google Scholar, arXiv     |
| **中期：建模+算法设计** | 提出你自己的优化算法/变体，理论分析                          | Python, NetworkX, Jupyter |
| **后期：实验验证**    | 用公开数据集做对比实验（效率/准确率）                         | SNAP, PyG, Matplotlib     |
| **写作阶段**       | 规范撰写论文结构，做好图表、公式                            | LaTeX, Overleaf           |

---

## 📚 四、建议的学习资料和参考资源

### 📘 推荐书籍：

* 《Algorithm Design》（Kleinberg & Tardos）→ 经典图算法书
* 《Mining of Massive Datasets》（Stanford）→ 含分布式图算法
* 《Graph Representation Learning》→ 图神经与图采样

### 📝 入门必读论文（方向可变）：

1. *Graph sparsification by effective resistances* (Spielman, 2011)
2. *Dynamic influence maximization under uncertainty* (AAAI 2023)
3. *Scaling Personalized PageRank via Sparse Bookmark-Coloring Vectors* (WSDM 2016)

---

## ✍️ 五、我们可以从这里开始（行动建议）

现在你可以从以下 3 个方向中选一个，我们就可以立即进入选题细化 + 阅读论文 + 搭建实验环境：

| 编号 | 方向                  | 你选哪个？             |
| -- | ------------------- | ----------------- |
| ①  | **动态图分析：实时传播/社群发现** | ✅适合做创新优化+有真实图数据   |
| ②  | **图划分与分布式计算优化**     | ✅适合结合工程系统，论文可写性强  |
| ③  | **图推荐系统中的算法优化**     | ✅应用强，工业界价值高，结果可展示 |

---

你告诉我你最想从哪个方向开始，我可以：

* 给你设计一个**具体论文题目 + 实验路线**
* 推荐3\~5篇入门论文 + 数据集 + 工具
* 按周帮你制定研究进度

👉 **你现在想选哪一个方向？** 或者你也可以告诉我你感兴趣的实际应用场景（比如社交网络、推荐系统、知识图谱等），我们从那入手！


## 查论文的渠道

1. 中国知网 https://www.cnki.net/
1. 万方数据知识服务平台,内容以理工类文献和科技信息为主，也有一部分经济、金融、社会、人文以及生活实用信息。 https://wanfangdata.com.cn/index.html
1. 维普中文期刊全文数据库 https://wwwv3.cqvip.com/
1. Elsevier数据库产品: Science Direct、SCOPUS、SCIRUS
    1. Science Direct,是Elsevier公司的核心产品，是全学科的全文数据库，集世界领先的经同行评审的科技和医学信息之大成, https://www.sciencedirect.com/
    1. SCOPUS, https://www.scopus.com
    1. Mendeley, 是Elsevier旗下的文献管理器， https://www.mendeley.com
1. [Lancet](https://www.thelancet.com/) 侧重医学领域的论文
1. Web of science核心合集, Thomson公司将SCI(Science Citation Index),SSCI(Social Science Citation Index)以及AHCI（Arts & Humanities Citation Index）整合,利用互联网开放环境，创建了网络版的多学科文献数据库，https://apps.webofknowledge.com
1. NCBI美国国立生物技术信息中心,National Center for Biotechnoleg Information, https://www.ncbi.nlm.nih.gov/ https://www.nlm.nih.gov/
    1. PubMed文献数据库，提供生物医学方面的论文文献搜索服务 https://pubmed.ncbi.nlm.nih.gov/
1. 各个省市图书馆， [国家图书馆](https://www.nlc.cn/web/index.shtml) [中国优秀硕士学位论文](http://202.106.125.35/kns55/brief/result.aspx?dbPrefix=CMFD)
1. [Google Scholar](https://scholar.google.com/)
1. DBLP计算机科学文献集成检索系统 https://dblp.uni-trier.de
1. 百度学术 http://xueshu.baidu.com
1. 中外文数据库
1. DOI,Digital Object Unique Identifier,即数字对象唯一标识符。每篇论文都有一个对应的DOI，DOI就是确定的，不会再改变。
1. Sci-Hub 文献下载平台： https://pismin.com/
1. 中国人民大学图书馆： http://www.lib.ruc.edu.cn
1. 科学社交网络，号称学术界的Facebook，Research Gate https://www.researchgate.net/
1. 数据共享网站
    1. Dryad科研人员 https://datadryad.org
    1. Kaggle 数据建模和数据分析竞赛平台 https://www.kaggle.com/
1. 公开数据集
    1. 金融数据
        1. 美国劳工部官方统计数据 http://download.bls.gov
        1. 美国股票和新闻数据 https://www.kaggle.com/aaron7sun/stocknews
        1. HomeSite 保险定价竞赛数据 https://www.kaggle.com/c/homesite-quote-conversion

## 常见的索引的区别

1. SCI(Science Citation Index)，科学引文索引，包括有：自然科学、生物、医学、农业、技术和行为科学等，主要侧重基础科学。
1. EI，EngineeringIndex，工程索引，
1. SSCI，社会科学引文索引，为美国科学情报研究所建立的综合性社科文献数据库，涉及，经济、法律、管理、心理学、区域研究、社会学、信息科学等
1. CSSCI,中文社会科学引文索引，有南京大学研制成功的、我国人文社会科学评价领域的标志性工程
1. AHCI,艺术和人文引文索引，是美国科技信息所编辑出版的用于对人文和社科论文数量进行统计分析的大型检索工具，是SCI的姐妹篇

清华大学一个比较厉害的人物 [姚期智](https://iiis.tsinghua.edu.cn/zh/yao/),第一个获得图灵奖、京都奖的中国人（出生中国，生长台湾，台湾大学物理学学士、哈佛大学物理学博士、伊利诺伊大学计算机科学博士），