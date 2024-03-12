---
layout: post
title:  "23种设计模式-适配器模式"
date:   2024-03-12 14:25:00 +0800
categories: 设计模式
tags: 设计模式
permalink: /patterns/adapter
published: true
publish_file: 2024-03-12-patterns-adapter.md
toc: true
---
# Adapter Pattern / 适配器模式

## Intent/目的

Adapter（适配器）允许不兼容接口的类一起工作，从而将一个类的接口转换成客户端所期望的另一个接口。

## Also Known As/其它叫法

Wrapper

## Motivation/动机

有时设计上可复用的工具类并不能被复用，仅仅是因为工具类的接口不能复合特定领域应用程序的需要。

举一个画板的例子，它可以让用户拖动并排列图形元素（线、多边形、文本框等等）到图片和图表中去。绘图编辑器的关键抽象是图形对象，它具有可编辑的形状并能够绘制自己。图形对象的接口由一个名为`Shape`的抽象类定义。编辑器为每种类型的图形对象定义了`Shape`的子类：用于线条的`LineShape`类，用于多边形的`PolygonShape`类，依此类推。

像`LineShape`和`PolygonShape`这样的基本几何形状类相对容易实现，因为它们的绘制和编辑能力本质上是有限的。但是，能够显示和编辑文本的`TextShape`子类要难得多，因为即使基本的文本编辑也涉及复杂的屏幕更新和缓冲区管理。与此同时，一个现成的用户界面工具包可能已经提供了一个复杂的`TextView`类用于显示和编辑文本。理想情况下，我们希望重用`TextView`来实现`TextShape`，但是工具包并没有考虑`Shape`类。因此，我们不能将`TextView`和`Shape`对象互换使用。

现有的并且不相关的类（比如`TextView`）如何在一个期望具有不同且不兼容接口的应用程序中工作呢？我们可以修改`TextView`类，使其符合`Shape`接口，但除非我们有工具包的源代码，否则这不是一个选项。即使我们有源代码，修改`TextView`也没有意义；工具包不应该为了让某一个应用程序工作而采用特定领域的接口。

相反，我们可以定义`TextShape`，使其将`TextView`接口适配到`Shape`接口。我们可以通过以下两种方式之一来实现：
1. 通过继承`Shape`的接口和`TextView`的实现，或者
2. 通过在`TextShape`中组合一个`TextView`实例，并根据`TextView`的接口实现`TextShape`。
这两种方法对应于适配器模式的类和对象版本。我们称`TextShape`为适配器。

![](/assets/notes/patterns/adapter_01.png)

这张图展示了对象适配器的情况。它展示了在`Shape`类中声明的`BoundingBox`请求是如何转换为`TextView`中定义的`GetExtent`请求的。由于`TextShape`将`TextView`适配到`Shape`接口，绘图编辑器可以重用原本不兼容的`TextView`类。

通常，适配器负责适配类本身不提供的功能。该图展示了适配器如何实现这些功能。用户应该能够互动地将每个形状对象“拖动”到新位置，但`TextView`并没有设计成这样做。`TextShape`可以通过实现`Shape`的`CreateManipulator`操作来添加这个缺失的功能，该操作返回适当的`Manipulator`子类的实例。

`Manipulator`是一个抽象类，用于定义对象如何响应用户输入对形状进行动画操作，比如将形状拖动到新位置。`Manipulator`有不同形状的子类；例如，`TextManipulator`是`TextShape`的相应子类。通过返回一个`TextManipulator`实例，`TextShape`添加了`TextView`缺少但`Shape`所需的功能。


## Applicability/应用场景

- 你想使用一个现成的类，但是此类与目标接口不匹配
- 您想要创建一个可重用的类，与不相关或未预料到的类合作，即不一定具有兼容接口的类。
- (object adapter only) 您需要使用几个现有的子类，但通过对每一个子类进行子类化来适应它们的接口是不切实际的。对象适配器可以适应其父类的接口。

## Structure/结构

继承的方式:

![](/assets/notes/patterns/adapter_02.png)

组合的方式:

![](/assets/notes/patterns/adapter_03.png)


## Participants/角色

- Target (Shape)
    - 定义特定领域的接口，客户端使用
- Client (DrawingEditor)
    - 与`Target`接口交互，操作此接口
- Adaptee (TextView)
    - 被适配的类，已经存在的想使用的类，但是不符合`Target`接口
