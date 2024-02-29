# 查看java的实际执行的汇编代码

## hsdis
https://blogs.oracle.com/javamagazine/post/java-hotspot-hsdis-disassembler

1. 从这个网站[下载](https://chriswhocodes.com/hsdis/ )对应CPU的hsdis文件
2. 把文件 `hsdis-amd64.so` 放在 `/usr/lib64/`下面
3. `java -XX:+UnlockDiagnosticVMOptions -XX:+PrintAssembly -Xcomp  -XX:LogFile=hotspot.log -XX:+LogCompilation  -XX:CompileCommand=compileonly,*Volatile.incrementV Volatile`

`java -XX:+UnlockDiagnosticVMOptions -XX:+PrintAssembly -Xcomp  -XX:CompileCommand=compileonly,*Volatile.incrementV Volatile | less` 这种方式其实就很明白了
4. 

`-XX:+UnlockDiagnosticVMOptions`：解锁用于 JVM 诊断的选项。
`-XX:+PrintAssembly`：配合反汇编插件（例如 hsdis-amd64.os）可以打印出字节码和本地方法的汇编码；必须和 `-XX:+UnlockDiagnosticVMOptions` 一起使用。
`-Xcomp`：在第一次调用时强制编译方法。默认情况下，无论是 -client 模式还是 -server 模式，都需要执行一定次数解释方法的调用才会触发方法的编译。（如果需要 JIT 日志，则不指定该参数）
`-XX:CompileCommand=compileonly,*ClassName.methodName`：只编译类名为 ClassName 中的 methodName 方法，支持使用 * 作为通配符。可以多次指定 -XX:CompileCommand 添加多条命令。（建议只指定需要的方法，否则将会产生大量的无关日志）
`-XX:+LogCompilation`：允许将编译活动记录到当前工作目录中名为 hotspot.log 的文件中。可以通过 -XX:LogFile 指定文件的路径和名字。
`-XX:LogFile=path`：指定日志的路径和文件名。例如：-XX:LogFile=/var/log/hotspot.log

5. 通过 jitwatch 工具优雅的查看汇编日志
https://github.com/AdoptOpenJDK/jitwatch

`mvn clean compile test exec:java`
碰到了jitwatch界面乱码的问题，这个地方需要使用jdk17版本，

## CPU指令集和架构
[amd指令集](https://www.amd.com/system/files/TechDocs/40332.pdf )
[intel指令集](https://www.intel.cn/content/www/cn/zh/developer/articles/technical/intel-sdm.html )