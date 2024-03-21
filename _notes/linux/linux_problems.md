2017-06-15

  今天是学习Linux的第一天，在此把学习期间遇到的各种问题记录下来，方便后期查阅
  1. JDK的配置 
     1.1  官网下载最新的jdk文件（tar.gz格式）
     1.2  使用md5sum/sha512sum命令查看文件是否被篡改过
     1.3  使用tar命令将压缩包解压到相应的位置（tar -zxvf  *.tar.zip -C /root/test）
     1.4  配置JDK的环境变量 
       1.4.1   修改/etc/profile文件当本机仅仅作为开发使用时推荐使用这种方法，因为此种配置时所有用户的shell都有权使用这些环境变量，
               可能会给系统带来安全性问题
               在/etc/profile 这个文件中的尾部追加
               export JAVA_HOME=...这里写jdk的home路径
               export PATH=$JAVA_HOME/bin:$PATH
               export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar

               source一下文件 
       1.4.2   修改.bashrc文件这种方法更为安全，它可以把使用这些环境变量的权限控制到用户级别，如果需要给某个用户权限使用这些环境变量，
               只需要修改其个人用户主目录下的.bashrc文件就可以了。
               在.bashrc文件末尾追加
               export JAVA_HOME=...这里写jdk的home路径
               export PATH=$JAVA_HOME/bin:$PATH
               export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar

               source一下文件
       1.4.3   直接在shell下设置变量不推荐使用这种方法，因为换个shell，该设置就无效了。这种方法仅仅是临时使用，以后要使用的时候又要重新设置，
               比较麻烦。只需在shell终端执行下列命令：
               export JAVA_HOME=...这里写jdk的home路径
               export PATH=$JAVA_HOME/bin:$PATH
               export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
       
       注意：1.要将 /usr/share/jdk1.5.0_05jdk 改为jdk安装目录
             2. linux下用冒号”:”来分隔路径
             3. $PATH / $CLASSPATH / $JAVA_HOME 是用来引用原来的环境变量的值在设置环境变量时特别要注意不能把原来的值给覆盖掉了。
             4. CLASSPATH中当前目录”.”不能丢掉。
             5. export是把这三个变量导出为全局变量。
             6. 大小写必须严格区分。
     1.5 linux服务器启动tomcat很慢解决方法
        在JVM环境中解决
            打开$JAVA_PATH/jre/lib/security/java.security这个文件，找到下面的内容：
            securerandom.source=file:/dev/urandom
            替换成
            securerandom.source=file:/dev/./urandom
  2. 配置root用户登录
     2.1 输入sudo gedit /usr/share/lightdm/lightdm.conf.d/50-ubuntu.conf
     2.2 在弹出的编辑框里输入：greeter-show-manual-login=true 保存关闭。
     2.3 关闭之后，回到终端窗口，输入：sudo passwd root  回车；回车之后会要你输入两次密码，出现已成功更新密码字样即为成功。
     2.4 关机重启
2017-06-18
  1. 安装eclipse
    1.1 使用tar命令将压缩包解压到相应的位置
    1.2 由于在Ubuntu16.04LTS版本中eclipse存在菜单栏不显示的BUG需要一下方法进行修正
      1.2.1 创建.sh的文件，里面写入
            #!/bin/bash
            export UBUNTU_MENUPROXY=0
            /root/devtools/eclipse/eclipse
            最下边是eclipse的路径
      1.2.2 在用户下边的.bashrc文件中添加自定义命令starteclipse来启动eclipse
            使用vim命令在文件中添加alias starteclipse = '这里面填写需要执行的命令';
    1.3 在执行了上面两步之后我发现直接自定义一个命令来执行'export UBUNTU_MENUPROXY=0 && /root/devtools/eclipse/eclipse'
        不就可以了吗，哈哈哈哈。。。
  2. Linux顺序执行多个命令
    2.1 命令1;命令2   多个命令顺序执行，命令之间没有任何逻辑关系
    2.2 命令1&&命令2  逻辑与 当命令1正确执行的时候，命令2才会执行,否则命令2不执行
    2.3 命令1||命令2  逻辑或 当命令1正确执行的时候，命令2不会执行，否则命令2执行
  3. 修改MAVEN的仓库地址，找到conf下面的setting.xml文件加入
     <localRepository>/home/root/mvnrepository</localRepository>
  4. 修改MAVEN的仓库镜像为阿里云的 找到conf下面的setting.xml文件加入
     <mirrors>
       <mirror>
        <id>alimaven</id>
        <name>aliyun maven</name>
        <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
        <mirrorOf>central</mirrorOf>        
       </mirror>
     </mirrors>
        
  5. Ubuntu安装显卡驱动的时候出现
     dpkg: 依赖关系问题使得 fglrx-core 的配置工作不能继续：
     fglrx-core 依赖于 lib32gcc1；然而：
     未安装软件包 lib32gcc1。
     fglrx-core 依赖于 libc6-i386；然而：
     未安装软件包 libc6-i386。
     fglrx-core 依赖于 dkms；然而：
     未安装软件包 dkms。
     说明缺少哦必要的包，这个时候执行命令sudo apt install lib32gcc1 libc6-i386 dkms;
     将所有的依赖包安装完之后在执行安装命令就可以了。
     安装依赖需要一次安装完成，切勿单个安装，主要是由于包之间彼此会有一定的依赖关系，这个是你无法准确定位的，故在一次安装动作中做完。

