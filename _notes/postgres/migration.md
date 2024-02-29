# 数据迁移

## PG自带的方式

### 相同版本 从一个db的scheme迁移到不同的db的不同scheme
```shell
# dump文件
pg_dump -h 192.168.17.242 -p 5432 -d boss_crm -U boss_crm -n boss_crm -O -t customer_trend_see  > customer_trend_see.sql
pg_dump -h 192.168.17.242 -p 5432 -d boss_crm -U boss_crm -n boss_crm -O -t customer_trend_competitor -t customer_trend_detail -t customer_trend_feedback -t customer_trend_item -t customer_trend_like -t customer_trend_valuable  > customer_trend_other.sql

# 替换scheme
sed 's/boss_crm\./boss_crm_business\./g' customer_trend_see.sql | sed 's/boss_crm;/boss_crm_business;/g' > customer_trend_see_bs.sql


# 恢复文件
psql -h 192.168.17.242 -p 5432 -d boss_crm_business -U boss_crm_business  -f customer_trend_see_bs.sql
psql -h 192.168.17.242 -p 5432 -d boss_crm_business -U boss_crm_business  -f customer_trend_other_bs.sql
```


## pgloader
[官网](https://pgloader.io/ )