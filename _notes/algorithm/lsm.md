# LSM-tree

## 历史

LSM tree（Log-Structured Merge tree）是由Jeffrey Dean和Sanjay Ghemawat在1996年发明的。
他们的工作被总结在论文《LevelDB: A Fast and Lightweight Key-Value Store》，这篇论文于2011年由Google发布。
在这个论文中，作者描述了LevelDB的设计和实现，LevelDB是使用LSM tree作为其存储引擎的键-值存储系统。值得注意的是，虽然LSM tree的概念在1996年提出，但它在后来的几年中得到了进一步的改进和应用，成为许多大规模分布式存储系统的基础，如Bigtable和Cassandra。