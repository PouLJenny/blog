# Google服务


## 红米note8 pro升级到miui12后无法安装google套件的问题

谷歌三件套分别指的是： 
谷歌服务框架apk（Google Services Framework） 谷歌play 
服务apk（Google play Services） 
谷歌play 的apk（Google Play Store）


### 方案1 
因andorid11后 所有使用谷歌gms服务的应用需要在特定XML声明对应gms的权限，而老版本的playstore没声明，导致权限受限无法启动（手机链接ADB后，点击登录后 会在控制台log里提示对应权限缺失）

安装给定版本的 service和 store（谷歌框架apk我没找到 使用 Hi谷歌安装器安装的）：
google play services v20.50.16（080406） 注意后面的小版本号 
google play store v22.5.28-16[0] 不用担心这个不是最新版，登录后会自动更新到最新版（建议下我给定版本）

## Google play 在国内无法安装商店内应用的问题

https://www.yetpage.com/archives/278


跟本原因就是
```yaml
  - DOMAIN-SUFFIX,googleapis.cn,GOOGLE_PLAY
  - DOMAIN-SUFFIX,xn--ngstr-lra8j.com,GOOGLE_PLAY
```
上面中的两个域名，需要代理到国外节点，而且这个节点的ip不能让google识别成中国的ip。


## IP被Google标记为中国的怎么处理
https://vps.dance/google-ip-location.html
https://www.74110.net/tutorial/linux/google-ip-location-2/
https://support.google.com/websearch/workflow/9308722 发起google申请


## 禁止浏览器重定向google地址

直接访问
`https://www.google.com/ncr`