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

[wiki](https://en.wikipedia.org/wiki/Chain-of-responsibility_pattern)

## 说明/Overview

责任链模式，是F4的23种设计模式之一，归属行为模式类下。

## 结构/Structure

![](/assets/notes/patterns/chain_of_responsibility_struct.png)

## 角色/Participants

- `Handler` 
    - defines an interface for handling requests.
    - (optional) implements the successor link.
- `ConcreteHandler`
    - handles requests it is responsible for.
    - can access it's successor.
    - if the `ConcreteHandler` can handle the request,it does so.otherwise it forwards the request to its successor.
- `Client`
    - initiates the request to a `ConcreteHandler` object on the chain.

## 协作/Collaborations
When a client issue a request,the request propagates along the chain until a `ConcreteHandler` object takes responsibility 
for handling it.

## 总结/Consequnces
Chain of Responsibility has the following benefits and liabilities:
1. Reduced coupling.
2. Added flexibility in assigning responsibilities to objects.
3. Receipt isn't guaranteed.
4. 此模式最大的优点就在于它弱化了发出请求的人和处理请求的人之间的关系，Client角色向第一个ConceretHandler角色发出请求,然后请求会在责任链中传播，
直到某个ConcerentHandler角色处理请求。如果不使用此种模式，就必须有个伟大的角色知道“谁应该处理什么请求”,这有点类似中央集权制。
而让发出请求的人知道谁应该处理什么事情并不明智，因为如果发出请求的人不得不知道处理请求的人各自的责任分担情况，就会降低其作为可复用的组件的独立性。
5. 可以动态的改变责任链,来满足不同场景的需求。
6. 专注自己的工作

缺点:
使用责任链模式，可以推卸请求，知道找到合适的处理请求的对象，这样确实可以提高程序的灵活性。但是也会导致处理的延迟.
这是一个需要权衡(trade off)的地方. 如果对响应时间要求非常敏感的地方，这种做法就不是太合适了。

## 相关的设计模式/Related Patterns
Chain of Responsibility is often applied in conjunction with Composite.There a component's parent can act its successor.

有时会使用Commond模式向Handler发送请求


## 例子/Use cases
F4的书里讲的都是些图形化界面组件的例子。
服务端的开源框架里，自己找到的有下面的比较像的： 
1. `Servlet` 中的 `Filter` 比较像,不过它是会单独定义一个`FilterChain`内部通过一个集合字段来维护一个`Filter`链条
运行起来就是 一个Http请求过来 通过Filter链来找到那些不合法的请求 并立即响应

TODO

