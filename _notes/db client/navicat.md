## navicat15 破解

### mac
https://www.geek-share.com/detail/2792406973.html

### linux 

https://github.com/HeQuanX/navicat-keygen-tools/blob/main/README.zh-CN.md

### 无限试用方式  15/16

https://gist.github.com/tuxity/32b353f00b38fe41c64434b98fdee077 这是个无限试用脚本
为防止此地址后期可能会无法访问，把此脚本粘出来
`navicat15_reset_trial.sh`
```shell
#!/bin/bash

set -e

file=$(defaults read /Applications/Navicat\ Premium.app/Contents/Info.plist)

regex="CFBundleShortVersionString = \"([^\.]+)"
[[ $file =~ $regex ]]

version=${BASH_REMATCH[1]}

echo "Detected Navicat Premium version $version"

case $version in
    "16")
        file=~/Library/Preferences/com.navicat.NavicatPremium.plist
        ;;
    "15")
        file=~/Library/Preferences/com.prect.NavicatPremium15.plist
        ;;
    *)
        echo "Version '$version' not handled"
        exit 1
       ;;
esac

echo -n "Reseting trial time..."

regex="([0-9A-Z]{32}) = "
[[ $(defaults read $file) =~ $regex ]]

hash=${BASH_REMATCH[1]}

if [ ! -z $hash ]; then
    defaults delete $file $hash
fi

regex="\.([0-9A-Z]{32})"
[[ $(ls -a ~/Library/Application\ Support/PremiumSoft\ CyberTech/Navicat\ CC/Navicat\ Premium/ | grep '^\.') =~ $regex ]]

hash2=${BASH_REMATCH[1]}

if [ ! -z $hash2 ]; then
    rm ~/Library/Application\ Support/PremiumSoft\ CyberTech/Navicat\ CC/Navicat\ Premium/.$hash2
fi

echo " Done"
```


### 模型存放文件夹位置

Macos
`/Library/Application\ Support/PremiumSoft\ CyberTech/Navicat\ CC/Navicat\ Premium/Profiles`


