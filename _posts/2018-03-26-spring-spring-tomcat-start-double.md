---
layout: post
title:  "Spring项目,Tomcat启动时加载了两次"
date:   2018-03-26 10:00:00 +0800
categories: spring
tags: spring
permalink: /spring/spring-tomcat-start-double
published: true
publish_file: 2018-03-26-spring-spring-tomcat-start-double.md
toc: true
---
# Spring项目,Tomcat启动时加载了两次

  今天开发项目的时候，发现tomcat加载了两次项目。
先交代一下开发环境：
 `eclipse`
 `tomcat 7`
  首先排查了spring的配置文件和web.xml文件是否加载了两次Spring的容器，但是并没有发现问题。随后感觉像是tomcat的问题。
随后在网上找到了问题所在

## 问题原因 ：
虚拟目录引起的问题，我们在Host标签里配置了appBase="webapps"，tomcat加载一次应用。这里配置了一次docBase，tomcat又去加载一次应用。

```xml
<Host appBase="webapps" autoDeploy="true" name="localhost" unpackWARs="true">


        <!-- SingleSignOn valve, share authentication between web applications
             Documentation at: /docs/config/valve.html -->
        <!--
        <Valve className="org.apache.catalina.authenticator.SingleSignOn" />
        -->


        <!-- Access log processes all example.
             Documentation at: /docs/config/valve.html
             Note: The pattern used is equivalent to using pattern="common" -->
        <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs" pattern="%h %l %u %t &quot;%r&quot; %s %b" prefix="localhost_access_log." suffix=".txt"/>

      <Context docBase="backend" path="/cf-hrtop" reloadable="true" source="org.eclipse.jst.jee.server:backend"/></Host>
```

## 解决办法：

开发项目的时候难免就会出现项目名字和项目访问的路径不一样的情况。
eclipse的修改方式是：
![](/assets/notes/spring/spring-tomcat-start-double-01.png)
但是这样修改的话eclipse会自动吧tomcat的server.xml改成上边xml中的样式。
如果用eclipse重新部署的话还会出现这个问题。但是如果每次自己手动改server.xml文件的话有很麻烦。感觉像是eclipse的一个bug。
其实不然，eclipse的开发者应该早就想到这个问题了，在我们第一次配置tomcat的时候，eclipse给出的配置是这样的
![](/assets/notes/spring/spring-tomcat-start-double-02.png)
默认的部署路径并不是webapps而是wtpwebapps这个路径，
而且eclipse在启动tomcat的时候会指定一个参数
`-Dwtp.deploy=D:\dev_workspace\webserver\tomcat\apache-tomcat-7.0.82-top-hr\wtpwebapps`
上边这个命令的意思就是将tomcat的部署路径指定到wtpwebapp这个目录下，也就是eclipse给tomcat的默认的部署路径，这个就是eclipse的解决方式。


----------
我还是更喜欢idea开发工具的解决方式，直接吧部署到webapps下的项目文件夹名字改掉了想要的项目访问目录的名字，这样更简单，更有效。