# Privoxy

https://www.privoxy.org/

Privoxy是一个 HTTP 协议过滤代理。Privoxy 是有着先进的过滤能力和保护隐私的代理工具，它可以过滤网页内容，管理cookies，控制访问，除广告、横幅、弹出窗口等等，它同时支持单系统和多用户网络。
如你看到这个简介一样，有意思的是它既能屏蔽广告,也可以弹出广告，所以，任何事物都有两面性。

除了上述功能外， privoxy很多时候结合其他的隧道工具使用，达到一些保护隐私的作用，本文简单介绍PAC。

## 安装

archlinux:
```shell
sudo pacman -S privoxy
```

centos:
```shell
sudo yum -y install privoxy
```

## 管理
```shell
sudo systemctl status privoxy # 查看运行状态
sudo systemctl restart privoxy # 重启停止
sudo systemctl stop privoxy # 重启停止
sudo systemctl start privoxy # 重启停止
```

## 配置
编辑配置文件`/etc/privoxy/config` 注释掉下面的配置
```config
actionsfile match-all.action # Actions that are applied to all sites and maybe overruled later on.
actionsfile default.action   # Main actions file
actionsfile user.action      # User customizations

## 改成
#actionsfile match-all.action # Actions that are applied to all sites and maybe overruled later on.
#actionsfile default.action   # Main actions file
#actionsfile user.action      # User customizations
```
添加新配置
```config
actionsfile gfwlist.action
```

`gfwlst.action`文件内容如下
```config
{+forward-override{forward-socks5 127.0.0.1:1080 .}}
.chinaaffairs.org
.hizb-ut-tahrir.info
.gaymap.cc
.twtkr.com
.freedomhouse.org
....
下面配置需要走代理的域名地址即可,贼方便
```

最好配置一下链接数，默认的128有点少
```config
# 最大客户端连接数（默认是 128）
max-client-connections 1024
```

`/etc/profile`文件如下配置
```config
## 代理
proxy="http://127.0.0.1:8118"
export https_proxy=$proxy
export http_proxy=$proxy
export ftp_proxy=$proxy
```

## 重启
配置完了之后重启一下`privoxy`
```shell
sudo systemctl restart privoxy # 重启

source /etc/profile
```