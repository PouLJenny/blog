# Linux源码阅读

当前源码基于版本`6.15.9`来的


## 下载源码

[网址](https://www.kernel.org/ )


## 源码目录结构

```shell
linux-6.15.9/
├── arch/          —— 处理器架构代码
│   ├── x86/       —— x86 架构相关（启动、汇编、CPU）
│   ├── arm/       —— ARM 架构代码
│   ├── arm64/     —— 64位 ARM
│   ├── riscv/     —— RISC-V 架构
│   └── ...        —— 其他架构
│
├── drivers/       —— 设备驱动
│   ├── net/       —— 网络设备驱动
│   ├── usb/       —— USB 设备驱动
│   ├── gpu/       —— 显卡驱动
│   ├── sound/     —— 声卡驱动
│   ├── pci/       —— PCI 总线相关驱动
│   ├── mmc/       —— 多媒体卡驱动
│   ├── input/     —— 输入设备驱动
│   └── ...        —— 其他驱动
│
├── fs/            —— 文件系统
│   ├── ext4/      —— ext4 文件系统实现
│   ├── nfs/       —— 网络文件系统
│   ├── btrfs/     —— Btrfs 文件系统
│   ├── xfs/       —— XFS 文件系统
│   ├── proc/      —— /proc 虚拟文件系统
│   └── tmpfs/     —— 临时文件系统
│
├── net/           —— 网络子系统
│   ├── ipv4/      —— IPv4 协议
│   ├── ipv6/      —— IPv6 协议
│   ├── core/      —— 网络核心协议栈
│   ├── ethernet/  —— 以太网支持
│   ├── wireless/  —— 无线网络
│   └── netfilter/ —— 防火墙和包过滤
│
├── mm/            —— 内存管理
│   ├── slab/      —— slab 分配器
│   ├── page_alloc/—— 页分配器
│   ├── transparent_hugepage/ —— 大页支持
│   ├── hugetlbpage/—— HugeTLB 支持
│   └── mprotect/  —— 内存保护
│
├── kernel/        —— 核心内核功能
│   ├── sched/     —— 调度器
│   ├── signals/   —— 信号处理
│   ├── locking/   —— 同步机制
│   ├── printk/    —— 内核打印
│   └── panic/     —— 异常处理
│
├── crypto/        —— 加密子系统
├── Documentation/ —— 文档
├── include/       —— 公共头文件
├── init/          —— 启动和初始化
├── ipc/           —— 进程间通信
├── lib/           —— 库函数
├── samples/       —— 示例代码
├── scripts/       —— 构建脚本
├── security/      —— 安全模块
├── sound/         —— 音频子系统
├── tools/         —— 用户空间工具
├── usr/           —— 用户空间镜像相关
└── virt/          —— 虚拟化子系统

```

## System Call 

### 入口

1. 搜索`SYSCALL_DEFINE`，这是system call的宏定义，可以直接定位到代码的入口，推荐用这个
2. `syscall_64.tbl` 文件中列举了所有的system call，有一个整体的认识, 里面列举的system call方法，前面再加上`__` 就是源代码中的方法。

# EOF