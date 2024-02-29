# Git


## 常用命令 

同步远程已经删除的分支
    查看本地分支和追踪情况： git remote show origin
    同步分支： git remote prune origin

## 解决github拉取代码 慢的问题
   1. 首先搭建科学上网工具 本地开启代理
   2. git config --global http.proxy 'socks5://127.0.0.1:1080'
      git config --global https.proxy 'socks5://127.0.0.1:1080'

      git config http.proxy 'socks5://127.0.0.1:1080'
      git config https.proxy 'socks5://127.0.0.1:1080'

      取消代理
      git config --global --unset http.proxy
      git config --global --unset https.proxy
      
    https://www.cnblogs.com/StevenWind/p/11735352.html

    
