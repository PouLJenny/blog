# NLP



## Java开源工具

[stanfordnlp](https://stanfordnlp.github.io/CoreNLP/)
[apache open nlp](https://opennlp.apache.org/)
[hanlp](https://hanlp.hankcs.com/)

### Stanford NLP



### HanLP

比较适合中文处理,其他语言不是很好


## 词嵌入 

大部分模型方法期望的输入是固定长度的数值特征向量,而不是不同长度的文本文件。所以需要词嵌入。  
词嵌入（Word Embeddings）是一种将词语或文本表示为固定维度的向量的方法。这些向量能够捕捉词语之间的语义关系，是自然语言处理（NLP）中的一种关键技术。词嵌入将词语映射到一个连续的向量空间中，相似语义的词语在该空间中彼此距离较近。


相关算法：

### One-Hot Encoding
最简单的词表示方法是 One-Hot Encoding，即用一个高维稀疏向量表示词语，向量中只有一个位置为 1，其余为 0

局限性： 这种方法不能捕捉词语之间的语义关系，词向量之间没有语义信息，且维度随词汇量线性增长，计算代价高。

### 哈希表
哈希表算法通过哈希表用哈希函数来确定词块在特征向量的索引位置，可以不创建词典，称为哈希技巧。哈希技巧是无固定状态的，它把任意数据块映射到固定数目的位置，并且保证相同的输入一定产生相同的输出，不同的输入尽可能产生不同的输出。

### Latent Semantic Analysis (LSA)
LSA 是一种基于线性代数的降维技术，通过奇异值分解（SVD）来提取词语和文档之间的语义关系。

局限性： 虽然 LSA 能够发现词汇共现模式，但其方法是基于计数的，不够高效且需要较大的计算资源。

### TF-IDF
TF-IDF文本特征提取算法的主要思想是：如果某个词或短语在一篇文章中出现的频率高，并且在其他文章中很少出现，则认为此词或短语具有很好的类别区分能力，适合用来分类。TF-IDF实际上是TF*IDF，即词频(term frequency)与反文件频率(inverse document frequency)。TF表示词条在文档$d$中出现的频率。IDF的主要思想是：如果包含词条$t$的文档少，也就是$n$越小，IDF越大，则说明词条$t$具有很好的类别区分能力。如果某一类文档$C$中包含词条$t$文档数为$m$，而其他类包含$t$的文档总数为$k$,显然所有包含$t$的文档数$n=m+k$,当$m$大的时候，$n$也大，按照IDF公式得到的IDF值会小，就说明该词条$t$类别区分能力不强。但是实际上如果一个词条在一个类的文档中频繁出现，则说明该词条能狗很好地代表这个类的文本的特征，这样的词条应赋予较高的权重，并选来作为该类文本的特征词以区别于其他类文档。


### Word2Vec

Google 团队的 Tomas Mikolov 等人在 2013 年提出。

Word2Vec方法使用的是distributed representation 的词向量表示方式。distributed representation 最早由[Hinton](https://www.cs.toronto.edu/~hinton/) 在[1986年提出](https://gwern.net/doc/ai/nn/1986-rumelhart-2.pdf)，其基本思想是通过训练将每个词映射成$K$维实数向量（$K$一般为模型中的超参数）,通过词之间的距离(比如余弦相似度、欧式距离等)来判断它们之间的语义相似度。它采用一个三层的神经网络，即输入层-隐藏层-输出层，核心技术是根据词频使用Huffman编码，使得所有词频相似的词隐藏层激活的内容基本一致，出现频率越高的词语激活的隐藏层数目越少，这样有效地降低了计算的复杂度。Word2Vec输出的词向量可用于很多自然语言处理相关的工作，如聚类、分类、找同义词、词性分析等。

模型：包括 Skip-Gram 和 CBOW 两种主要架构。
- Skip-Gram：根据目标词预测上下文词，适用于小数据集且对罕见词效果较好。
- CBOW：根据上下文词预测目标词，适用于大数据集且计算速度更快。

特点： 生成的词向量可以捕捉到语义和语法关系，支持向量运算（如“国王 - 男人 + 女人 = 女王”），在 NLP 任务中表现出色。


https://www.cs.toronto.edu/~hinton/backprop.html
[hinton的一些论文](https://www.cs.toronto.edu/~hinton/papers.html)
https://code.google.com/archive/p/word2vec/
https://arxiv.org/abs/1301.3781
https://arxiv.org/abs/1310.4546
https://www.microsoft.com/en-us/research/publication/linguistic-regularities-in-continuous-space-word-representations/?from=http%3A%2F%2Fresearch.microsoft.com%2Fpubs%2F189726%2Frvecs.pdf



### GloVe (Global Vectors for Word Representation)

斯坦福大学的 Jeffrey Pennington 等人在 2014 年提出。

结合全局统计信息（词共现矩阵）和局部上下文，训练得到词向量。

特点： 通过优化一个基于共现概率的损失函数，能够更好地捕捉词语间的全局语义关系。

### FastText

Facebook 的 AI 研究团队在 2016 年提出。

扩展 Word2Vec，使用字符 n-gram，将词分解为多个子词或字符块，从而能够处理未登录词（OOV）和拼写错误的词。

特点： 对稀有词和复合词有更好的语义捕捉能力。

[官网](https://fasttext.cc/)  
[github](https://github.com/facebookresearch/fastText/)


### ELMo (Embeddings from Language Models)

提出者：AllenNLP 团队在 2018 年提出。

使用双向 LSTM 语言模型生成词向量，能够捕捉到上下文信息，词的向量表示会随着上下文变化而变化。

特点： 对多义词处理效果显著增强。

### BERT (Bidirectional Encoder Representations from Transformers)

Google 在 2018 年提出。

基于 Transformer 的双向编码器，能够捕捉深层次的上下文依赖关系。

特点： 生成的向量能够精确地表示词语在不同上下文中的含义，显著提升了自然语言理解任务的表现。


### 参考文档
[网络博客-白话词嵌入：从计数向量到Word2Vec](https://cloud.tencent.com/developer/article/1508923)




