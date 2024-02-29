# Gradle

## 官网
https://gradle.org/

官方文档的安装教程很详细，建议看官方的


### 通过gradle自带的脚手架搭建项目

gradle help --task :init 查看init可以执行的参数
gradle init --type java-application 初始化java的项目
https://spring.io/guides/gs/rest-service/   springboot官方给的搭建springboot的参考案例
https://docs.spring.io/spring-boot/docs/current/gradle-plugin/reference/html/  springboot gradle插件官方参考指南

### gradle参数的优先级
- 命令行
- System properties 例如：  systemProp.http.proxyHost=somehost.orgs 在gradle.properties文件中
- Gradle properties
- Environment variables 
- Project properties
	
idea中编译gradle项目  无法编译src/main/java目录下的xml文件
在build配置文件中 加上sourceSets.main.resources.srcDirs = ["src/main/java","src/main/resources"]  可解决此问题

### 加速依赖
`build.gradle`文件中添加配置，加速jar包的导入
```
buildscript {
  repositories {
    mavenLocal()
    maven { url 'https://maven.aliyun.com/repository/central' }
    maven { url 'https://maven.aliyun.com/repository/jcenter' }
    maven { url 'https://maven.aliyun.com/repository/google' }
    maven { url 'https://maven.aliyun.com/repository/gradle-plugin' }
    mavenCentral()
  }
}
allprojects{
    repositories {
            mavenLocal()
            maven { url 'https://maven.aliyun.com/repository/central' }
            maven { url 'https://maven.aliyun.com/repository/jcenter' }
            maven { url 'https://maven.aliyun.com/repository/google' }
            maven { url 'https://maven.aliyun.com/repository/gradle-plugin' }
            mavenCentral()
    }
}
```
 
