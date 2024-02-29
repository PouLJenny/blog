# 安装DNS服务端


## DNSmasq
https://cloud.tencent.com/developer/article/1174717

配置文件： `/etc/dnsmasq.conf`


## 碰到的问题

### 无法解析DNS
```shell
tecmint@ubuntu:~$ ping google.com
ping: tecmint.com: Temporary failure in name resolution
```

解决方式:
```shell
$ sudo systemctl restart systemd-resolved.service
```