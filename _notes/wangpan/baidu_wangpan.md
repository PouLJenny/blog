# 百度网盘



## 开放平台


[设备码授权模式](https://pan.baidu.com/union/doc/fl1x114ti)


1. 获取设备码、用户码
```shell
curl -L -X GET 'https://openapi.baidu.com/oauth/2.0/device/code?response_type=device_code&client_id=2905YlT7NExOqyESPfFlyoyNo&scope=basic,netdisk' \
-H 'User-Agent: pan.baidu.com' 
```

2. 授权
通过上个步骤获取到的信息来授权，使用网盘扫描完成授权

2. 用 Device Code 轮询换取 Access Token
```shell
curl "https://openapi.baidu.com/oauth/2.0/token?grant_type=device_token&code=24a6c07365899ff9cf3685a9725&client_id=2905YlT7AmxOqyESPfFlyoyNo&client_secret=NEq0BnRGV1gu8szpVAziL3OdUBY"

关于应用的相关信息，您可在控制台，点进去您对应的应用，查看应用详情获得。
```

# EOF

