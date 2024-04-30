# Trojan


[Trojan教程](https://tlanyan.pp.ua/trojan-tutorial/ '')
[Let's encrypt教程](https://tlanyan.pp.ua/use-lets-encrypt-certificate/ '')

## 简介

[官网](https://github.com/trojan-gfw '')

## 安装
### 服务端

1. 给域名安装证书
    1. 首先安装certbot：`yum install -y python3 && pip3 install certbot`（注意：该安装方式不是官方推荐的，但一直都很好使）
       安装完毕后，运行`certbot --help`可以查看该工具的用法。
    1. 获取证书， certbot 默认使用http方式对域名所有权进行验证，该操作需要绑定vps的80端口。如果80端口已被占用，请先停止占用的进程，例如停止Nginx：`systemctl stop nginx`。
       接着运行命令为域名 `www.poul.xyz` 和 `trojan.poul.xyz` 获取证书： `certbot certonly --standalone -d www.poul.xyz -d trojan.poul.xyz`。如果有其他二级域名，继续添加`-d`参数即可。
    1. 大概半分钟就拿到了免费的证书，运行 `certbot certificates` 命令可查看域名证书的路径和国旗时间。
    1. `/usr/local/bin/certbot renew` 命令可以更新证书，可以通过crontab做定时更新

1. 第二种安装证书的方式(推荐) 使用[acme.sh](https://tlanyan.pp.ua/use-acme-sh-get-free-cert/ '')
    ```shell
    curl https://get.acme.sh | sh
    acme.sh --set-default-ca --server letsencrypt
    ~/.acme.sh/acme.sh  --upgrade  --auto-upgrade
    ## 安装nginx 并且配置域名的监听不然下面会执行失败
    ~/.acme.sh/acme.sh --issue -d www.poul.xyz --nginx
    mkdir -p /root/cert/www.poul.xyz
    ~/.acme.sh/acme.sh --install-cert -d www.poul.xyz --key-file /root/cert/www.poul.xyz/key --cert-file /root/cert/www.poul.xyz/cert  --fullchain-file /root/cert/www.poul.xyz/fullchain 
    ```
    结果：
    ```
    [2021年 09月 25日 星期六 15:55:10 UTC] Installing key to: /root/cert/www.poul.xyz/key
    [2021年 09月 25日 星期六 15:55:10 UTC] Installing full chain to: /root/cert/www.poul.xyz/cert
    ```
    
    定时更新证书的方式 现在证书的有效期是两个月 需要定时更新
    ```shell
    /root/.acme.sh/acme.sh --issue -d vultr.poul666.top --nginx
    /root/.acme.sh/acme.sh --install-cert -d github.poul666.top --key-file /root/cert/github.poul666.top/key --fullchain-file /root/cert/github.poul666.top/cert
    systemctl restart trojan
    ## 此脚本已打包到服务器的目录 /root/cert/www.poul.xyz/renew.sh 并配置了crontab 
    ```
1. 登陆服务器后执行下面的命令
```shell
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/trojan-gfw/trojan-quickstart/master/trojan-quickstart.sh)"
```
该命令会下载最新版的trojan并安装。安装完毕后，trojan配置文件路径是 `/usr/local/etc/trojan/config.json`

1. 修改`config.json`配置 根据自己的需求修改配置文件（大部分参数保持默认即可），保存，然后设置开机启动：`systemctl enable trojan`，并启动trojan： `systemctl start trojan`。
   - `local_port` 监听的端口，默认是443，除非端口被墙，不建议改成其他端口；
   - `remote_addr`和`remote_port` 非trojan协议时，将请求转发处理的地址和端口。可以是任意有效的ip/域名和端口号，默认是本机和80端口；
   - `password` 密码。需要几个密码就填几行，最后一行结尾不能有逗号；
   - `cert`和`key` 域名的证书和密钥，Let’s Encrypt申请的证书可用 `certbot certificates` 查看证书路径。注意不是mysql里面的key和cert！
   - `key_password` 默认没有密码（如果证书文件有密码就要填上）；
   - `alpn` 建议填两行：`http/1.1`和`h2`，保持默认也没有问题。

1. 为了让伪装更正常，配置文件中的 `remote_addr` 和 `remote_port` 请认真填写。如果使用默认的 `127.0.0.1` 和 `80`，可以使用nginx代理一个简单的页面
```shell
yum install -y epel-release && yum install -y nginx
systemctl enable nginx
systemctl start nginx
```
 如果更换伪装网站页面只需上传文件到 `/usr/share/nginx/html` 目录即可。

1. 安装加速
   几种选型 BBR，魔改BBR，BBR Plus，锐速(Lotserver)
   [对比博客](https://roov.org/2020/04/bbr-bbrplus-bbr2-2/#toc-2 '')
   [安装博客](https://blog.ylx.me/archives/783.html '')
   安装命令
   ```sehll
    wget -N --no-check-certificate "https://github.000060000.xyz/tcp.sh" && chmod +x tcp.sh && ./tcp.sh
    
   ```

1. 两台机器之间的网络测速工具iperf3
   [博客](https://zhuanlan.zhihu.com/p/137958252 '')
   - 服务端启动 `iperf3 -s`
   - 客户端启动来测速 `iperf3 -c 192.168.2.165` 默认是客户端发送，服务器端接收 也可以反过来，让服务器端发送，客户端接收，那就是后面跟随-R 参数，注意 R 要大写：`iperf3 -c 192.168.2.165 -R`

   

### 客户端

#### mac

1. [安装homebrew](../mac/tools '') 
2. 安装supervisor `brew install supervisor`
3. [github](https://github.com/trojan-gfw/trojan '')上下载安装包
4. 通过supervisor工具 使trojan客户端可以自启动
5. 配置网络自动代理pac路径 `https://blog.poul.top/pacs/gfwlist.pac`


## 备用方案

当自己的服务器连不上，但是需要科学上网的时候，可通过下面的方式应急
1. https://www.58zfdao.com/user
2. https://bywave.art/
新的google账号
stormnumbus@gmail.com
....0827P...