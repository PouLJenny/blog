# Reids安装

## Linux

### 源码安装

1.  从官网下载的压缩文件解压
2.  进入压缩文件的根目录执行make方法
    如果 失败 
    2.1. 安装  `yum install gcc-c++`
    2.2. 编译选择参数  `make MALLOC=libc`
    make时报如下错误：
    ```shell
    zmalloc.h:50:31: error: jemalloc/jemalloc.h: No such file or directory
    zmalloc.h:55:2: error: #error "Newer version of jemalloc required"
    make[1]: *** [adlist.o] Error 1
    make[1]: Leaving directory `/data0/src/redis-2.6.2/src'
    make: *** [all] Error 2
    ```
    原因是jemalloc重载了Linux下的ANSI C的malloc和free函数。解决办法：make时添加参数。

    `make MALLOC=libc`
        
    ```shell
    zmalloc.h:50:31： error： jemalloc/jemalloc.h： No such file or directory
    zmalloc.h:55:2： error： #error “Newer version of jemalloc required”
    　　make［1］： *** ［adlist.o］ Error 1
    　　make［1］： Leaving directory `/data0/src/redis-2.6.2/src‘
    　　make： *** ［all］ Error 2
    ```

　　解决办法是：
    进入源码包目录下的deps目录中执行
　　`make hiredis jemalloc linenoise lua`
3. 编译成功后  安装到指定目录 `make PREFIX=/usr/local/redis install`
   3.1 再安装之前最好执行一下`make test`
   出现`You need tcl 8.5 or newer in order to run the Redis test`
   去http://www.linuxfromscratch.org/blfs/view/cvs/general/tcl.html网站查看最新的tcl版本
   执行 :
       ```shell
       wget https://downloads.sourceforge.net/tcl/tcl8.6.8-src.tar.gz
       cd  /usr/local/tcl8.6.8/unix/
       ./configure --prefix=/usr/local/tcl8.6.8
       make
       make install
       ```
       
上述操作还是出现了，安装完成后，`make test`的时候不识别最新的tcl命令不知道为啥。。
`yum install tcl`
       
结果测试没通过，解决方法：https://blog.csdn.net/steven_liwen/article/details/51261567
4. 把redis.conf cp 到安装根目录
5. 修改redis.conf 为 bind 0.0.0.0 (运行别的ip的机器远程访问)   daemonize yes (按照后台运行方式启动redis)
6. bin目录下 使用`redis-server ../redis.conf `命令启动redis
7. 在bin目录下边使用redis-cli 命令进入命令模式

接下来是配置开机启动及将期添加至systemctl下进行管理
```
//增加redis用户组
[root@localhost /]# groupadd redis
[root@localhost /]# useradd -c "Redis Server" -s /sbin/nologin -d /var/lib/redis -g redis -G root redis
```

参数解释： 
-c 用户描述信息 
-s 用户执行脚本，此处为安全考虑，redis用户是不允许远程登录，故使用/sbin/nologin 
-d 用户home目录，此处无需在/home目录下创建redis子目录，故将其定位于/var/lib/redis空目录中 
-G 扩展用户组，即表示此用户同时属于root用户组

增加服务
进入`/usr/lib/systemd/system`目录，增加`redis.service`文件，并添加如下内容
```
[Unit]
#描述信息
Description=Redis Server 3.0.4
#启动时机,开机启动最好在网络服务启动后即启动
After=network.target
[Service]
#此处为命令行启动redis的命令及参数,可参考官方文档
ExecStart=/usr/local/bin/redis-server /etc/redis.conf --daemonize no  
#停止redis服务器命令
ExecStop=/usr/local/bin/redis-cli -h 127.0.0.1 -p 6379 shutdown 
User=redis #运行reddis用户
Group=redis #所属组
[Install]
WantedBy=multi-user.target #字符界面下启动
```
测试服务

```shell   
[root@localhost /] systemctl status redis.service   
redis.service - Redis Server 3.0.4   
Loaded: loaded (/usr/lib/systemd/system/redis.service; enabled)   
Active: active (running) since 一 2015-09-14 16:06:35 CST; 53min ago   
Main PID: 17604 (redis-server)   CGroup: /system.slice/redis.service           
└─17604 /usr/local/bin/redis-server *:6379    
9月 14 16:06:35 localhost.localdomain systemd[1]: Started Redis Server 3.0.4.
#停止服务后查看端口或进行状态
[root@localhost /] systemctl stop redis.service 
[root@localhost /] netstat -ntlp #如果没有6379商品则表示已成功关闭
```

### yum安装

1. `yum install redis`
2.  启动redis `service redis start`
    停止redis `service redis stop`
    查看redis运行状态 `service redis status`
    查看redis进程 `ps -ef | grep redis`
3. `chkconfig redis on `或者 `systemctl enable redis`
4. `vi /etc/redis.conf` 修改redis默认配置


异常问题解决方式：
redis默认安装会有很多问题，下面的文章讲解了怎么在生产中配置redis
https://www.techandme.se/performance-tips-for-redis-cache-server/