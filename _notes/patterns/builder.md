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

一种解决方案是类`RTFReader`中配置转换RTF格式成其他文本格式的`TextConverter`对象。当`RTFReader`解析RTF文档时，它使用`TextConverter`来执行实际的解析.无论什么时候`RTFReader`识别到了RTF文本字符，都会把请求转交给`TextConverter`。`TextConverter`对象负责执行数据转换，并输出为其它格式。

`TextConverter`的子类有着不同的转换和格式化逻辑。比如，`ASCIIConverter`类忽略非文本字符的处理。另外`TeXConverter`实现了所有请求的操作，以生成一个捕捉文本中所有样式信息的TeX表示。`TextWidgetConverter`类会生成一个复杂的用户界面对象，用户可以看到并编辑文本数据。

![](/assets/notes/patterns/builder_01.png)

每种转换类，都将创建复杂对象的机制，隐藏在了抽象接口的后面。转换器的代码从负责解析RTF文档的阅读器中分离了出来，

构造器模式保存了所有的这些关系。每个转换类被称为**Builder**,阅读器被称为**director**。

## Applicability/应用场景

## Structure/结构

## Participants/角色

## Consequences/总结

## Related Patterns/相关的模式
