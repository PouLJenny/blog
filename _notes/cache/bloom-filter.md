# 布隆过滤器

![](/assets/notes/cache/bloom-filter-01.jpeg)

1. 如果不在布隆过滤器里面，就一定不在数据库中
2. 如果在布隆过滤器中，由于存在hash冲突，则不一定在数据库中
3. 所以布隆过滤器不存在的值只是实际不存在值的子集


![](/assets/notes/cache/bloom-filter-02.jpeg)


布隆过滤器本身因为长度固定限制，刚开始数据量少的情况下，hash冲突不明显，效果比较好，等数据越来越多，hash冲突越来越多，效果就会下降。图中黄色的区域就会越来越小，红色区域就会越来越大，而红色区域是会直接访问数据库的。