2017-06-29
  1. 在刚修改完root权限自动登录后，发现开机出现以下提示：
     Error found when loading /root/.profile
     stdin:is not a tty
     …………
     解决方法：在终端中用命令gedit /root/.profile，打开文件后找到“mesg n”，
     将其更改为“tty -s && mesg n”。

~                                       


2017-11-02

	1. 查看某端口的占用情况 lsof -i:端口号  ；    netstat -anp | grep $port
    
2017-11-11
    
    1. centos查看系统信息 uname -a ; cat /proc/version; cat /etc/issue;  lsb_release -a;  cat /etc/redhat-release;
    2. centos7 防火墙配置
        
        查看已经开启的端口： firewall-cmd --list-ports 
        开启端口
        firewall-cmd --zone=public --add-port=80/tcp --permanent
        命令含义：
        --zone #作用域
        --add-port=80/tcp  #添加端口，格式为：端口/通讯协议
        --permanent  #永久生效，没有此参数重启后失效
        
        查询端口号80 是否开启：firewall-cmd --query-port=80/tcp
        移除80端口号：firewall-cmd --permanent --zone=public --remove-port=80/tcp
        重启防火墙
        firewall-cmd --reload
        开启防火墙
        systemctl start firewalld
        关闭防火墙
        systemctl stop firewalld
        禁用防火墙
        systemctl disable firewalld
        查看防火墙状态
        systemctl status firewalld.service
        禁ping
        firewall-cmd --permanent --add-rich-rule='rule protocol value=icmp drop'
    3. linux 中redis安装过程
    
        1.  从官网下载的压缩文件解压
        2.  进入压缩文件的根目录执行make方法
            如果 失败 
            1. 安装  yum install gcc-c++
            2. 编译选择参数  make MALLOC=libc
        3. 编译成功后  安装到指定目录 make PREFIX=/usr/local/redis install
        4. 把redis.conf cp 到安装根目录
        5. 修改redis.conf 为 bind 0.0.0.0 (运行别的ip的机器远程访问)   daemonize yes (按照后台运行方式启动redis)
        6. bin目录下 使用redis-server ../redis.conf 命令启动redis
        7. 在bin目录下边使用redis-cli 命令进入命令模式
        
2017-12-01
 
    1. linux设置固定IP
       http://blog.csdn.net/johnnycode/article/details/40624403
       
