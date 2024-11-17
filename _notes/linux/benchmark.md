# Linux中的基准测试工具

## 常见的基准测试工具

- [GreekBench](https://www.geekbench.com/download/linux/)
- sysbench

## CPU压测工具

### stress

```shell
sudo pacman -S stress
stress --cpu 4 --timeout 60s
```

### stress-ng

```shell
sudo pacman -S stress-ng
stress-ng --gpu 2 --timeout 60s --log-file stress_ng_result.log
stress-ng --cpu 2 --timeout 60s
```

## FIO
主要用来测试硬盘io性能

https://github.com/axboe/fio

https://bbs.huaweicloud.com/forum/thread-90290-1-1.html#