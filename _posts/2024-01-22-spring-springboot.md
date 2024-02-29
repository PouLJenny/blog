---
layout: post
title:  "Spring Boot 整体架构"
date:   2024-01-22 10:00:00 +0800
categories: spring springboot
tags: spring springboot
permalink: /spring/springboot
published: true
publish_file: 2024-01-22-spring-springboot.md
toc: true
---
# Spring boot

## 如何启动Jar包的

Spring boot项目打包之后，就是一个单独的jar包，执行的时候直接运行命令`java -jar application.jar`,那么如此简洁的启动流程背后是如何做到的呢?

1. 首先先看一下jar包解压后是什么样子的
```shell
drwxr-xr-x@  6 poul  staff   192B  2  4 10:04 BOOT-INF/
drwxr-xr-x@  5 poul  staff   160B  2  4 10:04 META-INF/
drwxr-xr-x@  3 poul  staff    96B  2  1  1980 org/
```
java本身的机制启动一个jar包的时候，可以通过命令的方式执行一个启动类
```shell
java -cp myjar.jar com.example.MainClass
```

还有一种方式是直接读取jar包中的配置文件`META-INF/MANIFEST.MF`,获取启动类信息，我们查看springboot jar包中的配置文件:
```conf
Manifest-Version: 1.0
Created-By: Maven JAR Plugin 3.3.0
Build-Jdk-Spec: 21
Implementation-Title: spring-boot-test
Implementation-Version: 0.0.1-SNAPSHOT
Main-Class: org.springframework.boot.loader.launch.JarLauncher
Start-Class: com.peng.test.springboottest.SpringBootTestApplication
Spring-Boot-Version: 3.2.2
Spring-Boot-Classes: BOOT-INF/classes/
Spring-Boot-Lib: BOOT-INF/lib/
Spring-Boot-Classpath-Index: BOOT-INF/classpath.idx
Spring-Boot-Layers-Index: BOOT-INF/layers.idx
```
可以看到文件中声明了启动类`org.springframework.boot.loader.launch.JarLauncher`
此类对应的jar包为
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-loader</artifactId>
</dependency>
```
这个类就在刚开始我们看到的jar包解压文件中的`org/`目录,确切的说是上面的整个jar包里面的类。把这个jar包的源码放到项目的`pom.xml`文件中，把源码下载下来。可以看到这个类的源码还是比较简单的
```java

package org.springframework.boot.loader.launch;

/**
 * {@link Launcher} for JAR based archives. This launcher assumes that dependency jars are
 * included inside a {@code /BOOT-INF/lib} directory and that application classes are
 * included inside a {@code /BOOT-INF/classes} directory.
 *
 * @author Phillip Webb
 * @author Andy Wilkinson
 * @author Madhura Bhave
 * @author Scott Frederick
 * @since 3.2.0
 */
public class JarLauncher extends ExecutableArchiveLauncher {

	public JarLauncher() throws Exception {
	}

	protected JarLauncher(Archive archive) throws Exception {
		super(archive);
	}

	@Override
	protected boolean isIncludedOnClassPath(Archive.Entry entry) {
		return isLibraryFileOrClassesDirectory(entry);
	}

	@Override
	protected String getEntryPathPrefix() {
		return "BOOT-INF/";
	}

	static boolean isLibraryFileOrClassesDirectory(Archive.Entry entry) {
		String name = entry.name();
		if (entry.isDirectory()) {
			return name.equals("BOOT-INF/classes/");
		}
		return name.startsWith("BOOT-INF/lib/");
	}