2017-12-06

    1. SSH客户端连接服务器（口令认证）
       直接连接到对方的主机，这样登录服务器的默认用户
       $ssh 192.168.142.84 
       使用账号登录对方主机nii用户
       [admin@localhost ~]$ ssh nii@192.168.142.84
       
    2. SSH客户端连接服务器（秘钥认证）
       这种认证方式是比较安全的。
       秘钥认证步骤：
       1. 生成公钥和私钥，生成的秘钥默认在/root/.ssh/文件夹里面
          [root@localhost admin]# ssh-keygen 
       2. 把生成的公钥发送到对方的主机上去，用ssh-copy-id命令，自动保存在对方主机的/root/.ssh/authorized_keys 文件中去
          [root@localhost ~]# ssh-copy-id -i /root/.ssh/id_rsa.pub root@192.168.142.84
          
          [root@localhost ~]# ssh 192.168.142.84 登录不需要密码了
        网络链接：  
        http://www.linuxidc.com/Linux/2016-03/129204.htm
    3. linux查看磁盘空间
       使用“df -k”命令，以KB为单位显示磁盘使用量和占用率。
       使用“df -m”命令，以M为单位显示磁盘使用量和占用率。
       使用“du -k /home”命令，列出home目录下所有文件或目录占用的大小，以KB作为计量单位。
    4. linux 服务器之间传输文件
       1.scp传输
         scp -r /data/file root@ip:/data/
         scp -C /data/sda.img root@ip:/data/img/
         #-r: 支持目录
         #-C: 启用压缩传送
         
         http://www.linuxidc.com/Linux/2015-05/117028.htm
         
    5. linux nginx的安装
    
        1.  安装nginx必须的依赖包 
            [root@rhel6u3-7 ~]# yum -y install gcc gcc-c++ openssl-devel pcre-devel zlib-devel  //yum创建过程略，安装略 
        2.  安装编译nginx，目前系统测试环境为rhel6.3  软件版本为nginx-1.27
            [root@rhel6u3-7 ~]# useradd -s /sbin/nologin -M nginx //给nginx服务器创建后台进程管理用户 
            [root@rhel6u3-7 ~]# tar zxvf nginx-1.2.7.tar.gz  //解压缩 
            [root@rhel6u3-7 ~]# cd nginx-1.2.7  
            [root@rhel6u3-7 nginx-1.2.7]# ./configure --user=nginx --group=nginx --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_gzip_static_module --with-http_realip_module --with-http_sub_module --with-http_ssl_module  --with-stream
            // --user=nginx –group=nginx 设置允许nginx允许的用户和组为nginx 
            // --prefix=/usr/local/nginx/  设置nginx安装路径 
            // --with-http_stub_status_module 安装允许状态模块 
            // --with-http_ssl_module 安装ssl模块 
            //更多参数请参看 ./configure --help 
        3.  [root@rhel6u3-7 nginx-1.2.7]# make & make install   //编译安装过程略 
        4.  [root@rhel6u3-7 ~]# /usr/local/nginx/sbin/nginx  –V  //安装完成后查看Nginx的相关环境配置信息是否正确        
        5.  [root@rhel6u3-7 ~]# /usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf   // -c指向nginx主配置文件 
        6.  启动nginx  ./nginx  
            这个步骤出现了 [emerg]: getpwnam(“nginx”) failed 异常  解决方法：  没有安装nginx用户导致的无法启动 [root@localhost nginx-1.11.2]# useradd -s /sbin/nologin -M nginx
            
        链接: http://blog.51cto.com/dreamfire/1140965         https://www.cnblogs.com/hanyinglong/p/5102141.html
    6. linux 查看哪个端口被占用
       1. 安装netstat   yum install net-tools
       2. 使用 netstat   -anp   |   grep  portno
       
2017-12-12

    1. linux下安装多个tomcat ？

2017-12-30

    1. linux 查看系统变量  方法1： export  方法2: echo $JAVA_HOME
    
2017-12-32

    1. centos7 中提示 You have new mail in /var/spool/mail/root 
       这是LINUX的邮件提示功能。LINUX会定时查看LINUX各种状态做汇总，每经过一段时间会把汇总的信息发送的root的邮箱里，以供有需之时查看。
       
    2. cron  Linux的定时任务 ？
       
       1. 检查服务器定时器服务的状态
          命令：service crond status        
    
       查看crontab的执行日志  看 /var/log/cron这个文件就可以       
       
       编辑定时任务使用 crontab -e 其实就是编辑的/var/spool/mail/root 这个文件
       
    3. service ？

    4. centos目录结构
       
       https://www.cnblogs.com/ellisonDon/archive/2012/10/03/2710730.html
       
    5. Linux下tomcat启动慢  
        有两种解决办法：
        1）在Tomcat环境中解决
        可以通过配置JRE使用非阻塞的Entropy Source。
        在catalina.sh中加入这么一行：-Djava.security.egd=file:/dev/./urandom 即可。
        加入后再启动Tomcat，整个启动耗时下降到Server startup in 2912 ms。
        
        2）在JVM环境中解决
        打开$JAVA_PATH/jre/lib/security/java.security这个文件，找到下面的内容：
        securerandom.source=file:/dev/random
        替换成
        securerandom.source=file:/dev/urandom
        或
        securerandom.source=file:/dev/./urandom
    
     6. Linux自己装git?   

