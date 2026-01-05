# LLVM

[官网](https://llvm.org/)
[github](https://github.com/llvm/llvm-project)



## 编译 18.1.8版本 clang和lld

```shell
## 安装gcc14
sudo pacman -S gcc14

/opt/cmake-3.20.6-linux-x86_64/bin/cmake -G Ninja ../llvm \
  -DCMAKE_BUILD_TYPE=Release \
  -DPython3_EXECUTABLE=/usr/bin/python3 \
  -DCMAKE_INSTALL_PREFIX=/opt/llvm/18 \
  -DCMAKE_C_COMPILER=gcc-14 \
  -DCMAKE_CXX_COMPILER=g++-14 \
  \
  -DLLVM_ENABLE_PROJECTS="clang;lld" \
  -DLLVM_ENABLE_RUNTIMES="" \
  -DLLVM_INCLUDE_TESTS=OFF \
  -DLLVM_BUILD_TESTS=OFF \
  \
  -DLLVM_TARGETS_TO_BUILD="X86;AArch64" \
  \
  -DLLVM_ENABLE_RTTI=ON \
  -DLLVM_ENABLE_EH=ON

ninja

sudo ninja install
```





