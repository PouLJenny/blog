---
layout: post
title:  "JVM 源码阅读"
date:   2022-03-18 10:50:56 +0800
categories: jvm
tags: jvm
permalink: /jvm/read-source
published: true
publish_file: 2022-03-18-jvm-read-source.md
toc: true
---
# JVM 源码阅读

[github](https://github.com/openjdk/jdk)
[openjdk](https://openjdk.java.net/)
[openjdk8](https://github.com/openjdk/jdk8)

## JDK 11
### Linux 编译源码



## JDK 1.8

### MACOS 编译源码
https://www.cnblogs.com/jhxxb/p/11094578.html
1. 安装 mercurial
`brew install hg` 或者 `brew install mercurial`

    加速编译
    `brew install ccache`

2. 下载源码
```shell
hg clone http://hg.openjdk.java.net/jdk8u/jdk8u
cd jdk8u
bash get_source.sh
```

3. 阅读`README-builds.html` 文件，按照文档给出的指导进行下面的编译操作

4. 下载安装jdk7,jdk7和8是可以共存的


5. 执行配置 `bash ./configure --enable-ccache --with-boot-jdk=/Library/Java/JavaVirtualMachines/jdk1.7.0_80.jdk/Contents/Home --with-debug-level=slowdebug --with-native-debug-symbols=internal`
报错
```shell
configure: error: Failed to determine Xcode version.
# 查看xcode版本
xcodebuild -version
# 报错
xcode-select: error: tool 'xcodebuild' requires Xcode, but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance
# 由于本地安装了xcode 则直接执行下面的命令 问题解决
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
```

报错
```shell
configure: error: Could not find freetype!
## 安装
brew install freetype
```

最终输出信息
```shell
====================================================
A new configuration has been successfully created in
/Users/admin/Workspace/src/jdk8u/build/macosx-x86_64-normal-server-slowdebug
using configure arguments '--with-boot-jdk=/Library/Java/JavaVirtualMachines/jdk1.7.0_80.jdk/Contents/Home --with-debug-level=slowdebug --with-native-debug-symbols=internal'.

Configuration summary:
* Debug level:    slowdebug
* JDK variant:    normal
* JVM variants:   server
* OpenJDK target: OS: macosx, CPU architecture: x86, address length: 64

Tools summary:
* Boot JDK:       java version "1.7.0_80" Java(TM) SE Runtime Environment (build 1.7.0_80-b15) Java HotSpot(TM) 64-Bit Server VM (build 24.80-b11, mixed mode)  (at /Library/Java/JavaVirtualMachines/jdk1.7.0_80.jdk/Contents/Home)
* Toolchain:      clang (clang/LLVM)
* C Compiler:     Version 12.0.5 (at /usr/bin/clang)
* C++ Compiler:   Version 12.0.5 (at /usr/bin/clang++)

Build performance summary:
* Cores to use:   4
* Memory limit:   16384 MB
```

6. 编译
CONF参数可以不指定
`make images JOBS=8 CONF=macosx-x86_64-normal-server-slowdebug`

7. 验证是否成功
`./build/macosx-x86_64-normal-server-release/jdk/bin/java -version`
`/Users/admin/Workspace/src/jdk8u/build/macosx-x86_64-normal-server-slowdebug/jdk/bin/java -version`

### debug

#### gdb
mac 环境没法用 会卡住，现在官方还没给出解决方案
export LD_LIBRARY_PATH=/Users/admin/Workspace/src/jdk8u/build/macosx-x86_64-normal-server-slowdebug/hotspot/bsd_amd64_compiler2/debug
`gdb --args /Users/admin/Workspace/src/jdk8u/build/macosx-x86_64-normal-server-slowdebug/jdk/bin/java -version`

#### lldb 
由于gdb 没法用 
`lldb -- /Users/admin/Workspace/src/jdk8u/build/macosx-x86_64-normal-server-slowdebug/jdk/bin/java -version`

可能会碰到线程中断的问题
```shell
* thread #3, stop reason = signal SIGSEGV
    frame #0: 0x0000000108cc42b4
->  0x108cc42b4: movl   (%rsi), %eax
    0x108cc42b6: leaq   0xf8(%rbp), %rsi
    0x108cc42bd: vmovdqu %ymm0, (%rsi)
    0x108cc42c1: vmovdqu %ymm7, 0x20(%rsi)
Target 0: (java) stopped.
```
解决方式
```shell
process handle -p true -n true -s true SIGSEGV
c
```
最终成功

