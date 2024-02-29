# 软件工程 9th Ian Sommerville


## 软件工程导论

### 软件过程
计划驱动的软件过程
形式化开发过程
进化式开发过程

#### 软件过程模型
1. 瀑布模型
    1. 需求分析和定义
    2. 系统和软件设计
    3. 实现和单元测试
    4. 集成和系统测试
    5. 运行和维护


    对需求了解的很好，而且在系统开发过程中不太可能发生重大改变的时候，适合使用瀑布模型
2. 增量式开发
    增量式开发是敏捷方法的一个基本部分，对于商务，电子商务和个人系统特别合适
3. 面向复用的软件工程
    1. 组件分析
    2. 需求修改
    3. 使用复用的系统设计
    4. 开发和集成

    3种类型的软件组件可能用于面向复用的过程
    1. 通过标准服务开发的web服务，可用于远程调用
    2. 对象的集合，作为一个包和组件框架，如.net或者j2ee等集成在一起
    3. 独立的软件系统，通过配置在特定的环境下使用

#### 需求工程过程
1. 可行性研究
2. 需求导出和分析
3. 需求描述
4. 需求有效性验证

#### 软件有效性验证 （Verification and Validation） V&V
1. 组件（或单元）测试
    由开发人员对组成系统的组件进行测试
2. 系统测试
    集成组件形成完整的系统。这个过程主要是关注
3. 接收测试
    这是系统在接受并运行之前进行的最后阶段测试。这个阶段不再是用模拟数据来测试系统，而是用客户提供的真实数据测试系统。

##### beta测试
当一个系统要作为软件产品在市场上销售时，所要进行的测试时beta测试。beta测试就是将系统交付给所有愿意使用该系统的潜在客户。
他们有义务报告系统中的问题，以使产品面向实际使用

##### Boehm的螺旋模型
1. 目标设置
2. 风险评估和规避
3. 开发和有效性验证
4. 规划

##### Rational 统一过程  RUP
1. 开端
2. 细化
3. 构造
4. 转换

### 敏捷开发
#### 敏捷宣言
We are uncovering better ways of developing software by doing it and helping others do it. Through this work we have come to value:

Individuals and interactions over processes and tools 

Working software over comprehensive documentation 

Customer collaboration over contract negotiation 

Responding to change over following a plan

That is, while there is value in the items on the right, we value the items on the left more.
#### 极限编程 extreme programing
Kent Beck.
极限编程中的创新思想
1. Test-first/ 测试驱动
2. pair programming 结对编程


极限编程中测试的关键特性
1. Test-first development 
2. incremental test development from scenarios
3. user involvement in the test development and validation, and
4. the use of automated testing frameworks. 

#### Scrum
是一个通用的敏捷方法，但它主要注重迭代开发的管理。
scrum 有三个阶段
1. Outline Planning and Architectural Design
2. Sprint Cycle
3. Project Closure

Scrum的创新在于它的中心阶段，也就是冲刺循环。一个循环是一个计划单元，需要做的工作有：评估、特性的选择和开发、软件的实现。循环的最后一个阶段，所
开发的全部功能都将交付给信息持有者。这个过程的主要特点如下：
1. 冲刺有一个固定的周期，一般是2～4周。在XP中，对应一个系统版本的开发
2. 规划的起点是所谓的backlog，是项目中要完成的工作清单。在评估阶段。这些挤压的任务经过审核。
进行优先级排序和风险的指派。此过程中用户都紧密的参与，在每一个循环开始时。提出新的需求或任务的建议
3. 在选择阶段，项目中的所有人员都要参加，和用户一起选择在冲刺循环中要开发的特性和功能
4. 一旦这些都得到同意，团队将组织进行软件开发。每天团队的开发成员都要参加短时会议，回顾开发过程。若有必要，将重新安排工作。
这个阶段，开发团队时隔离于客户和机构的。所有的交流都通过所谓的“Scrum master”进行。Scrum master使团队免受外界干扰。
工作方式取决于遇到的问题和团队本身，不像XP，Scrum对于如何写需求，使用测试优先开发等不做具体要求。但是如果团队觉得合适，这些XP的实践也可以使用。
5. At the end of the spints,the work done is reviewed and presented to takeholders(利益相关者).The next sprint cycle then begins.

#### 要点
- 敏捷方式是一种专注于快速开发的增量开发方法。频繁的发布软件、降低过程开销、生产高质量的代码.使用户直接参与到开发过程中。
- 决定使用敏捷还是计划驱动的方式开发，取决于所开发系统的类型，开发团队的能力和开发系统公司的文化
- 极限编程是一种著名的敏捷方法，它集成了一系列好的编程经验，例如频繁的软件发布、连续软件改善和客户参与到软件开发中
- 极限编程的一个特色就是开发程序功能之前先开发自动测试。在增量集成进系统的时候，所有的测试用例必须成功执行
- The Scrum method is an agile method that provides a project management framework.It is centered around a set of spints,which are 
fixed times periods when a system increment is developed.Planning is based on prioritizing a backlog of work and selecting the highest-
priority tasks for a sprint
- Scaling agile methods for large systems is difficult.Large systems need up-front design and some documentation. Continuous integration is practically impossible when there are several separate development teams working on a project.





### 需求工程
 The process of finding out, analyzing, documenting and checking these services and constraints is called requirements engineering (RE).



## 可依赖性和信息安全性

## 高级软件工程

## 软件管理

## 课后习题回答

### 第二章
#### 2.1 
1. 汽车防锁死刹车控制系统，需求变化固定，适合瀑布开发模型
2. 支持维护说明后期需求变动大，频繁。适合增量式开发模型
3. 已存在的系统，应该有很多成型的组件，适合面向服用的软件工程模型
4. 需求不明确，适合敏捷式增量开发模型
#### 2.2 
商务软件需求不固定，客户需求变动大。
#### 2.3
### 第三章
#### 3.1 
1. 等到系统完全交付的时候，客户之前的需求可能已经不存在了，系统已经没有存在的意义了
#### 3.2


