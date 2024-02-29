# 安装部署git服务


```shell
sudo docker run -it -d --hostname git.poul666.top \
  --publish 19443:443 --publish 19980:80 --publish 19922:22 \
  --name gitlab \
  --volume $GITLAB_HOME/config:/etc/gitlab \
  --volume $GITLAB_HOME/logs:/var/log/gitlab \
  --volume $GITLAB_HOME/data:/var/opt/gitlab \
  -v /etc/localtime:/etc/localtime -v /etc/timezone:/etc/timezone \
  gitlab/gitlab-ce
```


sudo docker run -d -it --hostname git.poul666.top \
  --publish 19443:443 --publish 19980:80 --publish 19922:22 \
  --name gitlab \
  -v /etc/localtime:/etc/localtime -v /etc/timezone:/etc/timezone \
  gitlab/gitlab-ce