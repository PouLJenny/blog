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


安装配置
```shell
# ubuntu
sudo apt update
sudo apt install wireguard

# manjaro
sudo pacman -s wireguard-tools

# macos
brew update
brew install wireguard-tools

## 生成密钥对
wg genkey | tee private.key | wg pubkey > public.key
```

### 服务端

配置文件 `/etc/wireguard/wg0.conf`
```conf
[Interface]
# 服务端私钥
PrivateKey = gO0NaG+3YxHvkFS7lKn8Bs9md4XL50632xAhhZuH/mg=
# 服务端ip
Address = 10.0.1.1/24
# 服务端监听的端口号，因为走的是udp的协议，所以telnet是不通的！
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -o wg0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o wg0 -j MASQUERADE

[Peer]
# Host home
# 客户端公钥
PublicKey = 8PvlyrlZoHWL+DuJ/sRbl/UKwVVtlcCusCTCfRX0Sjg=
# 客户端ip
AllowedIPs = 10.0.1.2/32
PersistentKeepalive = 25

[Peer]
# Host work
# 客户端公钥
PublicKey = /0NYJkAMm1Zgbe/+Bi2ggZDYL7vt0d/1wg3U0WZgZmI=
# 客户端ip
AllowedIPs = 10.0.1.3/32
PersistentKeepalive = 25
```

```shell
# 启动
wg up wg0
# 配置开机自动启动
systemctl enable wg-quick@wg0
# 更新配置文件后重启
wg down wg0
wg up wg0
```

服务端需要添加配置
```shell
sysctl net.ipv4.ip_forward
# 期望返回的值应该是： net.ipv4.ip_forward = 1
echo 1 > /proc/sys/net/ipv4/ip_forward
```
持久化到 `/etc/sysctl.conf`
```ini
net.ipv4.ip_forward = 1
```


### 客户端
客户端配置文件`/etc/wireguard/wg0.conf`
```conf
[Interface]
# 客户端私钥
PrivateKey = SGsItP+Bbg3h+BEzKaOtbDKPt0dDjqusPQbiQQGJqUk=
Address = 10.0.1.2/24
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o enp2s0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o enp2s0  -j MASQUERADE

[Peer]
# 服务端公钥
PublicKey = PKNMzruckKZukzaICKh/LP1/WguK+z0Wc41PnVO57GE=
AllowedIPs = 10.0.1.0/24
# 服务端ip端口号，
Endpoint = 117.50.220.144:51820
PersistentKeepalive = 25
```

macos的客户端配置文件在`/opt/homebrew/etc/wireguard/wg0.conf`
```conf
[Interface]
PrivateKey = IPV2DATaTiaBQ/0YQ4nZkZX/fDVrj7eFOUix43vrVkQ=
Address = 10.0.1.5/24


[Peer]
PublicKey = PKNMzruckKZukzaICKh/LP1/WguK+z0Wc41PnVO57GE=
AllowedIPs = 10.0.1.0/24
Endpoint = 117.50.220.144:51820
PersistentKeepalive = 25
```


## tailscale

[官网](https://tailscale.com/)

安装脚本
`curl -fsSL https://tailscale.com/install.sh | sh`

https://login.tailscale.com/admin/machines

查看当前在线的


卸载：

```shell
sudo systemctl stop tailscaled
sudo systemctl disable tailscaled
sudo dnf remove -y tailscale

sudo rm -rf /etc/tailscale
sudo rm -rf /var/lib/tailscale
sudo rm -rf /usr/local/bin/tailscale
sudo rm -rf /var/lib/systemd/system/tailscaled.service
```

# EOF