---
layout: post
title:  "23种设计模式-组合模式"
date:   2024-03-15 00:40:00 +0800
categories: 设计模式
tags: 设计模式
permalink: /patterns/composite
published: true
publish_file: 2024-03-15-patterns-composite.md
toc: true
---
# Composite模式 组合模式

## Intent/目的

将对象组合成树形结构，以表示部分-整体的层次关系。组合模式让客户端能够统一地处理单个对象和对象组合。

## Motivation/动机

图形应用程序，如绘图编辑器和原理图捕获系统，允许用户通过简单组件构建复杂的图表。用户可以将组件分组形成更大的组件，这些更大的组件又可以被分组形成更大的组件.一个简单的实现可以定义图形原语的类，例如文本和线条，以及其他作为这些原语容器的类。

但是，这种方法存在一个问题：使用这些类的代码必须区分原始对象和容器对象，即使大多数情况下用户将它们视为相同的。必须区分这些对象会使应用程序变得更加复杂。组合模式描述了如何使用递归组合，使客户端不必进行此区分。

![](/assets/notes/patterns/composite_01.png)

组合模式的关键是一个抽象类，代表了原语和它们的容器。对于图形系统来说，这个类就是 `Graphic`。`Graphic` 声明了诸如 `Draw` 等特定于图形对象的操作。它还声明了所有组合对象共享的操作，例如用于访问和管理其子对象的操作。

子类 `Line`、`Rectangle` 和 `Text`（参见前面的类图）定义了原始的图形对象。这些类实现了 `Draw `方法来绘制线条、矩形和文本。由于原始图形没有子图形，因此这些子类都不实现与子对象相关的操作。

`Picture` 类定义了一组 `Graphic` 对象的聚合体。`Picture` 实现了 `Draw` 方法来调用其子对象的` Draw `方法，并相应地实现了与子对象相关的操作。由于 `Picture` 接口符合 `Graphic` 接口，因此 `Picture` 对象可以递归地组合其他 `Picture` 对象。

下表显示了典型的递归组合的` Graphic` 对象的复合对象结构：

![](/assets/notes/patterns/composite_02.png)

## Applicability/应用场景

- 你想要表示对象的部分-整体层次结构。
- 你希望客户端能够忽略对象组合和单个对象之间的差异。客户端将统一对待组合结构中的所有对象。

## Structure/结构

![](/assets/notes/patterns/composite_03.png)

典型的组合对象结构：

![](/assets/notes/patterns/composite_04.png)

## Participants/角色

- Component (Graphic)
  - 声明组合中对象的接口
  - 实现接口的默认行为
  - 声明管理子组件的接口
  - （可选）定义一个接口，用于访问递归结构中组件的父级，并在必要时进行实现。
- Leaf (Rectangle, Line, Text, etc.)
  - 表示组合中的叶子对象。叶子对象没有子对象。
  - 在组合中定义了原始对象的行为。
- Composite (Picture)
  - 定义了具有子节点的组件的行为。
  - 存储子组件。
  - 在 `Component` 接口中实现了与子节点相关的操作。
- Client
  - 通过 `Component` 接口操纵组合中的对象。

## Consequences/总结

- 定义了由原始对象和组合对象组成的类层次结构。原始对象可以组成更复杂的对象，而这些对象又可以被组合，以此类推，形成递归结构。在客户端代码需要原始对象时，也可以接受组合对象。

- 使客户端代码简单化。客户端可以统一对待组合结构和单个对象。通常客户端不知道（也不应该关心）它们是在处理叶子对象还是复合组件。这简化了客户端代码，因为它避免了在定义组合的类上编写标记和 case 语句式函数。

- 使添加新种类的组件更容易。新定义的 `Composite` 或 `Leaf` 子类会自动与现有的结构和客户端代码配合工作。客户端不必为新的 `Component` 类而做出更改。

- 可能使设计过于通用。使添加新组件变得容易的缺点是，它使得限制组合的组件变得更加困难。有时您希望一个组合仅具有某些特定的组件。使用 `Composite`，您不能依赖类型系统来为您强制执行这些约束。您将不得不使用运行时检查。

## Related Patterns/相关的模式

通常，组件-父级链接用于责任链模式。

装饰者模式通常与组合模式一起使用。当装饰者和组合模式一起使用时，它们通常会有一个共同的父类。因此，装饰者必须支持 `Component` 接口，包括 `Add`、`Remove` 和 `GetChild` 等操作。

享元模式允许您共享组件，但它们不能再引用它们的父级。

迭代器模式可用于遍历组合对象。

访问者模式将原本分散在组合和叶子类中的操作和行为局部化