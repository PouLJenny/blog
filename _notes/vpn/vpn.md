# VPN


## openvpn

### 安装server端
https://as-portal.openvpn.com/quick-start-guide
https://as-portal.openvpn.com/get-access-server/centos

```log
Initial Configuration Complete!

You can now continue configuring OpenVPN Access Server by
directing your Web browser to this URL:

https://193.9.44.122:943/admin

During normal operation, OpenVPN AS can be accessed via these URLs:
Admin  UI: https://193.9.44.122:943/admin
Client UI: https://193.9.44.122:943/
To login please use the "openvpn" account with "WoodpwsV60lE" password.

See the Release Notes for this release at:
   https://openvpn.net/vpn-server-resources/release-notes/
```

### 安装client
直接访问上面的url即可


### 配置固定ip
配置客户端的固定ip
https://openvpn.net/vpn-server-resources/assigning-a-static-vpn-client-ip-address-to-a-user/

### 网络问题

`ip route show`发现路由转发表有些问题
`traceroute www.baidu.com` 所跳的路由器也不太对
`sudo ip route del 0.0.0.0/1`


## wireguard

[官网](https://www.wireguard.com/)


安装
```shell
sudo apt update
sudo apt install wireguard

## 声称服务端密钥对
wg genkey | tee server_private.key | wg pubkey > server_public.key


## 添加客户端配置
wg genkey | tee client_private.key | wg pubkey > client_public.key
```

配置文件 `/etc/wireguard/wg0.conf`
```conf
[Interface]
# 服务端的私钥
PrivateKey = <服务端的私钥>
# WireGuard VPN 服务端的监听端口
ListenPort = 51820
# VPN 网段配置，例如使用 10.0.0.1/24
Address = 10.110.110.1/32
# 打开 IP 转发
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE


[Peer]
# 客户端的公钥
PublicKey = <客户端公钥>
# 客户端的 VPN 内网 IP 地址
AllowedIPs = 10.110.110.2/32
```


客户端配置文件`wg0-client.conf`
```config
[Interface]
# 客户端的私钥
PrivateKey = 2Duu6Hxa0u29TfU2Br26SMM+l7hKM5pkldNCUDiPVVc=
# 客户端的 VPN 内网 IP 地址
Address = 10.110.110.2/32
# DNS 配置（可选）
DNS = 1.1.1.1

[Peer]
# 服务端的公钥
PublicKey = jcjc7Dy57j2j06kQn/ulXrUNSxKMUrk04m5ECQ47vn8=
# 服务端的 IP 和端口
Endpoint = 117.50.220.144:51820
# 允许通过 VPN 的网段
AllowedIPs = 0.0.0.0/0
```

