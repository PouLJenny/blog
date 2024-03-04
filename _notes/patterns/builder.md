---
layout: post
title:  "23种设计模式-构造器模式"
date:   2024-03-03 08:27:00 +0800
categories: 设计模式
tags: 设计模式
permalink: /patterns/builder
published: false
publish_file: 2024-03-03-patterns-builder.md
toc: true
---
# Builder模式 构造器模式


## Intent/目的

分离复杂对象的构造和其本身，这样相同的构造过程可以创建不同的对象。

## Motivation/动机

RTF（Rich Text Format）文档交换格式的阅读器应该能够将RTF转换为多种文本格式。它可以将RTF文档转换成ASCII 文本或者是可以编辑的文本部件。问题是，转换的目标格式是不确定的。所以需要容易的添加新的转换器而不需要修改阅读器的代码。

一种解决方案是类`RTFReader`中配置转换RTF格式成其他文本格式的`TextConverter`对象，

## Applicability/应用场景

## Structure/结构

## Participants/角色

## Consequences/总结

## Related Patterns/相关的模式
