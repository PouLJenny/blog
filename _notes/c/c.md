# C语言学习

[wiki](https://en.wikipedia.org/wiki/The_C_Programming_Language '')

结构化编程

## History

Ken Thompson 
Dennis Ritchie

- 1969 K 用汇编语言写了UNIX系统
- 1969 K 设计了B语言，衍生自 BCPL
- 1970 K & R 用B语言重写的UNIX
- 1971 R 在B语言的基础上设计了NB（New B）语言，后来改名为C
- 1973 K & R 用C语言重写的UNIX系统
- 1978 K & R 出版了书 The C Programming Language
- C89/C90 C标准的定制工作交给了ISO来处理
- C99
- C11
- C17
- C2x

## 数据类型
C语言的基本数据类型及其所占内存可以根据C语言标准来确定。下面是C语言中常见的基本数据类型及其所占内存的典型大小（**取决于具体的编译器和操作系统**）：

**整型类型（整数类型）**：

- char：1字节
- unsigned char：1字节
- short：2字节
- unsigned short：2字节
- int：通常为4字节（32位系统）或8字节（64位系统）
- unsigned int：通常为4字节（32位系统）或8字节（64位系统）
- long：4字节（32位系统）或8字节（64位系统）
- unsigned long：4字节（32位系统）或8字节（64位系统）
- long long：8字节
- unsigned long long：8字节

**浮点类型**：

- float：4字节
- double：8字节
- long double：通常为8字节或16字节

**指针类型**：

指针的大小取决于系统的位数，通常为4字节（32位系统）或8字节（64位系统）
枚举类型：


通常和int类型具有相同的大小，即4字节（32位系统）或8字节（64位系统）
需要注意的是，这些大小是典型值，实际的大小可能因编译器、操作系统和平台的不同而有所变化。可以使用sizeof运算符来获取在特定系统上的数据类型大小。

另外，还有一些修饰符（如`signed`、`unsigned`、`short`、`long`等）可以与基本数据类型结合使用，来表示不同的取值范围和符号性质。这些修饰符的具体含义也可能因编译器和操作系统的不同而有所变化。

## GNU C Library
C的源码实现

[官网](https://sourceware.org/glibc/libc.html)

下载源码
```shell
git clone https://sourceware.org/git/glibc.git
cd glibc
git checkout release/2.41/master
```

源码结构
```shell
glibc-2.41/
├── elf/                      # ELF 相关代码，动态链接器 ld.so 及启动代码
├── elf/ldso/                 # 动态链接器实现
├── malloc/                   # 内存分配器实现（malloc/free/realloc 等）
├── math/                     # 数学库函数（sin, cos, exp 等）
├── nptl/                     # Native POSIX Thread Library（POSIX 线程实现）
├── stdio-common/             # 标准输入输出库通用代码（printf, scanf 等核心实现）
├── string/                   # 字符串和内存操作函数（memcpy, strcpy, strcmp 等）
├── sysdeps/                  # 系统依赖代码，按平台/架构区分
│   ├── unix/                 # Unix-like 系统实现
│   │   ├── sysv/             # System V 风格 Unix 实现
│   │   │   ├── linux/        # Linux 特有系统调用和功能封装（syscall 等）
│   │   │   └── ...           # 其他 SysV Unix 相关目录
│   │   ├── freebsd/          # FreeBSD 相关实现
│   │   ├── solaris/          # Solaris 相关实现
│   │   └── ...               # 其他 Unix-like 系统
│   ├── win32/                # Windows 平台实现（极少用）
│   └── include/              # 系统相关头文件（平台相关的定义）
├── iconv/                    # 字符编码转换库实现（iconv 相关）
├── locale/                   # 本地化和国际化支持（语言环境等）
├── posix/                    # POSIX 标准相关代码（部分系统调用封装）
├── rt/                       # 实时扩展库实现（POSIX realtime 扩展）
├── sysdeps/posix/            # POSIX 标准相关实现（系统依赖）
├── dns/                      # DNS 解析相关实现
├── gnulib/                   # GNU 通用库辅助代码（复用功能）
├── tests/                    # 单元测试和测试工具
└── misc/                     # 其他杂项代码
```

### 编译源码方便查看源码

```shell
mkdir build && cd build
mkdir install

../configure --prefix=$(pwd)/install
make -j$(nproc)
make install
```

### VSCode 查看源码

为了方便查看源码，防止点击跳转源码的时候跑到系统自带的gcc上去，需要简单做个配置,添加配置文件`.vscode/c_cpp_properties.json`
```json
{
    "configurations": [
        {
            "name": "Linux",
            "compilerPath": "/usr/bin/gcc",
            "includePath": [
                "${workspaceFolder}/include",
                // "${workspaceFolder}/build/install/include",
                "${workspaceFolder}/sysdeps/*"
            ],
            "cStandard": "c11",
            "cppStandard": "c++17",
            "intelliSenseMode": "gcc-x64"
        }
    ],
    "version": 4
}
```



## `__attribute__ ((__packed__))`

在C语言中，`__attribute__ ((__packed__))`是GCC编译器提供的一个特殊属性（attribute）。这个属性用于告诉编译器以最小的内存对齐方式来对结构体或联合体进行内存布局，即取消对结构体或联合体进行默认的对齐操作。

在默认情况下，编译器会根据平台和数据类型的大小进行内存对齐操作，以提高内存访问的效率。这意味着结构体或联合体的成员可能会在内存中存在填充字节，以满足对齐的要求。而使用`__attribute__ ((__packed__))`属性可以取消这种对齐，让结构体或联合体的成员按照其声明的顺序连续存储，减少内存的浪费。

使用`__attribute__ ((__packed__))`的语法示例：
```c
struct __attribute__((__packed__)) MyStruct {
    int a;
    char b;
    short c;
};
```
在上面的示例中，MyStruct结构体的成员将按照声明的顺序连续存储，没有额外的填充字节。

需要注意的是，使用`__attribute__ ((__packed__))`可能会导致性能下降，因为无对齐的内存访问可能会导致效率降低。此外，该属性是GCC编译器特有的，并不属于C语言标准的一部分，因此在使用时需要注意编译器的兼容性。

## 书

- C程序设计语言 The C programming language 
- C Programming, A Modern Approach [配套的网站](http://knking.com/books/c2/programs/index.html '')


# EOF
