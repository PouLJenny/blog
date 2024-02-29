# 服务启动预热

## java8的参数
- https://www.zybuluo.com/changedi/note/975529

## tomcat启动加速
- -Djava.security.egd=file:/dev/./urandom

## JVM预热
- -XX:CompileThreshold=invocations
    编译前解释型方法调用次数。设置这个值，在编译前，会用解释器执行方法若干次用于收集信息，从而可以更高效率的进行编译。默认这个值在JIT中是10000次。可以通过使用-Xcomp参数来禁止编译时的解释执行。

- 