2018-01-17
    
    1. linux 安装docker 
       http://www.imooc.com/article/16448
       https://docs.docker.com/engine/installation/linux/docker-ce/centos/
      大家在国内使用，Docker Hub 速度慢，有什么好的解决方案？ https://www.daocloud.io/mirror
      
2018-03-15
    1. hohup和&的区别
        nohup是永久执行
        &是指在后台运行
        就是指，用nohup运行命令可以使命令永久的执行下去，和用户终端没有关系，例如我们断开SSH连接都不会影响他的运行，注意了nohup没有后台运行的意思；&才是后台运行
        &是指在后台运行，但当用户推出(挂起)的时候，命令自动也跟着退出
        http://blog.csdn.net/stpeace/article/details/76389073
        
2018-06-05
    1. linux时间问题
       NTP是网络时间协议(Network Time Protocol)，它是用来同步网络中各个计算机的时间的协议。
       百度百科：https://baike.baidu.com/item/NTP
       在Windwos中，系统时间的设置很简单，界面操作，通俗易懂。而且设置后，重启，关机都没关系。系统时间会自动保存在Bios的时钟里面，启动计算机的时候，
       系统会自动在Bios里面取硬件时间，以保证时间的不间断。但在Linux下，默认情况下，系统时间和硬件时间，并不会自动同步。在Linux运行过程中，
       系统时间和硬件时间以异步的方式运行，互不干扰。硬件时间的运行，是靠Bios电池来维持，而系统时间，是用CPU tick来维持的。
       在系统开机的时候，会自动从Bios中取得硬件时间，设置为系统时间。
       
       
       Linux硬件时间的设置   http://blog.sina.com.cn/s/blog_636a55070101u1mg.html
            硬件时间的设置，可以用hwclock或者clock命令。其中，clock和hwclock用法相近，只用一个就行，只不过clock命令除了支持x86硬件体系外，
            还支持Alpha硬件体系。
            //查看硬件时间可以是用hwclock，hwclock --show 或者hwclock -r
            [root@localhost ~]# hwclock --show
            2008年12月12日星期五 06时52分07秒  -0.376932 seconds
            //设置硬件时间
            [root@localhost ~]# hwclock --set --date="1/25/09 00:00" <== 月/日/年时:分:秒
            [root@localhost ~]# hwclock
            2009年01月25日星期日 00时00分06秒  -0.870868 seconds
            [root@localhost ~]# hwclock  -w   根据系统时间设置硬件时间
       系统时间和硬件时间的同步
            同步系统时间和硬件时间，可以使用hwclock命令。
            //以系统时间为基准，修改硬件时间
            [root@localhost ~]# hwclock --systohc<== sys（系统时间）to（写到）hc（Hard Clock）
            [root@localhost ~]# hwclock -w
            //以硬件时间为基准，修改系统时间
            [root@localhost ~]# hwclock --hctosys
            [root@localhost ~]# hwclock -s
        
        http://www.ntp.org.cn/pool.php#china
    2. 查看外网ip
        curl icanhazip.com  
        curl ifconfig.me  
        curl curlmyip.com  
        curl ip.appspot.com  
        curl ipinfo.io/ip  
        curl ipecho.net/plain  
        curl www.trackip.net/i  
        
2018-11-03
    1. linux批量替换文件字符 
        https://www.cnblogs.com/qq78292959/archive/2012/03/08/2385080.html
        find -name run.sh | xargs sed -i "s/-Dspring.redis.port=7000//g"
        find -name run.sh | xargs sed -i "s/-Dspring.redis.password=e\%KMP6T\*M0AX04\^d//g"
        
    2. 批量kill进程脚本
        ps -ef | grep rtprecv | grep -v grep | awk '{print $2}' | xargs kill -9
		
