# docker

## 简介
docker是golang开发的 

[官网]('https://www.docker.com/' '')
[官方文档]('https://docs.docker.com/get-started/' '')

Docker容器的能力：
1. 文件系统隔离： 每个容器有自己的root文件系统
1. 进程隔离： 每个容器都运行在自己的进程环境中
1. 网络隔离： 容器间的虚拟网络接口和IP地址都是分开的
1. 资源隔离和分组： 使用cgroups讲CPU和内存之类的资源独立分配给每个docker容器

## 安装
### 在Linux中安装Docker
安装前检查：
    安装教程： https://docs.docker.com
  
阿里云镜像加速
网易云镜像加速

## 配置

### 修改默认的root dir

#### 方法1
查询当前的配置,默认情况下在 `/var/lib/docker` 目录下面
`sudo docker info | grep "Docker Root Dir"`

停掉Docker服务
`sudo systemctl stop docker`

复制整个 `/var/lib/docker` 目录到自定义的目录 `/data/docker`
`cp -R /var/lib/docker/ /data/docker/`

在systemctl配置文件中指定容器启动的参数 `--data-root` 来指定镜像和容器存放路径
`/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock --data-root /run/media/poul/新加卷/docker_data`

重新加载修改后的配置
`systemctl daemon-reload`

启动Docker服务
`sudo systemctl start docker`

#### 方法2
edit the `/etc/docker/daemon.json` file to contain the line
```json
{
    "data-root": "/mnt/docker-data",
    (...)
}
```

`sudo systemctl restart docker`

`docker info`


### 配置代理

[官方配置文档](https://docs.docker.com/engine/daemon/proxy/#daemon-configuration)

添加文件`/etc/systemd/system/docker.service.d/http-proxy.conf`

```conf
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:8118"
Environment="HTTPS_PROXY=http://127.0.0.1:8118"
```

然后执行`systemctl daemon-reload`

再执行`systemctl restart docker`重启一下docker服务

> 这里注意一下，需要把本地的代理服务开启域名的翻墙 `.docker.io`和`.docker.com`

## Dockerfile
[Reference文档](https://docs.docker.com/engine/reference/builder/ '')

从18.09版本开始，支持BuildKit 
To use the BuildKit backend, you need to set an environment variable `DOCKER_BUILDKIT=1` on the CLI before invoking `docker build`.

 A `Dockerfile` must begin with a `FROM` instruction.

## docker-compose
[Specifies文档](https://github.com/compose-spec/compose-spec/blob/master/spec.md '')



## 常用命令

- 进入运行中的docker容器的命令  `docker exec -it 64d99531cd10 /bin/bash`
- 在容器外执行某个容器内的命令 `sudo docker exec -it $DOCKER_ID /bin/bash -c 'cd /packages/detectron && python tools/train.py'`
- 解决docker container内时区跟宿主机不一致的问题的参数 `-v /etc/localtime:/etc/localtime -v /etc/timezone:/etc/timezone`
- 复制文件从宿主机到container `docker cp /path/source $DOCKER_ID:/path/target`
- 复制文件从container到宿主机 `docker cp $DOCKER_ID:/path/target /path/source`
- 访问宿主机IP https://jingsam.github.io/2018/10/16/host-in-docker.html
- docker container启动后修改 端口映射 https://cloud.tencent.com/developer/article/2170898

# EOF