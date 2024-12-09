# mac系统常用工具

## homebrew 

国内快速安装方式
https://www.jianshu.com/p/e0471aa6672d


### 加速 - 配置阿里云镜像

[国内homebrew加速配置阿里云镜像](https://learnku.com/mac/wikis/39228 )

更换 brew.git
```shell
cd "$(brew --repo)"
git remote set-url origin https://mirrors.aliyun.com/homebrew/brew.git
```

更换 homebrew-core.git
```shell
cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://mirrors.aliyun.com/homebrew/homebrew-core.git
```

执行更新命令
```
brew update
```

此时可以执行 `brew config` 命令，查看配置信息：


更换 homebrew-bottles
接下来是二进制文件下载的设置。
这与你当前 macOS 系统使用的 shell 版本有关系，执行以下命令查看 Shell 版本
```shell
echo $SHELL
```
根据版本不同，会输出 2 种结果，/bin/zsh 或 /bin/bash，根据类型进行操作即可
/bin/zsh
```shell
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.aliyun.com/homebrew/homebrew-bottles' >> ~/.zshrc
source ~/.zshrc
```

/bin/bash
```shell
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.aliyun.com/homebrew/homebrew-bottles' >> ~/.bash_profile
source ~/.bash_profile
```

到这里，更换 Homebrew 默认源的所有操作啦，尽情地去 brew install 吧！


恢复默认配置
出于某些场景，可能需要回退到默认配置，你可以通过下述方式回退到默认配置。
```shell
# 重置brew.git:
cd "$(brew --repo)"
git remote set-url origin https://github.com/Homebrew/brew.git

# 重置homebrew-core.git:
cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://github.com/Homebrew/homebrew-core.git
```

然后删掉 HOMEBREW_BOTTLE_DOMAIN 环境变量，将你终端文件 `~/.bash_profile` 或者 `~/.zshrc` 中 `HOMEBREW_BOTTLE_DOMAIN` 行删掉，并执行
```shell
source ~/.bash_profile
## 或者是
source ~/.zshrc
```

## 禁用swap
https://blog.ixiaocai.net/2020/12/31/Disable_Swap_On_Macos_Catalina.html
https://www.bilibili.com/read/cv10125678/

## 限制进程CPU使用率
https://sspai.com/post/67331

## 查询端口占用
`lsof -i tcp:port`

## 局域网工具

### 查询所有的局域网ip
`arp -a`
### 查询ip对应的hostname
`smbutil status ip`
### 通过主机名查ip
`smbutil lookup ABCD`


## App包内无权限操作
比如你在Application的某个Contents里面要操作数据，正常macos是提示操作受限制的比如
```shell
liqiushi@bogon staruml % cp app.asar /Applications/StarUML.app/Contents/Resources/
cp: /Applications/StarUML.app/Contents/Resources/app.asar: Operation not permitted
```

这个是macos的保护机制
system integrity protection (SIP)

怎么解决这个问题呢？
[stackoverflow有此解决方案](https://stackoverflow.com/questions/32659348/operation-not-permitted-when-on-root-el-capitan-rootless-disabled )

总结下来分这么几个步骤：

1. 进入Recovery System
    - Intel处理器 在电脑开机时候马上按着Command+R 不放，等出现苹果标志3秒之后，松开按键等待进入Recovery 模式
    - M1/M2 处理器  将Mac关机，按住开机电源键不要松开，等出现选项后，再松开电源键，然后点击选项即可进入Recovery 模式
2. 禁用sip
    ```shell
    csrutil disable
    ## 查看禁用状态
    csrutil status
    ```
3. 重启电脑 执行受限制的操作
4. 执行步骤1进入 Recovery System，启用sip
    ```shell
    csrutil enable
    ```
5. 正常重启电脑

## SoundSource

https://www.macappbox.com/a/soundsource.html
https://rogueamoeba.com/support/knowledgebase/?showArticle=ACE-StepByStep&product=SoundSource&arch=mchip&step=7#aceinstall

## 修改电脑时区

https://testingbot.com/software-testing-questions/how-to-change-your-time-zone-on-mac


## 保持电脑唤醒状态

```shell
caffeinate -d
```

# EOF