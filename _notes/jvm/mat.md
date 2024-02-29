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

修改文件 `MemoryAnalyzer.ini`添加指定的java路径
```config
-vm
/Users/poul/workspace/soft/jdk-17.0.7.jdk/Contents/Home/bin/java
```

然后就可以启动了