	public static void main(String[] args) throws Exception {
		new JarLauncher().launch(args);
	}

}
```
根据jar包的协议，`java -jar` 启动的时候，会执行声明的类`Main-Class: org.springframework.boot.loader.launch.JarLauncher`的`main`方法,然后，再根据springboot的协议,再执行声明的类`Start-Class: com.peng.test.springboottest.SpringBootTestApplication`的`main`方法,其中目录`BOOT-INF/lib/`是程序依赖的jar包，目录`BOOT-INF/classes/`是项目代码





## 启动流程

1. `SpringApplication.run(Application.class, args);`
    1. 创建`Startup`
    1. 构建`SpringApplication`
        1. 根据jvm已经加载的类来判断当前应用的类型 `WebApplicationType`，有REACTIVE,NONE,SERVLET
        1. 扫描加载所有jar包中的`META-INF/spring.factories`文件中的扩展点 ,`SpringFactoriesLoader.load`方法，如果加载的类实现了`PriorityOrdered`并进行排序
            1. `BootstrapRegistryInitializer` 
                1. 具体的排序方式， 实现了`PriorityOrdered`接口的类排在没有实现`PriorityOrdered`的类前面，实现了`Ordered`接口的进行排序，上面提到的两个接口都没实现的排在最后面（并不能保证这部分的顺序）
            1. `ApplicationContextInitializer` 
            1. `ApplicationListener`
        1. 识别主类，带`main`方法的类
    1. 执行`run`方法,参数为`args`
        1. 创建`DefaultBootstrapContext` 
            1. 执行所有`BootstrapRegistryInitializer`类的`initialize`方法
        1. 从所有`spring.factories`中获取声明的类`SpringApplicationRunListener`,并传入启动类的`String[] args`参数
            1. spring-boot包中的类`org.springframework.boot.context.event.EventPublishingRunListener`order为`0`
        1. 触发`SpringApplicationRunListener.starting`方法
        1. 准备环境, 生成类`ConfigurableEnvironment`
            1. `spring.factories`文件中寻找`ApplicationContextFactory`，创建`ApplicationServletEnvironment`
        1. 配置环境
            1. 启动命令中的启动参数，加载到`ConfigurableEnvironment`的第一个`PropertySource`
            1. 第一个`PropertySource`转换成`environment`
            1. 触发`SpringApplicationRunListener.environmentPrepared`方法
            1. 移动`defaultProperties`到`MutablePropertySources`的最后面
        1. 打印banner
        1. 创建`ConfigurableApplicationContext`，这个应该就是spring的bean容器
            1. 实例化类`AnnotationConfigServletWebServerApplicationContext`
                1. 创建对象`AnnotatedBeanDefinitionReader`
                    1. `AnnotationConfigUtils.registerAnnotationConfigProcessors`方法给spring容器中注入5个bean，分别为
                        1. ConfigurationClassPostProcessor
                        1. AutowiredAnnotationBeanPostProcessor
                        1. CommonAnnotationBeanPostProcessor
                        1. EventListenerMethodProcessor
                        1. DefaultEventListenerFactory
                1. 创建对象`ClassPathBeanDefinitionScanner`
        1. `AnnotationConfigServletWebServerApplicationContext` 设置 `Startup`
        1. `prepareContext`
            1. `AnnotationConfigServletWebServerApplicationContext`设置`ConfigurableEnvironment`
            1. `postProcessApplicationContext`
                1. `AnnotationConfigServletWebServerApplicationContext`设置`Conversion`
            1. 触发所有`ApplicationContextInitializer`的`initialize`方法
            1. 触发`SpringApplicationRunListener.contextPrepared`方法
            1. 把*启动类*注入到spring容器中
        1. `refreshContext` 这个方法是大头，最最最重要的方法
            1. 调用方法`prepareRefresh` 准备环境
            1. 调用方法`prepareBeanFactory`
            1. 调用方法`postProcessBeanFactory`
            1. 调用方法`invokeBeanFactoryPostProcessors`, **重要方法**, Invoke factory processors registered as beans in the context. 扫描整个项目把所有生命的bean注入到spring容器中
                1. 执行`PostProcessorRegistrationDelegate.invokeBeanFactoryPostProcessors`
                    1. 按顺序执行`BeanDefinitionRegistryPostProcessor`的方法`postProcessBeanDefinitionRegistry` 
                        1. 最重要的Processor: `ConfigurationClassPostProcessor`
                        1. `org.springframework.context.annotation.ConfigurationClassPostProcessor#processConfigBeanDefinitions`
                        1. 由于启动类添加了`SpringBootApplicaton`注解，解析的时候会从这个类开始,如果注解中没有制定扫描的包路径，**则自动使用当前启动类的包路径**
                        1. `org.springframework.context.annotation.ConfigurationClassParser.DeferredImportSelectorHandler#process` 重要的解析方法,会解析除了本身项目的其它依赖jar包中的类
                            1. `ImportCandidates`类中加载所有jar及项目中的 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 文件，并获取文件中的类，这些类都是`AutoConfiguration`的类，为了下一步执行自动配置。读取文件方式是通过`java.lang.ClassLoader#getResources`方法定位所有文件的
                            1. 触发所有的类`AutoConfigurationImportListener`,消息事件为`AutoConfigurationImportEvent`
                                1. 触发方式，`org.springframework.core.io.support.SpringFactoriesLoader#loadFactories` 通过此方法，获取所有文件`META-INF/spring.factories`中声明的类`AutoConfigurationImportListener`并触发
                            1. 处理所有的`AutoConfiguration`类 `org.springframework.context.annotation.ConfigurationClassParser#doProcessConfigurationClass`
                            1. 将所有的配置类解析成`ConfigurationClass`
                    1. 触发`BeanDefinitionRegistry`的方法``
            1. 调用方法`onRefresh` ， 初始化一些特殊的bean和特殊的上下文子类
                1. 生成并启动`WebServer`
        1. `afterRefresh`
## 如何实现的自动装配机制

## 问题

springboot的代码相当的庞大，怎么才能快速的掌握核心的逻辑呢？？
抓大放小

切分任务大小，使目标更简单的完成，快速获得完成任务的成就感。
比如：
### sprinboot中的tomcat是怎么启动的

1. 关键类
    1. `WebServer`,代表web服务的抽象接口，相关的实现类有:
        1. `JettyWebServer`
        1. `NettyWebServer`
        1. `TomcatWebServer`, tomcat是我们关注的重点
        1. `UndertowWebServer`
        1. `UndertowServletWebServer`
    1. `WebServerFactory`的继承接口`ServletWebServerFactory`，生成`WebServer`类的工厂接口,实现类有：
        1. `JettyServletWebServerFactory`
        1. `TomcatServletWebServerFactory` 是我们关注的重点
        1. `UndertowServletWebServerFactory` 
    1. 综上可以看到这里用到的是工厂方法模式(factory method)

1. 触发启动的流程
    1. 从整体的启动流程里面能看出来，是在`refreshContext`阶段的`onRefresh`方法中触发启动的tomcat

随之而来的又一个问题:

### SpringBoot是怎么自动装配Bean而省去Xml的
换句话说，springboot是怎么自动注入bean的

1. 启动类
