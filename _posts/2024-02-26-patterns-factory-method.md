---
layout: post
title:  "23种设计模式-工厂方法模式"
date:   2024-02-26 16:34:15 +0800
categories: 设计模式
tags: 设计模式
permalink: /patterns/factory-method
published: true
publish_file: 2024-02-26-patterns-factory-method.md
toc: true
---
# 工厂方法模式

此文章翻译自《Design Patterns - Elements of Reusable Object-Oriented Software》 ISBN 0-201-63361-2
Chapter 3 Creational Patterns , Factory Method (P107)

才疏学浅，翻译之处或许有疏漏，还请各位慧眼识珠，指点迷津。

## Intent/目的
定义一个创建对象的接口，最终让子类来决定生成哪种类的对象。工厂方法模式使得类生成的时机延迟到子类。

## Also Known As/其它叫法
Virtual Constructor

## Motivation/动机
框架使用抽象的类来定义和维护对象之间的关系。一个框架通常也有责任创建这些对象。

一个可以向用户呈现多个文档的应用程序框架。有两个关键的抽象类分别是`Application`和`Document`。这两个类都是抽象的，各自的客户端有自己的实现。比如，创建一个画图应用，定义两个类分别为`DrawingApplication`和`DrawingDocument`。`Application`这个类需要管理类`Document`，并且如果需要的话创建`Document`,比如用户在菜单中点击*打开*或者*创建*按钮。

由于实例化特定的`Document`子类对象是程序指定的，`Application`抽象类没办法预测到底是生成的哪个`Document`子类，它只知道什么时候需要创建一个`Document`。所以出现了一个痛点：框架只认识高层的抽象类`Document`，具体的子类不清楚，也就无法实例化他们。

工厂方法模式(Factory Method)给出了解决方案.它把创建`Document`子类的细节移到了框架外面去。

![](/assets/notes/patterns/factory_method_01.png)

`Application`子类重写了抽象方法`CreateDocument()`并返回适当的`Document`子类。`Application`子类实例化之后，它便可以实例化程序指定的`Document`，而不需要知道到底是哪个`Document`子类。我们称`CreateDocument`为工厂方法(factory method)因为它的责任是“生产”一个对象。

## Applicability/应用

- 一个类不能预先知道创建对象的类
- 一个类想要子类自己来指定创建什么对象
- 类将责任委托给多个辅助子类之一，你希望将哪个辅助子类作为委托的事局部化

## Structure/结构

![](/assets/notes/patterns/factory_method_02.png)

## Participants/角色

- Product (Document)
    - 定义工厂方法创建的对象的接口
- ConcreteProduct (MyDocument)
    - 实现`Product`接口
- Creator (Application)
    - 声明工厂方法，接口返回对象为`Product`.Creator也许会定义一个默认的工厂方法实现，并返回默认的`ConcreteProduct`对象
    - 可能会调用工厂方法，创建`Product`对象
- ConcreteCreator (MyApplication)
    - 重写工厂方法返回`ConcreteProduct`

## Consequences/结果

工厂方法模式去除了绑定指定的子类到你的代码中。只需要和`Product`接口打交道，因此它可以作用于与任何用户定义的具体的`Product`子类。

但是工厂方法模式有个潜在的缺点就是：客户端不得不子类化`Creator`类，为了创建特定的`ConcreteProduct`对象。有些情况客户端必须处理其它的演化点.(Subclassing is
fine when the client has to subclass the Creator class anyway, but otherwise the
client now must deal with another point of evolution)(这里贴出原文，因为我对这句话中最后的一部分不太能理解)

工厂方法模式提供了额外的两点重要特性：

1. 给子类提供了钩子。
    通过工厂方法模式创建的对象相比于直接创建一个对象更有扩展性。工厂方法模式给子类留了一个钩子，用来创建对象的扩展版本。

    在上面`Document`的示例中，`Document`类还可以定义一个名叫`CreateFileDialog`的工厂方法并创建一个默认的文件对话对象用来打开存在的document.一个`Document`子类会定义应用程序指定的文件对话对象来覆盖默认的。这个例子中工厂方法不是抽象的，会提供默认的实现。

1. 连接平行类层次结构。
    

## Related Patterns/相关的模式

- 抽象工厂模式（Abstract Factory）
- 模版方法模式（Template Methods）
- 原型模式（Prototypes）