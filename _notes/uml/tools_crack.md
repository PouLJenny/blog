# 常用工具破解教程

## star UML
### mac 系统下的破解方式

- 安装npm

    ` brew install node `
- 安装 asar

    ` npm install asar -g `
- 进入目录，解压文件app.asar

    `cd /Applications/StarUML.app/Contents/Resources/`
    `asar extract app.asar app`
    

    > 如果系统提示没有权限可以通过下面的方式来修改配置：
    > 系统设置 -> 隐私与安全性 -> App管理
    > 中把iTerm或者是其他的终端程序给打开即可。

- 修改新生成的app目录下的lisence文件

    `vim app/src/engine/license-manager.js `
- 找到 checkLicenseValidity()函数，大概是125行开始的，原代码：

    ```js
    checkLicenseValidity () {
        this.validate().then(() => {
            setStatus(this, true)
        }, () => {
            setStatus(this, false)
            UnregisteredDialog.showDialog()
    })
    ```
    改成
    ```js
    checkLicenseValidity () {
        this.validate().then(() => {
            setStatus(this, true)
        }, () => {
            setStatus(this, true)
        })
    }
    ```
- 打包覆盖原app.asar
  `asar pack app app.asar  `
  
这样就可以了！

不过有能力的同学还是尽量支持下正版。

[官网链接](https://staruml.io/ )
