# CPU火焰图


## History

火焰图由Brendan Gregg发明，他是一位著名的性能专家。Brendan Gregg在他的著作[《Systems Performance: Enterprise and the Cloud》]()和《BPF Performance Tools》中详细介绍了火焰图的使用。火焰图最初被用作一种可视化性能问题的工具，可以直观地展示CPU使用情况、内存分配等。由于其直观性和实用性，火焰图被广泛应用于性能分析和调优领域。

[Brendan Gregg官网](https://www.brendangregg.com/)
[Brendan Gregg FlameGraph github](https://github.com/BrendanGregg/FlameGraph)

## 使用方式

1. 安装perf工具
```shell
yum -y install perf
```

2. 采集cpu指标
```shell
perf record -F 99 -a -g -- sleep 10
perf script > out.perf
```

也可以采集某个进程的  
```shell
perf record -F 99 -p <pid> -g -- sleep 60
## 其中的pid为进程id
perf script > out.perf
```

3. 下载`FlameGraph`工具
```shell
git clone https://github.com/brendangregg/FlameGraph.git
```

4. 生成火焰图
```shell
./FlameGraph/stackcollapse-perf.pl out.perf > out.folded
./FlameGraph/flamegraph.pl out.folded > cpu_flamegraph.svg
## centos 运行上面的代码可能会出现错误 Can't locate open.pm in @INC，运行下面的命令即可解决
yum install perl-open.noarch
```
