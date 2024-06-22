# Nginx

[商业官网](https://www.nginx.com/ )
[商业文档](https://docs.nginx.com/ )
[开源官网](https://nginx.org/)
[开源文档](https://nginx.org/en/docs/ )

## 介绍


## linux nginx的安装
    
1.  安装nginx必须的依赖包 
    ```shell
    [root@rhel6u3-7 ~]# yum -y install gcc gcc-c++ openssl-devel pcre-devel zlib-devel libxslt-devel geoip-devel gperftools-devel //yum创建过程略，安装略 
    ```
2.  安装编译nginx，目前系统测试环境为rhel6.3  软件版本为nginx-1.27
    ```shell
    [root@rhel6u3-7 ~]# useradd -s /sbin/nologin -M nginx //给nginx服务器创建后台进程管理用户 
    [root@rhel6u3-7 ~]# tar zxvf nginx-1.2.7.tar.gz  //解压缩 
    [root@rhel6u3-7 ~]# cd nginx-1.2.7  
    [root@rhel6u3-7 nginx-1.2.7]# ./configure --user=nginx --group=nginx --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_gzip_static_module --with-http_realip_module --with-http_sub_module --with-http_ssl_module  --with-stream
    // --user=nginx –group=nginx 设置允许nginx允许的用户和组为nginx 
    // --prefix=/usr/local/nginx/  设置nginx安装路径 
    // --with-http_stub_status_module 安装允许状态模块 
    // --with-http_ssl_module 安装ssl模块 
    //更多参数请参看 ./configure --help 
    ```
3.  `[root@rhel6u3-7 nginx-1.2.7]# make & make install`   //编译安装过程略 
4.  `[root@rhel6u3-7 ~]# /usr/local/nginx/sbin/nginx  –V`  //安装完成后查看Nginx的相关环境配置信息是否正确        
5.  [root@rhel6u3-7 ~]# `/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf`   // -c指向nginx主配置文件 
6.  启动nginx  `./nginx  `
    这个步骤出现了 [emerg]: getpwnam(“nginx”) failed 异常  解决方法：  没有安装nginx用户导致的无法启动 
    `[root@localhost nginx-1.11.2]# useradd -s /sbin/nologin -M nginx`
    

http://blog.51cto.com/dreamfire/1140965         
https://www.cnblogs.com/hanyinglong/p/5102141.html


## 限流作用


## 跨域配置

## 配置误区
https://www.nginx.com/blog/avoiding-top-10-nginx-configuration-mistakes/


### Mistake 3: Not Enabling Keepalive Connections to Upstream Servers


## Nginx 动态更新upstream
https://zhuanlan.zhihu.com/p/326612058
https://blog.51cto.com/qiangsh/2021399
https://zhuanlan.zhihu.com/p/260663451
http://nginx.org/en/docs/http/ngx_http_upstream_module.html
http://nginx.org/en/docs/http/ngx_http_upstream_conf_module.html
http://nginx.org/en/docs/http/ngx_http_api_module.html#compatibility

https://github.com/cubicdaiya/ngx_dynamic_upstream


## Ngxin 平滑升级
https://zhuanlan.zhihu.com/p/193078620
https://www.digitalocean.com/community/tutorials/how-to-upgrade-nginx-in-place-without-dropping-client-connections

原理，基于nginx对一些信号的处理
- **USR2**: This spawns a new set of master/worker processes without affecting the old set.
- **WINCH**: This tells the Nginx master process to gracefully stop its associated worker instances.
- **HUP**: This tells an Nginx master process to re-read its configuration files and replace worker processes with those adhering to the new configuration. If an old and new master are running, sending this to the old master will spawn workers using their original configuration.
- **QUIT**: This shuts down a master and its workers gracefully.
- **TERM**: This initiates a fast shutdown of the master and its workers.
- **KILL**: This immediately kills a master and its workers without any cleanup.

大体步骤
1. 生成新的nginx master/work进程组
```shell
kill -s USR2 masterpid

```
老的nginx进程会写到 `/usr/local/nginx/logs/nginx.pid.oldbin`中

1. 检查新的nginx进程是否有问题

1. 关闭老的nginx master/worker进程组
```shell
kill -s WINCH `cat /usr/local/nginx/logs/nginx.pid.oldbin`
```

1. nginx平滑升级完毕


## 日志级别

- debug, 
- info, 
- notice, 
- warn, 
- error,
- crit,
- alert, 
- emerg.


## nginx日志乱码如何解析

使用python脚本  
```python
s = "\x22\xE8\x91\xA1\xE8\x90\x84\xE9\x85\x92\x22"
decoded_s = s.encode('latin-1').decode('utf-8')
print(decoded_s)
```