---
layout: post
title:  "Tomcat源码阅读"
date:   2023-07-20 04:32:24 +0800
categories: tomcat
tags: tomcat
permalink: /tomcat/read-source
published: true
publish_file: 2023-07-20-tomcat-read-source.md
toc: true
---
# Tomcat源码阅读


## 准备
1. 下载tomcat 9.0.78源码
    `git clone -b 9.0.78 https://github.com/apache/tomcat.git`
2. 详细阅读源码目录中的`BUILDING.txt`文件
3. 下载安装ant
    - 下载ant压缩包`wget https://dlcdn.apache.org//ant/binaries/apache-ant-1.10.13-bin.tar.gz`，解压缩到指定目录
    - 配置`ANT_HOME`的环境变量，并在PATH环境变量后面加入`$ANT_HOME/bin`,让ant命令可以直接在shell中使用
    - shell中直接执行`ant -version`,见到下面的输出说明ant安装成功了。
        ```shell
        Apache Ant(TM) version 1.10.13 compiled on January 4 2023
        ```
4. tomcat源码根目录下新建文件`build.properties`,内容如下
    ```properties
    ## 指定ant下载依赖jar包的位置，建议不要放在tomcat源码目录下
    base.path=/Users/admin/libs

    ## 配置ant下载时使用的代理，国内网络环境导致下载jar包巨慢
    ## 如果不代理的话下面的配置就不要添加，具体怎么搭建代理，网上很多文章可以看，这里就不展开说了
    proxy.use=true
    proxy.host=domain
    proxy.port=8118
    ```
5. tomcat源码目录下直接执行命令`ant`,看到下面的输出，说明构建成功了，tomcat的源码编译还是很快的，依赖的jar包少。
    ```shell
    BUILD SUCCESSFUL
    Total time: 1 minute 12 seconds
    ```
6. 一般需要在ide中打开源码来debug调试，这样的话需要在tomcat源码根目录下执行命令`ant -buildfile build.xml ide-intellij` 生成idea的配置文件，直接用idea打开项目
7. idea中找到类，`org.apache.catalina.startup.Bootstrap` 直接启动即可，tomcat启动的时候可能会出现中文乱码，通过添加jvm启动参数`-Duser.language=en`解决 
9. 好啦，现在可以愉快的在idea中调试tomcat源码了。

