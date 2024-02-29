# 邮件服务器搭建


[知乎博客](https://zhuanlan.zhihu.com/p/638569694)

## 开源组件选型
[博客1](https://itsfoss.com/open-source-email-servers/ )

### IRedMail

https://www.iredmail.org/
中国人开发的

### Mailcow
https://mailcow.email/
docker部署的

### Mail-in-a-Box
https://mailinabox.email/
[github](https://github.com/mail-in-a-box/mailinabox)
语言： python

### Sogo.nu
https://www.sogo.nu/
[github](https://github.com/Alinto/sogo)
语言： Objective-C

### Modoboa
https://modoboa.org/en/
[github](https://github.com/modoboa/modoboa)
语言： python


### Postal

它专为出站邮件而设计，没有邮箱管理功能。

[github](https://github.com/postalserver/postal) 13.5k stars
语言： ruby


### Cuttlefish
https://cuttlefish.io/
[github](https://github.com/mlandauer/cuttlefish ) 1.4k stars
语言： ruby


### Apache James
https://james.apache.org/

[github](https://github.com/apache/james-project/)
语言： java

### Haraka
https://haraka.github.io/

[github](https://github.com/haraka/Haraka) 4.7k stars

### Postfix
### Maddy
### Dovecot
### Poste

### Mailu
https://mailu.io/
是一个基于 Docker 的邮件服务器


## 企业邮箱服务商

### 国外

- gmail
- outlook
- zoho
- yandex
- goDaddy
- hostinger
- namecheap
- aws

### 国内

- 腾讯
- 网易
- 阿里
- 新浪
- 搜狐
- 

### aws企业邮箱部署
亚马逊有两个服务,[官方文档](https://aws.amazon.com/cn/blogs/china/quickly-configure-enterprise-e-mail-with-amazon-workmail/)
1. SES 邮件发送和接收服务
1. Work Mail 企业邮箱服务


## 问题

1. 现在的云服务器厂商为了避免用户拿来大量发垃圾邮件都禁止了25端口的出向流量，国内外知名点的云服务商都这样。我现在也是用的博主说的green cloud，目前感觉性价比不算高，国内访问起来也很慢，但也没找到更好的替代厂商
1. 


