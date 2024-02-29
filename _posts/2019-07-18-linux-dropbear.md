---
layout: post
title:  "Dropbear搭建轻量级的ssh服务"
date:   2019-07-18 10:00:00 +0800
categories: linux dropbear
tags: linux dropbear
permalink: /linux/dropbear
published: true
publish_file: 2019-07-18-linux-dropbear.md
toc: true
---
# Dropbear搭建轻量级的ssh服务

## 背景

最近在学习hadoop，然后想在自己的Manjaro上安装一下，安装前发现执行`ssh localhost` 命令时提示 `ssh: connect to host localhost port 22: Connection refused`。
这是因为自己的电脑没有启动ssh的server端。

## 安装
dropbear是个非常轻量级的ssh server端和client端
[Dropbear官网](https://matt.ucc.asn.au/dropbear/dropbear.html)
下载文件: dropbear-2019.78.tar.bz2  文件不大，不到3M

由于我的Manjaro自带的包管理器，可以直接安装
![](/assets/notes/linux/dropbear-01.png)
## 启动
安装完了之后就直接使用命令启动server端
`dropbear -p 22`
刚开始确怎么也启动不起来，而且终端也没有日志。
随后通过linux的`journalctl -ex`命令来查看系统级的日志
![](/assets/notes/linux/dropbear-02.png)
发现没有找到key，然后使用命令

```shell
dropbearkey -t rsa -f dropbear_rsa_host_key
dropbearkey -t ecdsa -f dropbear_ecdsa_host_key
```
两个文件生成之后，放到上图中dropbear寻找的目录下

```shell
cp dropbear_rsa_host_key /etc/dropbear
cp dropbear_ecdsa_host_key /etc/dropbear
```

最后启动

```shell
dropbear -p 22
```
看到了系统日志打印

```shell
7月 18 17:18:49 poul-pc dropbear[10381]: Running in background
```
这样应该是启动成功了
最后一步确认

```shell
[poul@poul-pc .ssh]$ ssh localhost
The authenticity of host 'localhost (::1)' can't be established.
ECDSA key fingerprint is SHA256:yR7k3XqUXi4ll3TwBewgMytvFjRpkvf3nXKbu+plX+g.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
[poul@poul-pc ~]$ 
[poul@poul-pc ~]$ 
[poul@poul-pc ~]$ exit
注销
Connection to localhost closed.

```

最终ssh连接成功!