2019-03-13

	1. linux 使用supervisor来管理进程  
	   https://www.cnblogs.com/ydf0509/p/7747883.html
       http://supervisord.org/index.html

 ## 查询cpu信息

`lscpu` 


#### 每行管道输入执行一次命令
`... | xargs command`
```shell
cat error_customer_id_uniq.log  | awk '{print "curl http://172.21.15.20:8999/api/customer/es/syncCustomerById?id=" $1}' | head -1 | xargs command
```


### ssh超时自动断开问题
https://blog.csdn.net/qq_28296925/article/details/83828828#:~:text=%E6%96%B9%E6%B3%95%E4%B8%80%3A%E4%BF%AE%E6%94%B9%2Fetc%2F,config%E6%96%87%E4%BB%B6vi%20%2Froot%2F.

### 自己服务器的ssh端口 31010

### centeros升级python到3.8
https://blog.csdn.net/tony_vip/article/details/107161638

### 多网卡情况下联网问题（VPN）
https://diego.assencio.com/?index=d71346b8737ee449bb09496784c9b344

### Swap

#### 启用swap
https://azdigi.com/blog/en/linux-server-en/linux-fundementals/how-to-enable-swap-on-linux/
https://www.scaler.com/topics/how-to-increase-swap-space-in-linux/


### Too many open files

[讲的非常好的博客](https://imshuai.com/too-many-open-files-ulimit)

在 Linux 系统中，有多个地方可以设置和管理文件描述符（file descriptors）的限制。

1. 进程级别限制
使用 `ulimit` 命令可以在用户级别设置文件描述符的限制。
可以通过 `ulimit -n` 查看当前用户的文件描述符软限制，
通过 `ulimit -Hn` 查看硬限制。

1. 操作系统总限制
`cat /proc/sys/fs/file-max`
`sysctl fs.file-max`

1. 查看某个进程的限制
`cat /proc/3638917/limits`

1. 自己实验的小程序 `open-files.c`
```c
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/resource.h>

int main() {


    // 获取当前进程的ID
    pid_t processID = getpid();

    // 打印当前进程的ID
    printf("Current process ID: %d\n", processID);


    struct rlimit rlim;

    // 获取当前进程的文件句柄限制
    if (getrlimit(RLIMIT_NOFILE, &rlim) == 0) {
        if (rlim.rlim_cur == RLIM_INFINITY) {
            printf("Current process has no file descriptor limit (RLIMIT_NOFILE)\n");
        } else {
            printf("Current process has a file descriptor limit (RLIMIT_NOFILE): %ld\n", (long)rlim.rlim_cur);

	    // 设置软限制
        rlim.rlim_cur = 128;  // 例如，将软限制设置为 128

        // 设置当前进程的文件句柄限制
        if (setrlimit(RLIMIT_NOFILE, &rlim) == 0) {
            printf("Soft limit set successfully to %ld\n", (long)rlim.rlim_cur);
        } else {
            perror("Error setting soft limit");
        }
        }
    } else {
        perror("Error getting RLIMIT_NOFILE");
    }



    int fileDescriptor;
    char fileName[30];
    int counter = 1;

    while (1) {
        // Generate a new file name for each iteration
        sprintf(fileName, "file%d.txt", counter);

        // Open the file
        fileDescriptor = open(fileName, O_CREAT | O_RDWR, 0644);

        // Check if the file opening failed
        if (fileDescriptor == -1) {
            perror("Error opening file");
            break;
        }

        printf("File %s opened successfully with file descriptor: %d\n", fileName, fileDescriptor);

        counter++;
    }

    printf("Press Enter to close all opened files...\n");
    getchar();  // Wait for Enter key

    // Close all opened file handles
    for (int i = 1; i < counter; i++) {
        sprintf(fileName, "file%d.txt", i);
        close(open(fileName, O_RDONLY));  // Close the file
        printf("File %s closed\n", fileName);
    }

    return 0;
}
```

### AlmaLinux 8的GPG 密钥变更
```shell
rpm --import https://repo.almalinux.org/almalinux/RPM-GPG-KEY-AlmaLinux
dnf clean packages
yum update -y
```

https://almalinux.org/blog/2023-12-20-almalinux-8-key-update/
https://w3sun.com/3588.html


### linux端口网络限速

安装tc
```shell
yum install -y iproute-tc
```
