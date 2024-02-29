jenkins 安装使用

1. 安装环境
    
    1.	Contos 7
    2.	Jinkens 2.89.2 
    3.	Jdk 1.8.0_151
    4.	Tomcat 8.5.16
    5.	Maven 3.5.2
    6.	Git 1.8.3.1
    7.	Gradle 4.4.1
    
2. 下载jenkins的 war包 
    网址： https://jenkins.io/download/

3. 将下载的Jenkins.war 放到tomcat的webapps目录下 （${TOMCAT_BASE}/webapps/）

4. 启动tomcat  默认项目路径 jenkins  默认工作空间 /root/.jenkins/
   可以在tomcat的启动日志里找到jenkins的初始登陆密码，或者查看文件/root/.jenkins/initialAdminPassword
   
5. 浏览器访问Jenkins控制台 输入密码 建议选择安装官方推荐插件

6. 创建管理员用户 密码

7. 进入系统管理-》全局工具配置   分别配置 maven jdk  git gradle

8. 返回Jenkins主控制台 点击新建-》构建一个自由风格的软件项目
   
   点击确定
   general    =》 可选择参数化构建过程 在下边的配置中使用  
   源码管理   =》 Repository URL： 添加git源码地址  Credentials：添加git账号密码  Branch Specifier (blank for 'any')：填写需要构建的分支
   构建触发器 =》 设置构建的触发动作 此处暂时不设置
   构建环境   =》 设置jenkins的构建环境 此处暂不设置
   构建       =》 增加构建步骤-> Invoke Gradle Script 选择gradle版本  然后 填写gradle执行的task  此处我填写clean build
                  增加构建步骤-> Conditional Steps(multiple)  Run? : Current build status    
                                                              Worst status和Best status 都选择success
                                                              On evaluation failure 选择 Fail The build
                                                              Steps to run if condition is met : 选择Execute shell  写入复制构建成功的文件到远程服务器的命令
   构建后操作 =》 可添加E-mail Notification   填写正确的email地址
        
9. 保存配置后，点击立即构建 或 Build with Parameters