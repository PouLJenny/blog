---
layout: post
title:  "Nginx网站添加访问校验"
date:   2019-07-18 20:07:07 +0800
categories: nginx
tags: nginx
permalink: /nginx/auth
published: true
publish_file: 2019-07-18-nginx-auth.md
toc: true
---
# Nginx网站添加访问校验

## 背景

自己的网站需要做一个简单的访问权限校验，于是就想到了nginx可以做这个事儿。
随后就去网上搜了一下教程，结果没有几个说的比较全面的而且照做下来也没有成功，因此在这里做个记录，方便有需要的人能看到

## 过程
首先讲一下nginx的版本: 1.14.0  (如果版本不一样不保证我的教程是正确的）。
nginx使用的是`ngx_http_auth_basic_module`模块，此模块不需要安装直接可以使用。


## 使用httpasswd生成密码
如果没有这个命令的话centos的安装命令是 `yum -y install httpd-tools`

生成带用户名和密码的文件

```shell
htpasswd -c /usr/local/nginx/passwd/access  nginx # 最后一个参数是用户名，可自定义
下面根据提示输入密码
```

## 配置nginx

```
server {
   listen 80;
   server_name  -;
  
   location / {
    .......
 	
   	auth_basic "closed site";  
   	auth_basic_user_file /usr/local/nginx/passwd/access; 
   	 .......
   }
  
}
```
参数讲解
auth_basic : 默认值是false，如果不修改的话是不生效的
auth_basic_user_file: 验证的帐号密码，这个填的是用htpasswd生成的文件路径

保存之后

```shell
nginx -t  # 查看配置修改是否正确
nginx -s reload # 重启nginx
```

下面贴一下nginx官网的模块介绍
http://nginx.org/en/docs/http/ngx_http_auth_basic_module.html


至此 配置完毕!
