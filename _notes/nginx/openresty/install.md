# 安装

## 源码安装

### Linux (arch)

1. 下载源码包 [在页面](https://openresty.org/cn/download.html '')
   解压
   ```shell
   tar -xzvf openresty-VERSION.tar.gz
   ```

2. 然后在进入 openresty-VERSION/ 目录, 然后输入以下命令配置:
    ```shell
    ./configure --prefix=/home/poul/workspace/soft/openresty/openresty-install
    ## 下面是石杉的流量课中的安装方法
    cd bundle
    wget https://github.com/FRiCKLE/ngx_cache_purge/archive/2.3.tar.gz  
    tar -xvf 2.3.tar.gz 

    wget https://github.com/yaoweibin/nginx_upstream_check_module/archive/v0.3.0.tar.gz  
    tar -xvf v0.3.0.tar.gz

    ./configure --prefix=/home/poul/workspace/soft/openresty/openresty-install --with-http_xslt_module --with-http_addition_module --with-http_realip_module  --with-pcre  --add-module=./bundle/ngx_cache_purge-2.3/ --add-module=./bundle/nginx_upstream_check_module-0.3.0/ --add-module=/home/poul/workspace/soft/openresty/ngx-fancyindex -j2  
    ```
    默认, `--prefix=/usr/local/openresty` 程序会被安装到`/usr/local/openresty`目录。
 
3. `make && make install`