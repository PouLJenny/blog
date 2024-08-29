# Manjaro配置远程桌面



## 安装RDP

1. 安装
```shell
sudo pacman -Syu yay
# 安装xrdp之前可能需要安装一些开发包,因为需要做源码的编译
sudo pacman -S base-devel
yay -S xrdp xorgxrdp-glamor pulseaudio-module-xrdp
```

2. 配置
编辑文件`/etc/X11/Xwrapper.config`
添加配置
```config
allowed_users=anybody
needs_root_rights=no
```

3. 配置
```shell
cp /etc/X11/xinit/xinitrc ~/.xinitrc
vim ~/.xinitrc
```

修改成下面的配置
```config
# 注释掉.xinitrc最后几行
# twm &
# xclock -geometry 50x50-1+1 &
# xterm -geometry 80x50+494+51 &
# xterm -geometry 80x20+494-0 &
# exec xterm -geometry 80x66+0+0 -name login
export DESKTOP_SESSION=plasma
exec /usr/lib/plasma-dbus-run-session-if-needed startplasma-x11
```

4. `/etc/pam.d/xrdp-sesman`
```config
#%PAM-1.0
auth        include     system-remote-login
-auth       optional    pam_gnome_keyring.so
-auth       optional    pam_kwallet5.so
account     include     system-remote-login
password    include     system-remote-login
-password   optional    pam_gnome_keyring.so    use_authtok
session     include     system-remote-login
-session    optional    pam_gnome_keyring.so    auto_start
-session    optional    pam_kwallet5.so         auto_start
```

5. 提高画质 `/etc/xrdp/xrdp.ini`
```ini
bitmap_compression=false
bulk_compression=false
max_bpp=32
```

6. 启动服务
```shell
sudo systemctl enable --now xrdp.service xrdp-sesman.service

sudo systemctl restart xrdp.service xrdp-sesman.service
```

7. 一些问题

发现每次restart xrdp的时候都会出现连接黑屏的问题

### 参考文档

https://alvin.red/2021/11/06/archlinux-xrdp/ , 此博客有些错误的地方
https://wiki.archlinux.org/title/Xrdp, archlinux官方的文档，我觉得看这个就足够了