---
layout: post
title:  "Spring MVC 接口返回406错误"
date:   2018-03-22 10:00:00 +0800
categories: spring
tags: spring
permalink: /spring/spring-mvc-406-error
published: true
publish_file: 2018-03-22-spring-spring-mvc-406-error.md
toc: true
---

 # Spring MVC 接口返回406错误
 
 刚接手一个项目，开发接口的时候需要使用`@RequestBody`注解,来接受POST请求体里面的JSON数据，但是加上之后请求接口的时候竟然报`406`错误。真是坑了个爹了
 


----------


 首先先交代一下案发现场：
 - `Spring 4.0.2.RELEASE`
 - `jackson 1.9.13`
 Sring MVC 的配置信息
 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:p="http://www.springframework.org/schema/p"
	xmlns:context="http://www.springframework.org/schema/context"
	xmlns:mvc="http://www.springframework.org/schema/mvc"
	xsi:schemaLocation="http://www.springframework.org/schema/beans
                        http://www.springframework.org/schema/beans/spring-beans-3.1.xsd
                        http://www.springframework.org/schema/context
                        http://www.springframework.org/schema/context/spring-context-3.1.xsd
                        http://www.springframework.org/schema/mvc
                        http://www.springframework.org/schema/mvc/spring-mvc-4.0.xsd">
	<!-- 自动扫描该包，使SpringMVC认为包下用了@controller注解的类是控制器 -->
	<context:component-scan base-package="net.hrtop" />
	<!-- 静态资源不经过springmvc拦截 -->

	<!--避免IE执行AJAX时，返回JSON出现下载文件 -->
	<bean id="mappingJacksonHttpMessageConverter"
		class="net.hrtop.util.tools.CustomMappingJacksonHttpMessageConverter">
		class="org.springframework.http.converter.json.MappingJacksonHttpMessageConverter">
		<property name="supportedMediaTypes">
			<list>
				<value>text/html;charset=UTF-8</value>
			</list>
		</property>
	</bean>

	<!-- 启动SpringMVC的注解功能，完成请求和注解POJO的映射 -->
	<bean
		class="org.springframework.web.servlet.mvc.annotation.AnnotationMethodHandlerAdapter">
		<property name="messageConverters">
			<list>
				<ref bean="mappingJacksonHttpMessageConverter" /> <!-- JSON转换器 -->
			</list>
		</property>
	</bean>
	<!-- 定义跳转的文件的前后缀 ，视图模式配置-->
	<bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
		<!-- 这里的配置我的理解是自动给后面action的方法return的字符串加上前缀和后缀，变成一个 可用的url地址 -->
		<property name="prefix" value="/WEB-INF/pages/" />
		<property name="suffix" value=".jsp" />
	</bean>

	<!-- 配置文件上传，如果没有使用文件上传可以不用配置，当然如果不配，那么配置文件中也不必引入上传组件包 -->
	<bean id="multipartResolver"
        class="org.springframework.web.multipart.commons.CommonsMultipartResolver">
        <!-- 默认编码 -->
        <property name="defaultEncoding" value="utf-8" />
        <!-- 文件大小最大值 -->
        <property name="maxUploadSize" value="10485760000" />
        <!-- 内存中的最大值 -->
        <property name="maxInMemorySize" value="40960" />
    </bean>
	
    <mvc:annotation-driven />
    <mvc:default-servlet-handler/>           
