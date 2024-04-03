---
layout: post
title:  "23种设计模式-责任链模式"
date:   2023-02-24 10:00:00 +0800
categories: 设计模式
tags: 设计模式
permalink: /patterns/chain-of-responsibility
published: true
publish_file: 2024-02-26-patterns-chain-of-responsibility.md
toc: true
---
# 责任链模式/chain of responsibility

## Intent/目的

通过给予多个对象机会来处理请求，避免请求的发送者与接收者之间的耦合。将接收对象进行链式连接，并沿着链传递请求，直到有一个对象处理它。

## Motivation/动机

考虑一个图形用户界面的上下文敏感帮助设施。用户可以通过单击界面的任何部分来获取帮助信息。提供的帮助取决于被选中的界面部分及其上下文；例如，对话框中的按钮小部件可能与主窗口中的类似按钮有不同的帮助信息。如果该界面部分没有具体的帮助信息，那么帮助系统应该显示一个关于即时上下文的更通用的帮助信息——例如，整个对话框。

因此，根据帮助信息的通用性来组织帮助信息是很自然的——从最具体到最通用。此外，很明显，帮助请求由几个用户界面对象之一处理；具体由哪一个处理取决于上下文以及可用帮助的具体程度。

这里的问题在于，最终提供帮助的对象对于发起帮助请求的对象（例如，按钮）并不是明确知道的。我们需要的是一种方法来解耦发起帮助请求的按钮和可能提供帮助信息的对象。责任链模式定义了这一过程是如何发生的。

这种模式的思想是通过给多个对象机会处理一个请求来解耦发送者和接收者。请求沿着一系列对象传递，直到其中一个对象处理它。

![](/assets/notes/patterns/chain_of_responsibility_01.png)

链上的第一个对象接收请求，要么处理它，要么将其转发给链上的下一个候选对象，后者也采取同样的操作。发出请求的对象并不明确知道谁将处理它——我们说请求有一个隐式接收者(implicit receiver).

假设用户点击标有“打印”的按钮小部件以获取帮助。该按钮包含在一个`PrintDialog`实例中，这个实例知道它所属的应用程序对象（参见前面的对象图）。以下交互图说明了帮助请求是如何沿着链转发的：

![](/assets/notes/patterns/chain_of_responsibility_02.png)



## Applicability/应用场景

## Structure/结构

## Participants/角色

## Consequences/总结

## Related Patterns/相关的模式

