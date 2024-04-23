# Command模式 命令模式

## Intent/目的

将请求封装为对象，从而允许您使用不同的请求为客户端参数化、排队或记录请求，并支持可撤销的操作。

## Also Known As
Action,Transaction

## Motivation/动机

有时候，需要向对象发出请求，而不知道所请求的操作或接收请求的对象的任何信息。例如，用户界面工具包包括按钮和菜单等对象，以响应用户输入执行请求。但是工具包不能在按钮或菜单中明确实现请求，因为只有使用工具包的应用程序知道应该在哪个对象上执行什么操作。作为工具包设计者，我们无法知道请求的接收者或执行请求的操作。

命令模式使工具包对象能够通过将请求本身转换为对象来向未指定的应用程序对象发出请求。这个对象可以像其他对象一样存储和传递。该模式的关键是一个抽象的 `Command` 类，它声明了执行操作的接口。在最简单的形式中，该接口包括一个抽象的 `Execute` 操作。具体的 `Command` 子类通过将接收者存储为实例变量，并实现 `Execute` 来调用请求，来指定一个接收者-动作对。接收者具有执行请求所需的知识。

![](/assets/notes/patterns/command_01.png)

菜单可以很容易地使用命令对象来实现。菜单中的每个选项都是 `Menultem` 类的一个实例。应用程序类创建这些菜单和它们的菜单项以及其他用户界面。应用程序类还跟踪用户打开的文档对象。

应用程序使用具体的命令子类的实例配置每个 `Menultem`。当用户选择一个 `Menultem` `时，Menultem` 调用其命令的 `Execute` 方法，并执行操作。`Menultem` 不知道它们使用的是 `Command` 的哪个子类。命令子类存储请求的接收者，并在接收者上调用一个或多个操作。

例如，`PasteCommand `支持将剪贴板中的文本粘贴到文档中。`PasteCommand` 的接收者是在实例化时提供的文档对象。`Execute` 操作在接收文档上调用 `Paste`。

![](/assets/notes/patterns/command_02.png)

`OpenCommand` 的 `Execute` 操作不同：它会提示用户输入文档名称，创建相应的文档对象，将文档添加到接收应用程序，并打开文档。

![](/assets/notes/patterns/command_03.png)

有时候，一个菜单项需要执行一系列的命令。例如，一个用于将页面居中显示为正常大小的菜单项可以由一个 `CenterDocumentCommand` 对象和一个 `NormalSizeCommand` 对象构建而成。因为通常会以这种方式串联命令，我们可以定义一个 `MacroCommand` 类来允许一个菜单项执行任意数量的命令。`MacroCommand` 是一个具体的 `Command` 子类，它简单地执行一系列命令。`MacroCommand` 没有显式的接收者，因为它所串联的命令定义了它们自己的接收者。

![](/assets/notes/patterns/command_04.png)

在这些例子中，注意到命令模式将调用操作的对象与执行操作的对象解耦。这为我们设计用户界面提供了很大的灵活性。一个应用程序可以通过使菜单和按钮共享同一个具体的命令子类的实例，为一个功能提供菜单和按钮界面。我们可以动态地替换命令，这对于实现上下文敏感的菜单是有用的。我们还可以通过将命令组合成更大的命令来支持命令脚本。所有这些都是可能的，因为发出请求的对象只需要知道如何发出请求；它不需要知道请求将如何被执行。

## Applicability/应用场景



## Structure/结构

![](/assets/notes/patterns/command_05.png)

## Participants/角色

- Command
  - 定义一个执行操作的接口.
- ConcreteCommand (PasteCommand, OpenCommand)
  - 绑定具体的动作到接收对象.
  - 实现操作接口，并在关联的接收者上执行对应的操作.
- Client (Application)
  - 创建具体的命令对象，并设置它的接收者
- Invoker (Menultem)
  - 请求命令来执行请求。
- Receiver (Document, Application)
  - 知道如何执行与执行请求相关的操作。任何类都可以作为接收者。

## Consequences/总结




## Related Patterns/相关的模式

组合模式可以被用来实现`MacroCommands`。  
备忘录模式可以保持命令需要撤销其效果的状态。  
必须在放置在历史记录列表之前被复制的命令充当原型模式。  
