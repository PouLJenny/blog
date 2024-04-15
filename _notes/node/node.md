# Node

几个npm使用国内镜像加速的方法，

## 一、修改成腾讯云镜像源
1. 命令
    `npm config set registry http://mirrors.cloud.tencent.com/npm/`
2. 验证命令
    `npm config get registry`
    如果返回http://mirrors.cloud.tencent.com/npm/，说明镜像配置成功。
## 二、修改成淘宝镜像源
1. 命令
    `npm config set registry https://registry.npmmirror.com`
2. 验证命令
    `npm config get registry`
    如果返回https://registry.npmmirror.com，说明镜像配置成功。
## 三、修改成华为云镜像源
1. 命令
    `npm config set registry https://mirrors.huaweicloud.com/repository/npm/`
2. 验证命令
    `npm config get registry`
    如果返回https://mirrors.huaweicloud.com/repository/npm/，说明镜像配置成功。

## 四、通过使用淘宝定制的cnpm安装
1. 安装cnpm
    `npm install -g cnpm --registry=https://registry.npmmirror.com`
2. 使用cnpm
    `cnpm install xxx`

## 管理多个版本的NODE

在本地管理多个版本的Node.js，最常用且方便的工具是 nvm（Node Version Manager）。nvm 允许你在同一台机器上安装和切换多个Node.js版本，这对于开发多个项目或需要测试在不同Node.js环境下的兼容性非常有帮助。以下是如何在不同操作系统上使用 nvm 来管理Node.js版本的步骤：

```shell
brew install nvm
```

配置环境：
安装完成后，你可能需要重启终端或者手动执行下面的命令来使nvm命令生效：

