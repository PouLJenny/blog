# NFS

https://en.wikipedia.org/wiki/Network_File_System


## linux安装nfs服务端

https://www.cnblogs.com/misfit/p/10552547.html


### 安装NFS软件
```shell
# 安装
# NFS主程序
sudo pacman -S nfs-utils
# PRC主程序
sudo pacman -S rpcbind
```
### 配置NFS服务端
`sudo vim /etc/exports`

```conf
# [共享目录]    [客户端地址1(权限)]    [客户端地址2(权限)]    ...
# [共享目录]    [客户主机名1(权限)]    [客户主机名2(权限)]    ...
# 设置目录最高权限        sudo chmod 777 [共享目录] 
/tftp1    10.82.16.233(rw,no_root_squash,no_subtree_check,sync)    
/tftp2    *(rw,no_root_squash,no_subtree_check,sync)

/home/poul/workspace  *(rw,all_squash,sync,insecure,anonuid=1000,anongid=1000)
```


mac挂载我的linux共享目录
```shell
## noappledouble 参数解决._前缀的文件的问题
sudo mount -o noappledouble,noserverino -t nfs poul-work:/home/poul/workspace /Users/poul/poul_work_workspace_share
sudo mount -t nfs 192.168.31.240:/run/media/poul/0e95d2b1-3be7-4243-a987-43126704be5e/nfs_share  /Users/admin/nfs_share
finder 直接访问 nfs://192.168.31.240/run/media/poul/0e95d2b1-3be7-4243-a987-43126704be5e/nfs_share
```

挂载的时候可能会提示权限的问题，需要添加配置`anonuid=1000,anongid=1000`


卸载nfs目录
```shell
sudo umount /mnt/nfs
```