# Hash




## Hash分桶，Redis如何解决扩容带来的rehash问题



### 普通的hash分桶的缺点

假设有4个Redis节点，通过hash(key) % 4 来选择存储节点：

```txt
Redis 节点： R0,R1,R2,R3
映射逻辑： 位置 = hash(key) % 4
```

如果再加一个节点： R4
位置 = hash(key) % 5 
这样几乎所有的key都要做数据迁移，性能波动非常大




### 一致性hash/ consistent hashing


[wiki](https://en.wikipedia.org/wiki/Consistent_hashing)





#### python代码示例

```python
import hashlib
import bisect
import random


def hash_fn(key):
    """使用 MD5 哈希函数并取前 8 位作为哈希值"""
    return int(hashlib.md5(key.encode('utf-8')).hexdigest()[0:8], 16)


class ConsistentHashRing:
    def __init__(self, virtual_nodes=100):
        self.virtual_nodes = virtual_nodes
        self.ring = dict()             # 哈希值 -> 虚拟节点名
        self.sorted_keys = []          # 排序后的哈希值列表
        self.nodes_map = dict()        # 虚拟节点名 -> 真实节点名

    def add_node(self, real_node):
        """添加真实节点及其虚拟节点"""
        for i in range(self.virtual_nodes):
            virtual_node = f"{real_node}#{i}"
            h = hash_fn(virtual_node)
            self.ring[h] = virtual_node
            self.nodes_map[virtual_node] = real_node
            bisect.insort(self.sorted_keys, h)

    def remove_node(self, real_node):
        """移除真实节点及其虚拟节点"""
        for i in range(self.virtual_nodes):
            virtual_node = f"{real_node}#{i}"
            h = hash_fn(virtual_node)
            self.ring.pop(h, None)
            self.nodes_map.pop(virtual_node, None)
            index = bisect.bisect_left(self.sorted_keys, h)
            if index < len(self.sorted_keys) and self.sorted_keys[index] == h:
                self.sorted_keys.pop(index)

    def get_node(self, key):
        """根据 key 找到其映射的真实节点"""
        h = hash_fn(key)
        ## 在有序列表中返回第一个 大于 h 的元素索引（即“顺时针方向的第一个虚拟节点”）
        idx = bisect.bisect(self.sorted_keys, h)
        if idx == len(self.sorted_keys):
            idx = 0  # 环状结构，回到起点
        virtual_node = self.ring[self.sorted_keys[idx]]
        return self.nodes_map[virtual_node]


# -------------------------------
# 使用示例
ring = ConsistentHashRing(virtual_nodes=100)

# 添加真实节点
ring.add_node("NodeA")
ring.add_node("NodeB")
ring.add_node("NodeC")

# 映射一些键
keys = [f"user_{i}" for i in range(20)]
key_map_before = {k: ring.get_node(k) for k in keys}

print("初始映射:")
for k, v in key_map_before.items():
    print(f"{k} → {v}")

# 添加一个新节点
print("\n添加 NodeD 后的数据迁移:")
ring.add_node("NodeD")
key_map_after = {k: ring.get_node(k) for k in keys}

moved = 0
for k in keys:
    before = key_map_before[k]
    after = key_map_after[k]
    change = "✓ Moved" if before != after else "  "
    if before != after:
        moved += 1
    print(f"{k}: {before} → {after} {change}")

print(f"\n总共迁移了 {moved} 个键，占比 {moved / len(keys) * 100:.2f}%")
```


## 相关文献

- [Consistent Hashing and Random Trees:
Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web](https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash.pdf) 麻省理工学院的 David Karger 等人在 1997 年发表了一篇里程碑式的论文
- [Dynamo: Amazon’s Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) 提出了副本、冲突解决与 Gossip 协议，基于一致性哈希构建高可用系统
- [Cassandra - A Decentralized Structured Storage System](https://www.cs.cornell.edu/projects/ladis2009/papers/lakshman-ladis2009.pdf) 在 Dynamo 基础上优化了数据模型和读写路径，依然使用一致性哈希