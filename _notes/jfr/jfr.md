# Java Flight Recorder

## 简介
[jdk11 troubleshooting guide](https://docs.oracle.com/en/java/javase/11/troubleshoot/index.html '') 里面有JFR的详细介绍

[jdk8 jfr guide](https://docs.oracle.com/javacomponents/jmc-5-5/jfr-runtime-guide/preface_jfrrt.htm#JFRRT165 '')

[jmc 官方文档](https://www.oracle.com/java/technologies/jdk-mission-control.html '')
[jmc github](https://github.com/openjdk/jmc '')

## jmc安装

jmc依赖的jdk版本可能跟现在电脑上面的版本不一致，这种情况就需要指定jmc启动的jdk版本
找到文件`Eclipse/jmc.ini`
在文件的最上面添加下面的配置
```ini
-vm
/Users/admin/Workspace/soft/jdk-11.0.11.jdk/Contents/Home/bin
```

## 使用方式

先查询jmc的版本
```
jmc -version
```

[寻找对应版本的JMC文档](https://docs.oracle.com/en/java/java-components/jdk-mission-control/ '')

开启JFR
```shell
# jdk8的启动方式
java -XX:+UnlockCommercialFeatures -XX:+FlightRecorder -XX:StartFlightRecording=duration=60s,filename=myrecording.jfr MyApp
# 不想指定记录的时间，也可以用下面的方式 jvm进程退出的时候才会转存到文件中
java -XX:+UnlockCommercialFeatures -XX:+FlightRecorder -XX:StartFlightRecording=dumponexit=true,filename=mytestrecording.jfr MyApp
```


https://www.baeldung.com/java-flight-recorder-monitoring