# GNU project debugger

[官网](https://www.sourceware.org/gdb/ '')

## mac的权限问题

https://sourceware.org/gdb/wiki/PermissionsDarwin#Create_a_certificate_in_the_System_Keychain

而且创建正式的时候会报未知错误
通过下面的方式解决
https://www.pianshen.com/article/5485970358/


## 常用的命令
step over: 在单步执行时，在函数内遇到子函数时不会进入子函数内单步执行，而是将子函数整个执行完再停止，也就是把子函数整个作为一步。有一点,经过我们简单的调试,在不存在子函数的情况下是和step into效果一样的（简而言之，越过子函数，但子函数会执行）
step into: 单步执行，遇到子函数就进入并且继续单步执行（简而言之，进入子函数）；
step out: 当单步执行到子函数内时，用step out就可以执行完子函数余下部分，并返回到上一层函数。