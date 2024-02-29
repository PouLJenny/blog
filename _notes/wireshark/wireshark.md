# Wireshark

## 简介

[官网](https://www.wireshark.org/ '')


## 如果抓取localhost的请求

mac系统 执行命令 添加本地的ip到网关

```shell
#                本地ip         网关        子网掩码
sudo route add 172.16.25.180 172.16.24.1 255.255.252.0
```


## 问题

### macos m1 Ventura 13.2.1 无权限抓网卡
[解决方式](https://packetpushers.net/macos-ventura-13-1-breaks-wireshark/#:~:text=If%20you%20open%20Wireshark%2C%20you,message%20when%20you%20run%20Wireshark. ) 
1. 每次重启电脑就会失效的方式
    ```shell
    sudo launchctl unload '/Library/LaunchDaemons/org.wireshark.ChmodBPF.plist'
    sudo launchctl load '/Library/LaunchDaemons/org.wireshark.ChmodBPF.plist'
    ```
2. 永久解决方式
    1. Open the Wireshark app
    2. In the top Menu Bar, click on Wireshark > About Wireshark
    3. Go to Folders and double-click on the macOS Extras blue text link to open a directory in Finder with a few PKG files
    4. Run and complete the Uninstall ChmodBPF.pkg  and  Remove Wireshark from the system path.pkg  installer files to remove these Wireshark dependencies
    5. Close the Wireshark app and windows and drag the app from the Applications folder to the trash to uninstall it
    6. Download the latest Wireshark version from https://www.wireshark.org/download.html
    7. Open the package and drag the Wireshark app to the Applications folder to install it
    8. Install the Uninstall ChmodBPF.pkg  and  Remove Wireshark from the system path.pkg  installer files as normal
        1. If you get a message saying “There is no application set to open the document…“, then right click on the file and click on Show Original, then run the package files from that Finder window
    9. Wireshark should now open properly and should also work after a reboot




