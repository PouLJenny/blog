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