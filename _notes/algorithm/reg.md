# 正则表达式

## 简介 

[参考博客](https://blog.csdn.net/duxingxia356/article/details/40856167 '')


## 常用的正则表达式

- [手机号码](https://learnku.com/articles/31543 '')
- [邮箱](https://blog.csdn.net/make164492212/article/details/51656638 '')  
  [其它](http://jregex.sourceforge.net/examples-email.html '')
- [身份证号码](https://segmentfault.com/a/1190000016696368 '') 


## 正则匹配算法

- DFA确定有限状态自动机
- NFA非确定有限状态自动机
- Thompson NFA

[好的博客](https://blog.csdn.net/kingoverthecloud/article/details/41621557 '')


各种软件的实现方案
| Engine type | Programs |
|  ----  | ----  |
|DFA|awk (most versions), egr ep (most versions), flex, lex, MySQL, Procmail|
|Traditional NFA|GNU Emacs, Java, grep (most versions), less, more, .NET languages, PCRE library, Perl, PHP (all three regex suites), Python, Ruby,sed (most versions), vi|
|POSIX NFA|mawk, Mortice Kern Systems’ utilities, GNU Emacs (when requested)|
|Hybrid NFA/DFA|GNU awk, GNU grep /egrep, Tcl|





## 字符匹配算法

## 暴力匹配

### 利用有限自动机进行字符串匹配

有限自动机 M 是一个5元组 (Q,q0,A,$\Sigma$,$\delta$)

- Q是状态的有限集合
- q0 $\in$ Q 是初始状态
- A $\subseteq$ Q 是一个特殊的接受状态集合
- $\Sigma$ 是有限输入字母表
- $\delta$ 是一个从 Q $\times$ $\delta$ 到Q的函数，称为 M的转移函数


## 链接

- [正则表达式工具网站](https://regexlib.com/ '')
- [好的博客](https://www.cnblogs.com/Renyi-Fan/p/9694695.html#_label4)