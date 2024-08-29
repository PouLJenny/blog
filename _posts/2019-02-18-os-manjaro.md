---
layout: post
title:  "弃用Windows，拥抱Linux- Manjaro"
date:   2019-02-18 10:00:00 +0800
categories: linux
tags: linux
permalink: /os/manjaro
published: true
publish_file: 2019-02-18-os-manjaro.md
toc: true
---
## 前言

作为一个软件开发工程师，你都会或多或少的接触到Linux，它强大的稳定可靠性在服务器领域占有一席之地。
为了学习Linux前段时间把自己的电脑装上了桌面版的Linux-Manjaro。之前用过一段时间的Ubuntu，最后放弃了，原因首先是在我的笔记本上经常出现各种问题不稳定，而且一些工作生活中的软件安装起来很费劲。  
而自从使用了Manjaro之后，我所有的书写代码、娱乐生活的操作都可以在这个系统上完成，可谓工作娱乐两不误，很好。

## 1 系统介绍
Manjaro基于Arch Linux，继承了Arch Linux滚动更新的特点，可以直接使用AUR上最齐全的软件。  
针对ArchLinux的“硬伤”、对新手不友好的“弱点”，Manjaro采用了图形化安装程序，使安装过程非常轻松、人性化，同时也把安装ArchLinux后的大量繁琐工作——安装配置显卡驱动、AUR、X服务、桌面环境、中文输入法、Flash插件、音频解码器、显示管理器等——全都做到位了，为新手解决了大麻烦，为高级用户节省了大量时间。
而且[distrowatch](https://distrowatch.com)排行榜，Manjaro现在稳居第一。  

## 2 安装过程

1. 下载manjaro镜像  
这里我选择17的最新稳定版本，桌面KDE 。  

2. 制作启动U盘  
manjaro的镜像跟windows的镜像有很大的区别，刚开始我使用软牒通把镜像刻录到U盘里无法启动，最后使用rufus的DD模式刻录成功。  

macos系统可以使用[etcherlaena)](https://etcher.balena.io/)替代

3. 安装  
安装的时候驱动选择free，BIOS选择UEFI模式并关掉安全检查  

4. 安装完的配置  
安装完成后，重启会进入到桌面  
配置国内的软件源   `sudo pacman-mirrors -i -c China -m rank`  
刷新缓存          `sudo pacman -Syy`  
添加Archlinux中文社区仓库 在 /etc/pacman.conf 文件的末尾添加以下两行  

```
[archlinuxcn] 
Server = https://mirrors.shu.edu.cn/archlinuxcn/$arch
```

安装 `archlinuxcn-keyring` 包导入GPG key.   `sudo pacman -Sy archlinuxcn-keyring`    
更新系统 `pacman -Syu`  这个过程差不多要20多分钟 跟新完了之后建议重启，检查这个更新是否成功 

安装输入法管理工具   
`sudo pacman -S fcitx-im`  #选择默认全选   

```shell
sudo pacman -S fcitx-configtool
```

改配置文件 `~/.xprofile` 和 `/etc/profile` 添加如下语句
  
```
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS="@im=fcitx"
```

注销重新登录就可以配置输入法了，输入法我没有选择搜狗输入法因为安装了搜狗输入法之后，它非常流氓的让我打不开输入法配置了，所以我选择manjaro系统默认的拼音输入法，自我感觉非常好用。

 
最后来一张自己的系统截图  
![](/assets/notes/os/manjaro-01.png)

**注意：**  
显卡驱动在没有找到很好的解决方案的时候尽量使用manjaro默认的驱动 不然非常容易导致电脑再也启动不了了。

## 友情链接
[Manjaro官网](https://manjaro.org/)  
[Manjaro中文网](https://www.manjaro.cn/)