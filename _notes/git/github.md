# GitHub


## Github Pages
[官网](https://pages.github.com)
[githu pages使用的组件版本](https://pages.github.com/versions/ )

### Jekyll
[官网](https://jekyllrb.com/)

将文本转换成静态网站或者是博客

[文档](https://jekyllrb.com/docs)

[一些主题](https://jekyllrb.com/docs/themes/)
[好看的主题](https://github.com/mmistakes/minimal-mistakes )
[更炫酷的主题](http://jekyllthemes.org/themes/jekyll-theme-chirpy/)
[文档](https://mmistakes.github.io/minimal-mistakes/docs/quick-start-guide/ )

### 安装jekyll

[官方安装文档](https://jekyllrb.com/docs/installation/)


## 问题

### ssh: connect to host github.com port 22: Connection refused

```shell
$ git pull
ssh: connect to host github.com port 22: Connection refused
fatal: Could not read from remote repository.
​
Please make sure you have the correct access rights
and the repository exists.
```

解决方式

```shell
$ vim ~/.ssh/config

# Add section below to it
Host github.com
  Hostname ssh.github.com
  Port 443

$ ssh -T git@github.com
Hi xxxxx! You've successfully authenticated, but GitHub does not
provide shell access.
```