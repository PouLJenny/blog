# Python

[官网](https://www.python.org/ )
[文档](https://docs.python.org/3/)
[tutorial](https://docs.python.org/3/tutorial/index.html)


## pyenv

使用`pyenv`来管理多个python版本


1. 安装一些必要的依赖项
```shell
sudo pacman -S base-devel
sudo pacman -S libffi
```

1. 安装`pyenv`：
```shell
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

1. 配置环境变量`/etc/profile`
```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
```

1. 安装Python 3.6：
```shell
pyenv install 3.6.15
## url可能访问非常慢，可以使用本地文件安装
cd ~/.pyenv/
mkdir cache
## 系统安装的时候会做编译操作，需要安装一些开发库
## CentOS 
sudo yum install -y gcc zlib-devel bzip2-devel readline-devel sqlite-devel openssl-devel tk-devel libffi-devel xz-devel
## 把Python-3.6.x.tar.xz安装包下载到此目录
pyenv install 3.6.15
```


1. 等待安装完成。安装成功后，你可以使用以下命令设置全局或局部的Python版本：
```shell
pyenv global 3.6.15  # 设置全局Python版本为3.6.15
```

1. 或者，你也可以在项目级别使用：
```shell
pyenv local 3.6.15  # 在当前项目目录下设置Python版本为3.6.15
```


其他的一些命令

1. 查看安装了哪些版本的
`pyenv versions`
1. 查看可安装的版本
`pyenv install -l`

## pip安装加速

配置文件`~/.pip/pip.conf`
```conf
[global]
index-url = http://pypi.douban.com/simple
[install]
trusted-host=pypi.douban.com
```
上面的豆瓣地址可以替换成其他的镜像地址:
1. https://pypi.tuna.tsinghua.edu.cn/simple
1. https://mirrors.aliyun.com/pypi/simple/
1. https://pypi.mirrors.ustc.edu.cn/simple/
1. http://pypi.douban.com/simple/

也可以使用临时的方式：

```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple package_name
```

## python 使用虚拟环境运行程序

python安装包的时候会碰到各种各样的问题：
- 全局安装的话，可能会有版本的冲突
- 有些安装包macos可能并不能执行安装

创建虚拟环境
```shell
python -m venv env
source env/bin/activate
```

下面再执行具体的安装就可以了

# EOF