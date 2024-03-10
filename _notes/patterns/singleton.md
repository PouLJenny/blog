---
layout: post
title:  "23种设计模式-单例模式"
date:   2024-03-07 14:36:00 +0800
categories: 设计模式
tags: 设计模式
permalink: /patterns/singleton
published: false
publish_file: 2024-03-07-patterns-singleton.md
toc: true
---
# 设计模式-单例模式

## Intent/目的

确保类只有一个实例，并提供全局的访问点。

## Motivation/动机

对于某些类来说，拥有确切的一个实例是很重要的。尽管在系统中可以有许多打印机，但打印池应该只有一个。应该只有一个文件系统和一个窗口管理器。数字滤波器将有一个模数转换器。会计系统将专门为一家公司提供服务。

我们如何确保一个类只有一个实例，并且该实例易于访问？全局变量使对象可访问，但它不能阻止您实例化多个对象。

一个更好的解决方案是使类本身负责跟踪其唯一实例。类可以确保不会创建其他实例（通过拦截创建新对象的请求），并且可以提供访问实例的方式。这就是单例模式。

## Applicability/应用场景

- 一个类必须存在且仅存在一个实例，并且客户端必须能够从一个已知的访问点访问该实例。
- 唯一实例应该可以通过子类化进行扩展，并且客户端应该能够在不修改其代码的情况下使用扩展实例。

## Structure/结构

![](/assets/notes/patterns/singleton_01.png)

## Participants/角色

## Consequences/总结

## Related Patterns/相关的模式

