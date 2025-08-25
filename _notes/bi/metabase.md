# Metabase

[官网](https://www.metabase.com/)
[github](https://github.com/metabase/metabase)


## docker部署

```shell
sudo docker pull metabase/metabase:v0.55.12.x
sudo docker run -it -d -p 3000:3000 -e TZ=Asia/Shanghai --name metabase metabase/metabase:v0.55.12.x
```

然后访问`http://localhost:3000/setup` 配置一些信息即可

# EOF