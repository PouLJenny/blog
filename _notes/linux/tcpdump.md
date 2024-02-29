# tcpdump 命令

## 使用 wireshark 查看 tcpdump 的抓包结果

在服务器上执行命令
```shell
sudo tcpdump -i eth0 host 192.168.0.100 -w dump.pcap -vv
```
等到自己抓的数据差不多了就，`CTR+C`停止进程

用wireshark打开文件`dump.pcap`