- Adapter (TextShape)
    - 适配 `Adaptee` 到 `Target` 接口.

## Consequences/总结

类适配器和对象适配器有不同的权衡。

一个类适配器：

- 通过承诺使用具体的`Adaptee`类将`Adaptee`适配到`Target`。因此，当我们想要适配一个类及其所有子类时，类适配器将无法工作。
- 允许适配器覆盖`Adaptee`的部分行为，因为适配器是`Adaptee`的子类。
- 只引入一个对象，并且不需要额外的指针间接访问`Adaptee`。
   
一个对象适配器:

- 对象适配器允许单个适配器与许多`Adaptee`一起工作，即`Adaptee`本身以及所有的子类（如果有的话）。适配器还可以一次性为所有的`Adaptee`添加功能。
- 使得覆盖`Adaptee`行为变得更加困难。这将需要对`Adaptee`进行子类化，并使适配器引用子类而不是`Adaptee`本身。

还有一些其他的东西需要去考虑:

1.  适配器需要适配哪些工作？
适配器在将`Adaptee`适应到目标接口(Target interface)时的工作量各不相同。存在着一系列可能的工作，从简单的接口转换，例如更改操作名称，到支持完全不同的一组操作。适配器所做的工作量取决于目标接口与`Adaptee`的相似程度。
2. 可插拔适配器。
当你最小化其他类使用它时所需做出的假设时，一个类的可重用性就会更高。通过将接口适配集成到一个类中，你消除了其他类看到相同接口的假设。换句话说，接口适配让我们将我们的类整合到可能期望不同接口的现有系统中。ObjectWorks\Smalltalk使用术语"可插拔适配器"来描述具有内置接口适配的类。

考虑一个名为`TreeDisplay`的小部件，它可以以图形方式显示树结构。如果这是一个专用小部件，仅供一个应用程序使用，那么我们可能要求它显示的对象具有特定的接口；也就是说，所有对象必须是从一个`Tree`抽象类继承而来。但是，如果我们想要使`TreeDisplay`更具重用性（比如说我们想把它作为一个有用小部件的工具包的一部分），那么这个要求就是不合理的。应用程序将为树结构定义自己的类。它们不应该被强制使用我们的`Tree`抽象类。不同的树结构将具有不同的接口。

在目录层次结构中，例如，可以使用`GetSubdirectories`操作访问子目录，而在继承层次结构中，相应的操作可能被称为`GetSubclasses`。一个可重用的`TreeDisplay`小部件必须能够显示这两种类型的层次结构，即使它们使用不同的接口。换句话说，`TreeDisplay`应该内置接口适配功能。

3. 使用双向适配器实现透明度。
适配器的一个潜在问题是它们对所有客户端都不透明。一个适配后的对象不再符合适配器接口，因此无法像适配器对象一样在所有地方使用。双向适配器可以提供这种透明度。具体来说，当两个不同的客户端需要以不同的方式查看对象时，它们就很有用。

考虑一下双向适配器，它集成了`Unidraw`（一个图形编辑框架）和`QOCA`（一个约束求解工具包）。这两个系统都有表示变量的类：`Unidraw`有`StateVariable`，而`QOCA`有`ConstraintVariable`。为了使`Unidraw`能够与`QOCA`一起工作，`ConstraintVariable`必须适配为`StateVariable`；为了让`QOCA`向`Unidraw`传播解决方案，`StateVariable`必须适配为`ConstraintVariable`。

![](/assets/notes/patterns/adapter_04.png)

解决方案涉及到一个双向类适配器`ConstraintStateVariable`，它是`StateVariable`和`ConstraintVariable`的子类，将这两个接口适配到一起。在这种情况下，多重继承是一个可行的解决方案，因为适配后的类的接口差异较大。双向类适配器符合两个适配类，并且可以在任何系统中工作。


## Related Patterns/相关的模式

Bridge（桥接模式）的结构类似于对象适配器，但Bridge有一个不同的意图：它旨在将接口与其实现分离，以便它们可以轻松且独立地变化。适配器旨在改变现有对象的接口。

Decorator（装饰模式）增强另一个对象而不改变其接口。因此，装饰器对应用程序比适配器更透明。因此，装饰器支持递归组合，这是纯适配器无法实现的。

Proxy（代理模式）为另一个对象定义了一个代表或替代，并且不改变其接口。
