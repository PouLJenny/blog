# Linux源码阅读

## 下载源码

[网址](https://www.kernel.org/ )


## 源码目录结构

```lua
linux-5.10/
|-- arch/            # 架构相关代码
|   |-- arm/
|   |-- x86/
|   |-- ...
|-- block/           # 块设备子系统
|-- crypto/          # 加密子系统
|-- Documentation/   # 文档
|-- drivers/         # 驱动程序
|   |-- block/
|   |-- net/
|   |-- ...
|-- fs/              # 文件系统
|   |-- ext4/
|   |-- ntfs/
|   |-- ...
|-- include/         # 头文件
|   |-- asm/
|   |-- linux/
|-- ipc/             # 进程间通信子系统
|-- kernel/          # 内核核心代码
|-- lib/             # 通用库函数
|-- mm/              # 内存管理子系统
|-- net/             # 网络子系统
|-- samples/         # 示例代码
|-- scripts/         # 构建和辅助脚本
|-- security/        # 安全子系统
|-- sound/           # 声音子系统
|-- tools/           # 工具
|-- usr/             # 用户空间工具和库
|-- virt/            # 虚拟化子系统
|-- ...              # 其他目录

```