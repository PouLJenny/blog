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