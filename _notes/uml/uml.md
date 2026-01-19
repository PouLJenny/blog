# UML

## What
对面向对象系统进行可视化、详述、构造和文档化正是统一建模语言(UML)的目的。

## 类关系 Relationships

| Relationship   | Function                                                                 | Notation            |
|----------------|--------------------------------------------------------------------------|---------------------|
| association    | A description of a connection among instances of classes                 | —————              |
| dependency     | A relationship between two model elements                                 | - - - - - >         |
| generalization | A relationship between a more specific and a more general description, used for inheritance and polymorphic type declarations           | ───▷               |
| realization    | Relationship between a specification and its implementation               | - - - - ▷           |
| usage          | A situation in which one element requires another for its correct functioning | «kind» - - - > |


### Association 
在 UML 类图中， 用实线连接有关联的对象所对应的类

A description of a connection among instances of classes

含义： 持有引用
Java对应： 成员变量

```java
class A {
    private B b;
}
```
上面的例子中A和B就是关联关系

#### 双向关联
不带箭头的实现，默认就是双向关联

#### 单向关联
单向关联用带箭头的实线表示.

#### 自关联


#### Aggregation
表示的是整体和部分的关系，整体与部分 可以分开.
在 UML 中，聚合关系用带空心菱形的直线表示。 


#### Composition
也是整体与部分的关系，但是整体与部分不可以分开.
在 UML 中，组合关系用带实心菱形的直线表示。


### Dependency

在UML中，依赖关系用带箭头的虚线表示，由依赖的一方指向被依赖的一方。

含义： 临时使用
Java对应： 方法参数/局部变量

### Generalization
在UML中，泛化关系用带空心三角形的直线来表示。

含义： is-a
Java对应： extends


### Realization

是用来规定接口和实线接口的类或者构建结构的关系，接口是操作的集合，而这些操作就用于规定类或者构建的一种服务。
在 UML 中，类与接口之间的实现关系用带空心三角形的虚线来表示。

含义： implements
Java对应： implements




## 参考文献

[The Unified Modeling Language Reference Manual(Second Edition) James Rumbaugh,Ivar Jacobson,Grady Booch](https://pdf.poul666.top/web/viewer.html?file=https://file.poul666.top/poul/%E6%96%B0%E5%8A%A0%E5%8D%B71/study/ebook/uml/Rumbaugh--UML_2.0_Reference_CD.pdf)
