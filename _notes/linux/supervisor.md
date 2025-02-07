# Supervisor


[官方文档](http://supervisord.org/index.html )


## 安装
https://blog.csdn.net/sl1992/article/details/106165171

### AlmaLinux安装

1. Install EPEL repo
```shell
yum install epel-release
```

2.  Install supervisor
```shell
yum -y install supervisor
```

## `program:x`配置文件

- `command`
    程序的启动命令，这个命令执行的时候必须是前台启动，方便supervisor来管理。这个需要注意： 如果启动命令是一个`sh`脚本的话，需要在脚本中最终执行`exec`命令来替换掉当前的进程，否则，supervisor管理的是sh脚本的进程，而不是最终我们想要的进程
- `autostart`
    If true, this program will start automatically when supervisord is started
- 


## 需要修改的配置

1. 修改最小的句柄数，默认是1024，对一些通用的服务来说太小了，比如nginx
```conf
[supervisord]
minfds=65535                 ; min. avail startup file descriptors; default 1024
```

2. 修改`/tmp/` 目录下的配置文件，为`/var/tmp`，防止操作系统自动清理，导致应用程序不正常

```conf
[unix_http_server]
file=/var/tmp/supervisor.sock

[supervisord]
logfile=/var/tmp/supervisord.log
pidfile=/var/tmp/supervisord.pid

[supervisorctl]
serverurl=unix:///var/tmp/supervisor.sock
```