</beans>
```


----------
所以决定使用DUBUG源码的方式解决这个问题
首先吧项目的日志级别改成debug，使用postman请求接口
然后发现了spring打印的debug级别的错误信息
```
DEBUG 2018-03-22 10:25:41(AbstractHandlerExceptionResolver.java:134) - Resolving exception from handler [public java.util.Map<java.lang.String, java.lang.Object> net.hrtop.org.controller.OrgController.saveOrg(net.hrtop.org.pojo.OrganizationVO,org.springframework.validation.BindingResult)]: org.springframework.web.HttpMediaTypeNotAcceptableException: Could not find acceptable representation
DEBUG 2018-03-22 10:25:41(AbstractHandlerExceptionResolver.java:134) - Resolving exception from handler [public java.util.Map<java.lang.String, java.lang.Object> net.hrtop.org.controller.OrgController.saveOrg(net.hrtop.org.pojo.OrganizationVO,org.springframework.validation.BindingResult)]: org.springframework.web.HttpMediaTypeNotAcceptableException: Could not find acceptable representation
DEBUG 2018-03-22 10:25:41(AbstractHandlerExceptionResolver.java:134) - Resolving exception from handler [public java.util.Map<java.lang.String, java.lang.Object> net.hrtop.org.controller.OrgController.saveOrg(net.hrtop.org.pojo.OrganizationVO,org.springframework.validation.BindingResult)]: org.springframework.web.HttpMediaTypeNotAcceptableException: Could not find acceptable representation
```

然后找到报错信息输出地方的源码或者在自己的`Controller`方法里打断点，一路跟到报错的地方。
我选择的是后者，经过长时间的跟踪Spring源码终于发现了犯罪嫌疑人。位置定位在`org.springframework.web.servlet.mvc.method.annotation.AbstractMessageConverterMethodProcessor `这个类中的`writeWithMessageConverters`这个方法
```java
@SuppressWarnings("unchecked")
	protected <T> void writeWithMessageConverters(T returnValue,
												MethodParameter returnType,
												ServletServerHttpRequest inputMessage,
												ServletServerHttpResponse outputMessage)
			throws IOException, HttpMediaTypeNotAcceptableException {

		Class<?> returnValueClass = returnValue.getClass();

		HttpServletRequest servletRequest = inputMessage.getServletRequest();
		List<MediaType> requestedMediaTypes = getAcceptableMediaTypes(servletRequest);
		List<MediaType> producibleMediaTypes = getProducibleMediaTypes(servletRequest, returnValueClass);

		Set<MediaType> compatibleMediaTypes = new LinkedHashSet<MediaType>();
		for (MediaType r : requestedMediaTypes) {
			for (MediaType p : producibleMediaTypes) {
				if (r.isCompatibleWith(p)) {
					compatibleMediaTypes.add(getMostSpecificMediaType(r, p));
				}
			}
		}
		if (compatibleMediaTypes.isEmpty()) {
			throw new HttpMediaTypeNotAcceptableException(producibleMediaTypes);
		}
```

最后锁定了上边的11行和12行的代码`requestedMediaTypes`和`producibleMediaTypes `不匹配导致的，然后再去跟踪这两个方法的源码(这里不再做多的赘述了),发现了最终的答案
Spring 解析访问路径的时候会解析路径中点后缀格式，当时我们的项目接口路径采取的是*.htm的格式，因此Spring解析出来客户端只接受`text/html`的`MediaType`。


----------

好了原因找到了，开始解决。
第一种解决方案： 接口路径不要使用`*.htm`或`*.html`的格式，实测可以但是此项目以前的路径都是这样的格式，改起来成本太高，所以找别的解决方案。

第二种解决方案： 其实接口就是要给调用这返回JSON的字符串，项目中使用的是JACKSON的包做的转换，也就是说让JACKSON的包支持转成`text/html`就可以了，可是我发现在Spring mvc的配置文件中已经支持这种方式了
```
<bean id="mappingJacksonHttpMessageConverter"
		class="net.hrtop.util.tools.CustomMappingJacksonHttpMessageConverter">
		class="org.springframework.http.converter.json.MappingJacksonHttpMessageConverter">
		<property name="supportedMediaTypes">
			<list>
				<value>text/html;charset=UTF-8</value>
			</list>
		</property>
	</bean>
```
但是跟踪源码的时候发现这种配置没有起作用
于是就换了一种方式来配置
```xml
  <mvc:annotation-driven >
		<mvc:message-converters>
			<bean id="mappingJacksonHttpMessageConverter"
				class="org.springframework.http.converter.json.MappingJacksonHttpMessageConverter">
				<property name="supportedMediaTypes">
					<list>
						<value>text/html;charset=UTF-8</value>
						<value>application/json;charset=UTF-8</value>
						<value>application/*+json;charset=UTF-8</value>
					</list>
				</property>
			</bean>
		</mvc:message-converters>
	</mvc:annotation-driven>
```

 换了配置之后发现spring成功使用jackson转换。终于搞定了这个问题。


----------
不过还有一个遗留问题就是以前的jackson配置没有生效，由于时间的问题没有找原因。这个以后博主找到原因会写在这里。