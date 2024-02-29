# 安装rabbitmq

## docker安装

1. 下载docker桌面版
    https://www.docker.com/get-started
    安装并启动docker桌面版

2. 命令行终端内操作
    安装rabbitmq
    `docker pull rabbitmq:3.7.12-management`
    `docker run -it -d --name boss-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3.7.12-management`

    安装延迟队列插件
    [插件官网]('https://www.rabbitmq.com/community-plugins.html' '')
    [插件GitHub]('https://github.com/rabbitmq/rabbitmq-delayed-message-exchange/releases' '')

    `docker cp rabbitmq_delayed_message_exchange-3.8.0.ez boss-rabbit:/plugins`

    执行进入容器的命令：
    `docker exec -it boss-rabbit /bin/bash`

    容器内执行下面的命令

    1. `cd /plugins`
    2. `chown rabbitmq:rabbitmq rabbitmq_delayed_message_exchange-3.8.0.ez`
    3. `cd /usr/bin`
    4. `rabbitmqctl add_user work 123456`
    5. `rabbitmqctl  set_permissions -p "/" work '.*' '.*' '.*'`
    6. `rabbitmqctl set_user_tags work administrator`
    7. `rabbitmq-plugins enable rabbitmq_delayed_message_exchange`
    8. `exit`
    
    退出容器后执行命令
    `docker restart boss-rabbit`

3. 本地浏览器输入 http://127.0.0.1:15672 输入账号密码 work 123456 进入rabbitmq管理页面



## linux下安装rabbitMQ

1. 首先检查系统是否安装了gcc编译器

2. 下载RabbitMQ最新版本

3. 查看RabbitMQ支持的最新的erlang的版本

4. 下载erlang源码

5. 安装erlang
    解压
    tar -xvzf otp_src_19.0.tar.gz
    配置
    ./configure --prefix=/usr/local/erlang  --disable-javac
    ./configure --prefix=/usr/local/erlang  --without-javac
    -- 执行上一个步骤的时候出现了错误
    checking whether posix_fallocate() works... yes
    checking whether the emulator should use threads... yes; thread support required and therefore forced
    checking whether lock checking should be enabled... no
    checking whether lock counters should be enabled... no
    checking whether dlopen() needs to be called before first call to dlerror()... no
    checking for kstat_open in -lkstat... (cached) no
    checking for tgetent in -ltinfo... no
    checking for tgetent in -lncurses... no
    checking for tgetent in -lcurses... no
    checking for tgetent in -ltermcap... no
    checking for tgetent in -ltermlib... no
    configure: error: No curses library functions found
    configure: error: /bin/sh '/opt/otp_src_20.3/erts/configure' failed for erts
    
    原因：
    缺少ncurses安装包
    解决办法
    下载安装相应软件包
    一、如果你的系统是RedHat系列：
    yum list|grep ncurses
    执行上边的命令出现下面的错误：
    Repodata is over 2 weeks old. Install yum-cron? Or run: yum makecache fast
    执行yum makecache fast命令之后没有问题
    然后在list中找到ncurses，根据机器的cpu架构是否是64位的执行
    yum install ncurses-devel.x86_64
    二、如果你的系统是Ubuntu或Debian：
    apt-cache search ncurses
    apt-get install libncurses5-dev
    
    结果又报错了
    *********************************************************************
    **********************  APPLICATIONS DISABLED  **********************
    *********************************************************************

    odbc           : ODBC library - link check failed
    orber          : No C++ compiler found

    *********************************************************************
    *********************************************************************
    **********************  APPLICATIONS INFORMATION  *******************
    *********************************************************************

    wx             : wxWidgets not found, wx will NOT be usable

    *********************************************************************
    *********************************************************************
    **********************  DOCUMENTATION INFORMATION  ******************
    *********************************************************************

    documentation  : 
                     xsltproc is missing.
                     fop is missing.
                     The documentation can not be built.

    *********************************************************************

    首先http://www.unixodbc.org/ 下载最新的odbc安装包
    解压后进入odbc目录执行
    ./configure --prefix=/usr/local/unixODBC-2.3.6
    
    还是失败 所以选择yum安装
    ok 然后解决
    orber          : No C++ compiler found 这个问题
    
    使用yum安装gcc-c++  
    
    make
    make install
    
    测试Erlang是否安装正确：
    `# /home/erlang/bin/erl`
    Erlang/OTP 17 [erts-6.0] [source] [64-bit] [async-threads:10] [hipe] [kernel-poll:false]
    Eshell V6.0  (abort with ^G)
    1> EvenN = lists:filter (fun (N) -> N rem 2 == 0 end, lists:seq(1,100)).
    [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,
     44,46,48,50,52,54,56,58|...]
    2> halt().
    【安装总结】
    从源码编译安装Erlang，有两个库或工具是必须的：
    一是完整的GCC编译器环境
    二是Ncurses开发库

    还有一些库或工具，如果没有它们，在编译配置时会出现警告信息，而且可能不能通过配置。这些库有：
    1）  OpenSSL开发库
    2） ODBC开发库
    3） Java编译器
    
5. 安装RabbitMQ
    rpm -ivh --nodeps  rabbitmq-server-3.7.4-1.el7.noarch.rpm
    centos查看系统日志：
    journalctl -xe
    
    
    
上边的打开方式不正确很坑下面讲解正确的打开方式：
https://www.rabbitmq.com/install-rpm.html

2. 安装Zero-dependency Erlang from RabbitMQ 
3. 安装RabbitMQ rpm包
rpm --import https://www.rabbitmq.com/rabbitmq-release-signing-key.asc
`# this example assumes the CentOS 7 version of the package`
yum install rabbitmq-server-3.7.4-1.el7.noarch.rpm

chkconfig rabbitmq-server on

/sbin/service rabbitmq-server start

/sbin/service rabbitmq-server stop

The broker creates a user guest with password guest
三、配置网页访问RabbitMQ

1、查看RabbitMQ中用户命令

rabbitmqctl list_users

2、创建用户命令

 rabbitmqctl add_user hjp hjp

3、赋予用户权限命令

 rabbitmqctl  set_permissions -p "/" hjp '.*' '.*' '.*'

4、赋予用户角色命令

 rabbitmqctl set_user_tags hjp administrator

5、开启rabbitmq管理控制台命令


rabbitmq-plugins enable rabbitmq_management

6、访问http://192.168.196.136:15672/