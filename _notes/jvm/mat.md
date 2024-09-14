# MAT

https://www.eclipse.org/mat/


## 安装

macos安装问题

```
The JVM shared library "/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/../lib/server/libjvm.dylib"
does not contain the JNI_CreateJavaVM symbol.
```

解决方式：
```shell
cd /Applications/mat.app/Contents/Eclipse
```

修改文件 `MemoryAnalyzer.ini`添加指定的java路径,这个配置要放到最上面
```config
-vm
/Users/poul/workspace/soft/jdk-17.0.7.jdk/Contents/Home/bin/java
```

然后就可以启动了


## Manjaro 使用mat出现错误
```
No more handles because there is no underlying browser available," it may be because your operating system doesn't support the embedded browser widget or it needs to be configured. To fix this, you can try installing WebKit with its GTK 3.x bindings. The WebKit2 API level is preferred, and GTK4 doesn't currently support browsers.
```

```shell
sudo pacman -S webkit2gtk
sudo pacman -S gtk3
sudo pacman -S libffi gobject-introspection
```

安装完了后需要重启mat才能生效.