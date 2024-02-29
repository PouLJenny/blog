# 小知识

## PG 加字段 not null default 特别快

pg 11 版本之后加的这个特性

```
Many other useful performance improvements, 
including making ALTER TABLE .. ADD COLUMN
with a non-null column default faster
```
讲的很好的一个博客
https://brandur.org/postgres-default

相关源码 
https://github.com/postgres/postgres/commit/16828d5c0273b4fe5f10f42588005f16b415b2d8



