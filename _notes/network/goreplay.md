# goreplay


[github](https://github.com/buger/goreplay)
[官方文档](https://github.com/buger/goreplay/tree/master/docs)
[一个不错的文档](https://goreplay.org/blog/goreplay-setup-for-testing-environments/)


## 流量录制


## 流量回放

```shell
sudo ./gor --input-file request-8073_0-rm-auth.gor  --output-http "http://127.0.0.1:8073" --http-allow-url ^/api/search/asinKeywords\?  \ 
--output-http-timeout 30s -output-http-workers 4  \
--middleware "/usr/bin/python set_auth_header.py" \
--rate 200% 
```

## 需要注意的问题
1. `--input-file-loop`  参数会导致 `--http-allow-url` 参数失效
2. `--rate` 参数也会导致 `--http-allow-url` 参数失效



