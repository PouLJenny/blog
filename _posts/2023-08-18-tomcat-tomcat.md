---
layout: post
title:  "tomcat 整体架构"
date:   2023-08-18 18:01:09  +0800
categories: tomcat
tags: tomcat
permalink: /tomcat/tomcat
published: true
publish_file: 2023-08-18-tomcat-tomcat.md
toc: true
---

# Tomcat


[官网](https://tomcat.apache.org/ )
[github](https://github.com/apache/tomcat )
[官方文档](https://tomcat.apache.org/tomcat-9.0-doc/introduction.html )
[架构博客](https://github.com/heibaiying/Full-Stack-Notes/blob/master/notes/Tomcat_%E6%9E%B6%E6%9E%84%E8%A7%A3%E6%9E%90.md )

## 概念

### CATALINA_HOME & CATALINA_BASE
tomcat中有两个比较重要的概念
**CATALINA_HOME**: Represents the root of your Tomcat installation, for example `/home/tomcat/apache-tomcat-9.0.10` or `C:\Program Files\apache-tomcat-9.0.10`
**CATALINA_BASE**: Represents the root of a runtime configuration of a specific Tomcat instance. If you want to have multiple Tomcat instances on one machine, use the `CATALINA_BASE` property

If you set the properties to different locations, the `CATALINA_HOME` location contains static sources, such as `.jar` files, or binary files. The `CATALINA_BASE` location contains configuration files, log files, deployed applications, and other runtime requirements.

### 为什么要区分这两个概念 CATALINA_HOME & CATALINA_BASE
By default, `CATALINA_HOME` and `CATALINA_BASE` point to the same directory. Set `CATALINA_BASE` manually when you require running multiple Tomcat instances on one machine. Doing so provides the following benefits:

Easier management of upgrading to a newer version of Tomcat. Because all instances with single `CATALINA_HOME` location share one set of `.jar `files and binary files, you can easily upgrade the files to newer version and have the change propagated to all Tomcat instances using the same `CATALIA_HOME` directory.
Avoiding duplication of the same static `.jar` files.
The possibility to share certain settings, for example the setenv shell or bat script file (depending on your operating system).

### 怎么使用 CATALINA_BASE
The `CATALINA_BASE` property is an environment variable. You can set it before you execute the Tomcat start script, for example:

On Unix: `CATALINA_BASE=/tmp/tomcat_base1 bin/catalina.sh start`
On Windows: `CATALINA_BASE=C:\tomcat_base1 bin/catalina.bat start`


## Tomcat 架构

**Server**: 表示整个Servlet容器，在整个Tomcat运行环境中只有唯一一个Server实例，一个Server包含多个Service，每个Service互相独立，但共享一个JVM以及系统类库
**Service**: 一个Service负责维护多个Connector和一个Engine，其中Connector负责开启Socket并监听客户端请求，返回响应数据；Engine负责具体的请求处理
**Connector**:连接器，用于监听并转换来自客户端Socke请求，然后将Socket请求交由，Container处理，支持不同协议以及不同的I/O方式，
**Engine**: 表示整个Servlet引擎，在Tomcat中，Engine为最高层级的容器对象
**Host**: 表示Engine中的虚拟机，通常与一个服务器的网络名有关，如域名等
**Context**: 表示ServletContext，在Servlet规范中，一个ServletContext表示一个独立的web应用
**Wrapper**: 是对标准Servlet的封装


### Connector
主要功能就是将Socket的输入转换为Request对象,并交由容器进行处理；之后再将容器处理完成的Response对象写入到输出流。

####  ProtocolHandler
 
##### EndPoint

### 类加载机制

![](/assets/notes/tomcat/class-loaders.svg )


#### Common Class Loader
位于Tomcat架构顶层的公用类加载器，父加载器为Java的`Application Class Loader`,默认读取`conf/catalina.properties`配置文件中的`common.loader`属性，默认值为：`${catalina.base}/lib","${catalina.base}/lib/*.jar","${catalina.home}/lib","${catalina.home}/lib/*.jar`

#### Catalina Class Loader
以`Common Class Loader`为父加载器，用于加载tomcat应用服务器的类加载器，默认读取`conf/catalina.properties`配置文件中的`server.loader`属性，默认值为空

#### Shared Class Loader
以`Common Class Loader`为父加载器，所有Web应用的父类加载器，默认读取`conf/catalina.properties`配置文件中的`shared.loader`属性，默认值为空


#### Webapp Class Loader

以`Shared Class Loader`为父加载器，加载`/WEB-INF/classes`目录下的Class文件和资源，`/WEB-INF/lib`目录下的jar包文件，只对当前web应用可见

这级别的ClassLoader对应的类为`org.apache.catalina.loader.WebappClassLoaderBase`重写了`loadClass`方法，破坏了java中的“**双亲委派模型**”

```java
    public Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {

        synchronized (JreCompat.isGraalAvailable() ? this : getClassLoadingLock(name)) {
            if (log.isDebugEnabled()) {
                log.debug("loadClass(" + name + ", " + resolve + ")");
            }
            Class<?> clazz = null;

            // Log access to stopped class loader
            checkStateForClassLoading(name);

            // (0) Check our previously loaded local class cache
            clazz = findLoadedClass0(name);
            if (clazz != null) {
                if (log.isDebugEnabled()) {
                    log.debug("  Returning class from cache");
                }
                if (resolve) {
                    resolveClass(clazz);
                }
                return clazz;
            }

            // (0.1) Check our previously loaded class cache
            clazz = JreCompat.isGraalAvailable() ? null : findLoadedClass(name);
            if (clazz != null) {
                if (log.isDebugEnabled()) {
                    log.debug("  Returning class from cache");
                }
                if (resolve) {
                    resolveClass(clazz);
                }
                return clazz;
            }

            // (0.2) Try loading the class with the bootstrap class loader, to prevent
            //       the webapp from overriding Java SE classes. This implements
            //       SRV.10.7.2
            String resourceName = binaryNameToPath(name, false);

            // 其实这个地方拿到的只能是Java中的ExtensionClassLoader，因为BootClassLoader是null
            ClassLoader javaseLoader = getJavaseClassLoader();
            boolean tryLoadingFromJavaseLoader;
            try {
                // Use getResource as it won't trigger an expensive
                // ClassNotFoundException if the resource is not available from
                // the Java SE class loader. However (see
                // https://bz.apache.org/bugzilla/show_bug.cgi?id=58125 for
                // details) when running under a security manager in rare cases
                // this call may trigger a ClassCircularityError.
                // See https://bz.apache.org/bugzilla/show_bug.cgi?id=61424 for
                // details of how this may trigger a StackOverflowError
                // Given these reported errors, catch Throwable to ensure any
                // other edge cases are also caught
                URL url;
                if (securityManager != null) {
                    PrivilegedAction<URL> dp = new PrivilegedJavaseGetResource(resourceName);
                    url = AccessController.doPrivileged(dp);
                } else {
                    url = javaseLoader.getResource(resourceName);
                }
                tryLoadingFromJavaseLoader = (url != null);
            } catch (Throwable t) {
                // Swallow all exceptions apart from those that must be re-thrown
                ExceptionUtils.handleThrowable(t);
                // The getResource() trick won't work for this class. We have to
                // try loading it directly and accept that we might get a
                // ClassNotFoundException.
                tryLoadingFromJavaseLoader = true;
            }

            if (tryLoadingFromJavaseLoader) {
                try {
                    clazz = javaseLoader.loadClass(name);
                    if (clazz != null) {
                        if (resolve) {
                            resolveClass(clazz);
                        }
                        return clazz;
                    }
                } catch (ClassNotFoundException e) {
                    // Ignore
                }
            }

            // (0.5) Permission to access this class when using a SecurityManager
            if (securityManager != null) {
                int i = name.lastIndexOf('.');
                if (i >= 0) {
                    try {
                        securityManager.checkPackageAccess(name.substring(0,i));
                    } catch (SecurityException se) {
                        String error = sm.getString("webappClassLoader.restrictedPackage", name);
                        log.info(error, se);
                        throw new ClassNotFoundException(error, se);
                    }
                }
            }

            // 是否采用委托模式，
            boolean delegateLoad = delegate || filter(name, true);

            // (1) Delegate to our parent if requested
            if (delegateLoad) {
                if (log.isDebugEnabled()) {
                    log.debug("  Delegating to parent classloader1 " + parent);
                }
                try {
                    clazz = Class.forName(name, false, parent);
                    if (clazz != null) {
                        if (log.isDebugEnabled()) {
                            log.debug("  Loading class from parent");
                        }
                        if (resolve) {
                            resolveClass(clazz);
                        }
                        return clazz;
                    }
                } catch (ClassNotFoundException e) {
                    // Ignore
                }
            }

            // (2) Search local repositories
            if (log.isDebugEnabled()) {
                log.debug("  Searching local repositories");
            }
            try {
                clazz = findClass(name);
                if (clazz != null) {
                    if (log.isDebugEnabled()) {
                        log.debug("  Loading class from local repository");
                    }
                    if (resolve) {
                        resolveClass(clazz);
                    }
                    return clazz;
                }
            } catch (ClassNotFoundException e) {
                // Ignore
            }

            // (3) Delegate to parent unconditionally
            if (!delegateLoad) {
                if (log.isDebugEnabled()) {
                    log.debug("  Delegating to parent classloader at end: " + parent);
                }
                try {
                    clazz = Class.forName(name, false, parent);
                    if (clazz != null) {
                        if (log.isDebugEnabled()) {
                            log.debug("  Loading class from parent");
                        }
                        if (resolve) {
                            resolveClass(clazz);
                        }
                        return clazz;
                    }
                } catch (ClassNotFoundException e) {
                    // Ignore
                }
            }
        }

        throw new ClassNotFoundException(name);
    }

```

总结下来分这么几个步骤:
**破坏委托模式时：**
1. 从缓存中加载
1. 从JVM中的ExtensionClassLoader中加载，这个地方因为走的是委托模式，所以会按照Bootstrap -> Extension的路径查找
1. 从当前类加载器中加载
1. 从父加载器中加载，这个地方也会遵从委托模式，所以会按照 Bootstrap -> Extension -> Application -> Common -> Shared 路径查找


**开启委托模式时：**
1. 从缓存中加载
1. 从JVM中的ExtensionClassLoader中加载，这个地方因为走的是委托模式，所以会按照Bootstrap -> Extension的路径查找
1. 从父加载器中加载，这个地方也会遵从委托模式，所以会按照 Bootstrap -> Extension -> Application -> Common -> Shared 路径查找
1. 从当前类加载器中加载



**注意点：**
1. Bootstrap启动时，会把字段`catalinaDaemon`的`org.apache.catalina.startup.Catalina`对象的类的ClassLoader设置为`Shared Class Loader`，
