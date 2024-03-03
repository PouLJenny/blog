---
layout: post
title:  "23种设计模式-抽象工厂模式"
date:   2024-03-01 23:29:00 +0800
categories: 设计模式
tags: 设计模式
permalink: /patterns/abstract-factory
published: true
publish_file: 2024-03-01-patterns-abstract-factory.md
toc: true
---
# Abstract Factory Pattern / 抽象工厂模式

此文章翻译自《Design Patterns - Elements of Reusable Object-Oriented Software》 ISBN 0-201-63361-2
Chapter 3 Creational Patterns , Abstract Factory (P87)

才疏学浅，翻译之处或许有疏漏，还请各位慧眼识珠，指点迷津。

## Intent/目的

提供一个接口生成一组相关的对象，并无需指定具体的类。

## Also Known As/其它叫法

Kit

## Motivation/动机

考虑一个支持多种外观标准的用户界面工具包，例如 Motif 和 Presentation Manager。不同的外观标准定义了不同的外观和交互给用户界面部件，比如滚动条、窗口和按钮。为了在外观标准之间具有可移植性，应用程序不应该为特定的外观硬编码“部件”。在整个应用程序中实例化特定于外观的小部件类会使以后更改外观变得困难。

我们通过定义一个抽象的类`WidgetFactory`并声明创建每种类型部件的抽象方法来解决这个问题。并且每种类型的部件都是抽象的，具体的子类来实现自己的外观标准。`WidgetFactory`抽象类中有返回各个部件对象的抽象方法，每个方法都会返回新生成的部件对象。客户端通过调用每个方法来生成部件的实例，而且客户端不需要加载具体的部件子类。这样，客户端就跟具体的外观实现解偶了。

![](/assets/notes/patterns/abstract_factory_01.png)

上图中，每种外观标准都有各自的`WidgetFactory`子类。每个子类都实现了创建适当外观部件的方法。比如，类`MotifWidgetFactory`中的方法`CreateScrollBar`实例化并返回Motif 滚动条，而类`PMWidgetFactory`中的上述方法返回Presentation Manager的滚动条。客户端创建一些部件仅通过接口`WidgetFactory`即可，不需要知道实现具体外观的类。换句话说，客户端仅操作抽象类中的抽象方法即可，而不是具体的实现类。

类`WidgetFactory`会强依赖具体的部件类。一个Motif滚动条应该和Motif按钮还有Motif编辑器同时使用。这些限制，在使用类`MotifWidgetFactory`时会自动地实现。

## Applicability/应用场景

- 一个系统需要与产品的创建、组合和表现解偶
- 一个系统可以配置多种类型的产品族
- 一个产品族在设计上需要强制在一起使用
- 你想提供一个产品的类库，并希望只暴露接口而不关心具体的实现类

## Structure/结构

![](/assets/notes/patterns/abstract_factory_02.png)

## Participants/角色

- AbstractFactory (WidgetFactory)
  - 声明一组抽象方法创建抽象的产品对象
- ConcreteFactory (MotifWidgetFactory, PMWidgetFactory)
  - 实现创建具体产品对象的方法
- AbstractProduct (Window, ScrollBar)
  - 声明各种类型对象
- ConcreteProduct (MotifWindow, MotifScrollBar)
  - 实现接口`AbstractProduct`
  - 定义一个由相关的工厂类生成的产品对象
- Client
  - 只操作接口`AbstractFactory`和接口`AbstractProduct`的使用方
  

## Consequences/总结

抽象工厂模式有一下几处优缺点： 

1. **隔离具体的类** 抽象工厂模式帮助你控制应用程序创建对象的类。工厂负责创建对象的整个流程和细节，隔离了客户端和具体的产品实现类。客户端通过调用抽象类的抽象接口即可。具体的产品类名信息被隔离在具体的工厂实现类中，不会在客户端的代码中出现。
2. **更方便的变换产品族** 
3. **它促进了产品之间的一致性**
4. **支持新的产品相对困难一些**
   
## Related Patterns/相关的模式

- 工厂方法模式(factory method) `AbstractFactory`类通常通过工厂方法模式实现。
- 原型模式(Prototype) 上述提到的也可以通过原型模式实现。
- 单例模式(singleton) 具体的工厂通常是单例的。

