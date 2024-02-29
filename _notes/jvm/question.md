# JVM问题总结

## 线上程序 堆外内存溢出
https://www.cnblogs.com/wakey/p/13185935.html
https://www.kancloud.cn/alex_wsc/javajvm/1844985 (很棒)
https://www.cnblogs.com/rude3knife/p/13570423.html （这个也挺好）
https://www.programmerall.com/article/9702982354/ 怎么读取gdb dump下来的内存块

https://www.baeldung.com/native-memory-tracking-in-jvm  // TODO

top 然后 shift+m 查看哪个进程占用内存高

pmap -x 1394  | sort -n -k3  | less

cat /proc/1394/maps | grep fdfb8000000-

gdb --batch --pid 1394 -ex "dump memory a.dump 0x7fdfb8000000 0x7fdfbc000000"

strings -10 a.dump

perf record -g -p 1394

perf report -i perf.data

## CPU飙升问题定位

https://blog.csdn.net/crazymakercircle/article/details/128805374?spm=1000.2115.3001.6382&utm_medium=distribute.pc_feed_v2.none-task-blog-personrec_tag-7-128805374-null-null.pc_personrec&depth_1-utm_source=distribute.pc_feed_v2.none-task-blog-personrec_tag-7-128805374-null-null.pc_personrec