# DBMS

## 复习题

### 名词解析

- **操作型处理/OLTP/联机事务处理**
    对数据库联机的日常操作，通常是对一个或一组数据的查询和修改。主要是为企业特定应用服务。比较关心响应时间和数据的安全性、完整性。

- **分析型处理/OLAP/联机分析处理**
    用于管理人员的决策分析
    OLAP委员会给出的OLAP的定义为：
    OLAP是使分析人员、管理人员和执行人员能够从多种角度对从原始数据中转化出来的，能够真正为用户所理解的，并真实反应企业多维特性的信息进行快速、一致、交互的存取，从而获得对数据更深入了解的一类软件技术。

- **数据仓库**
    数据仓库是一个面向主题的、集成的、不可更新的、随时间不断变化的数据集合。

- **主题**
    主题是在较高层次上将企业信息系统中的数据综合、归类并进行分析利用的抽象。
- **面向主题**
    面向主题的数据组织方式，就是在较高层次上对分析对象的数据的完整、一致的描述。它能完整、统一的刻画各分析对象所涉及企业的各项数据，以及数据之间的联系。所谓较高层次是相对面向应用的数据组织方式而言的，即按照主题进行数据组织的方式具有更高的数据抽象级别。
- **主题域**
    一个完备的分析领域，具有独立性、完备性两个特点。
    - 独立性: 主题域必须具有独立内涵,要求有明确的界限，规定某项数据是否该属于该主题。
    - 完备性: 主题内包含任何对该主题对象的分析处理要求的一切内容
- **主题之间的重叠**
    1. 主题之间的重叠是逻辑上的重叠, 不是同一数据内容的重复物理存储
    2. 主题之间的重叠仅是细节级的重叠，因为在不同的主题中的综合方式是不同的。
    3. 主题间的重叠不一定是两两重叠。

- **粒度/数据粒度**
    数据的不同综合级别。有两种形式：
    1. 对数据仓库中的数据的综合程度高低的一个度量；
    2. 样本数据库，粒度级别是根据采样率的高低来划分的。

- **多重粒度**
    数仓的主要作用是联机分析处理，绝大部份查询都是基于一定程度的综合数据上。所以大粒度的数据存储在高性能设备上，满足绝大部份查询，小粒度的数据存放在低速设备上。

- **分割/数据分割**
    将数据分布到各自的物理单元中，以便能分别独立处理，提高数据分析效率。

- **分片/数据分片**
    数据分割后的数据单元。

 - **水平分片**
    按一定的条件将一个关系按行分为若干不相交的子集

- **垂直分片**
    将关系按列分为若干子集

- **导出分片**
    水平分片的条件不是本身属性的条件，而是其他关系的属性的条件

- **混合分片**
    水平分片、垂直分片、导出分片混合使用

- **集市/数据集市**
    部门级数据仓库，小型的、面向部门或工作组

- **操作型数据存储/ODS/Operational Data Store**
    ODS是用于支持企业日常全局应用的数据集合。

- **企业级OLTP/操作型处理模式**
    企业级OLTP，是指在实际数据处理中一个事务同时涉及多个部门的数据

    操作型处理模式，含有更新操作的工作模式（排他型）。
- **即时OLAP/信息型处理模式**
    即时OLAP，很多情况下公司中层决策过程并不需要参考太多的历史数据，而主要参考和存取当前和接近当前的数据，并且要求有较快的响应速度。

    信息型处理模式 只有查询操作的工作模式（非排他型）。

- **分层ODS**
    - 集团公司的ODS,侧重于向DW提供一致的数据以进行高层决策管理
    - 子公司的ODS,进行子公司全局事务的处理

- **DSS**
    决策支持系统
- **EIS**
    经理信息系统

- **多维数据模型**
    多维数据模型是一个多维空间，维表示用户的观察对象，多维空间中的点表示度量的值。其核心概念包括维、度量、数据方体、数据单元。
- **维**
    维是人们观察数据的特定角度，是某个事物的属性。
- **维成员 member**
    维的一个取值。
- **维层 level**
    观察数据的不同的细节程度
- **维层次 hierarchy**
    维的每种分类方法。
- **维属性 attribute**
    维成员所具有的特征。
- **度量 measure**
    度量是要分析的目标或对象。度量一般有名字、数据类型、单位、计算公式等属性。
- **输入度量**
    输入度量的值从业务处理活动中获取
- **导出度量**
    导出度量需要经过计算得到
- **可累计型度量**
    能沿着时间维度做聚集计算
- **不可累计型度量**
    不能沿着时间维度做聚集计算
- **数据方体/数据立方体/超级立方体/多维超方体 cube**
    多维数据模型构成的多维数据空间称作数据方体。
- **数据单元 cell**
    多维数据空间中的一个点。
- **星型模型**
    星型模型是多维数据模型的基本结构，通常由一个很大的事实表和一组较小的维表组成。事实表用来存储事实的度量值和各个维的码值。维表用来保存维的信息。事实表通过存储的每个维表的码值和每一个维表联系在一起。
- **雪花模型**
    星型模型把维表规范化后形成的。
- **事实群模型/星系模型**
    多个事实表共享一组维表
- **聚集**
    聚集是对细节数据进行综合的过程，是多维分析的基础。
- **分布型聚集函数**
    一个聚集函数可以用下述方式分布计算则是分布型聚集函数：
    将数据分成n份，对其中的每一份应用该函数，可以得到n个聚集值，对这n个聚集值进行计算得到的结果和整个数据应用该函数得到的结果一致。
    比如求和（sum）、计数（count）、最小值（min）、最大值（max），top-N
- **代数型聚集函数**
    由若干个分布型函数进行代数运算得出。
    比如：平均值（agerage）
- **整体型聚集函数**
    不能由其他函数进行代数运算得出。
    比如：求中间值（median），排序（rank）
- **多维分析操作**  
    是指对数据方体执行切片、切块、旋转等各种分析操作，剖析数据，使用户能从多个角度、多个侧面观察数据库中的数据，从而深入了解包含在数据中的信息和内涵。
- **切片**
    在数据方体的某一个维上选定一个维成员的动作
- **切块**
    在数据方体的某一个维上选定一区间维成员的动作
- **旋转**
    改变数据方体维的次序的动作
- **下钻**
    从更多的维或者某个维的更细层次上来观察数据。有两种类型
    1. 在现有的维上钻取到更细一层的数据
    2. 增加更多的维来钻取数据。
- **上卷**
    观察更粗的数据。有两种类型：
    1. 上卷到现有的某个维的更高层级去进行分析
    2. 减少一个维来进行分析。

- **MDX/多维查询语言**
    MDX是OLE DB for OLAP接口规范中定义的一组用于多维数据进行查询的语句，类似于关系数据库中的标准SQL语句。

- **导出关系**
    多维数据模型可以用一个数据方体来表示，一个数据方体由多个维和度量组成，而由不同维或维上的不同层又可以组合出多个数据方体，通常用cubiod表示。
    如果cuboid A是由cuboid B通过减少维的个数或上升维的层次得到的，则称cuboid A可以由cubiod B导出

- **数据方体格**
    数据方体格结构是一个有向图，图中每个节点表示一个cuboid，每条边表示节点之间的导出关系。

- **星形连接**
    每个维的维表需要同时和事实表做连接操作。

- **数据方体预计算**
    数据综合是一件非常耗时的操作，为了缩短查询响应时间，对常用的cuboid预先计算并存储，以减少事实计算时间。

- **数据方体缩减**
    数据方体中，随着维数的增加和事实表的增大，数据单元的个数呈爆炸式增长。只能存储部分的数据单元，损失了部分查询的效率。通过使用特殊的数据压缩技术将整个数据方体存储下来，称为数据方体缩减技术。
- **数据方体维护**
    当数据源中的数据发生变化后，需要将这些变化反映到数据方体中。包括实体化试图的维护、数据缩减结构的维护。

- **广义索引**
    用来记录具有某些特殊性质数据的索引.比如最值，top-k值等

- **数据库体系化环境**
    在一个企业或组织内, 由各面向应用的OLTP数据库、以及各级面向主题的数据仓库所组成的完整的数据环境；并在这个数据环境上建立和进行一个企业或部门的从联机事务处理到企业管理决策的所有应用。

### 简答题&论述题
- **请简要说明事务处理环境不适宜 DSS 应用的原因？**
- **为什么说在传统的数据库环境中直接构建分析型应用是一种失败的尝试？**
- **操作型环境在处理分析型应用时具有的局限性是什么？**
- **传统的数据库环境在处理分析型应用时所面临的局限性是什么？**
  1. 事务处理和分析处理的性能特性不同
        1. 事务处理，操作频率高，处理时间短
        1. 分析处理，处理数据量大，消耗资源多，响应时间长
  1. 数据集成问题
        1. 数据分散问题
        1. 蜘蛛网问题
        1. 数据不一致
        1. 外部数据和非结构化数据
  1. 数据动态集成问题
        1. 集成后的数据不会跟数据源联动
  1. 历史数据问题
        1. 事务处理只存储当前的数据，但是分析处理依赖历史数据
  1. 数据综合问题
        1. 分析处理，需要把细节数据做综合处理，但是事务处理只存储细节数据，不具备综合能力

- **操作型数据和分析型数据的主要区别是什么？**
- **操作性处理和分析型处理的主要区别是什么？**
  |操作型数据|分析型数据|
  |--|--|
  |原始数据|导出数据|
  |细节的|综合的或提炼的|
  |当前数据|历史数据|
  |可更新|不可更新，但周期性追加和刷新|
  |操作需求事先可知道|操作需求事先不知道|
  |生命周期符合软件开发生命周期（SDLC）|完全不同的生命周期|
  |对性能要求高|对性能要求宽松|
  |一个时刻操作一个单元|一个时刻操作一个集合|
  |事务驱动|分析驱动|
  |面向业务处理|面向分析处理|
  |一次操作数据量小，计算简单|一次操作计算量大，计算复杂|
  |支持日常操作|支持管理需求|


- **请举例说明什么是操作型处理？**
  银行工作人员根据用户的要求通过储蓄系统完成对某个账户的存款和取款操作，数据库管理系统在后台完成对数据库数据的增删改操作。

- **请举例说明什么是分析型处理？**
  销售经理希望通过调整商品在各零售店的分配数量来扩大某种商品的销售量。他首先要查询历史数据库中各零售店最近若干年（比如5年）内每天的销售记录，计算出近5年来每个零售店的年度销售量，通过对比确定销售量增长较快的零售店。为了进一步分析增长的原因，他还会计算出每月的销售量，判断增长的原因是否与季度有关，还要分析是否其它商品的销售带动了目标商品的销售。他还会到其它部分获取5年来商品的促销计划，确定销售量的增长与促销的关系。经过综合分析后，确定每个零售店对这种商品的分配数量。

- **什么是数据仓库？**
- **请给出一种数据仓库的定义。**
- **数据仓库的四个基本特征是什么？**
  见名词解析 "数据仓库"

- **什么是主题与面向主题？**
    见名词解析 "主题"、"面向主题"
- **什么是主题域？**
    见名词解析 "主题域"

- **你是如何理解数据仓库的数据是不可更新的，数据仓库的数据又是随时间不断变化的？**
- **为什么说数据仓库是不可更新的又是随时间不断变化的？**
    一旦某个原始数据进入数据仓库，一般情况下不允许修改，并且会长期保留。
    而随时间不断变化的，具体表现在以下三个方面：
    1. 数据仓库会随时间变化不断增加新的数据
    2. 数据仓库会将不需要的数据卸出，转存到其它存储设备。
    3. 数据仓库中包含有大量的综合数据，这些数据中很多与时间有关。需要随时间的变化不断地进行重新综合。

- **什么是数据库体系化环境？企业的数据库体系化环境的四个层次是什么？它们之间的关系是什么？**
    在一个企业或组织内, 由各面向应用的OLTP数据库、以及各级面向主题的数据仓库所组成的完整的数据环境；并在这个数据环境上建立和进行一个企业或部门的从联机事务处理到企业管理决策的所有应用。由4个层次
    1. 操作型环境
    2. 全局级数据仓库
    3. 部门级的局部仓库
    4. 个人级数据仓库  

    ```mermaid
    graph LR
    操作型环境--抽取-->全局级数据仓库
    全局级数据仓库--抽取-->部门级的局部仓库
    部门级的局部仓库--抽取-->个人级数据仓库
    全局级数据仓库--抽取-->个人级数据仓库
    ```

- **在向数据仓库追加数据时，如何捕捉变化了的数据？**
    1. 时标方法。
        如果数据含有时标，对新插入或更新的数据记录，加更新时的时标。但是许多数据库中的数据不包含时标。
    2. DELTA文件。
        由应用来生成DELTA文件，记录应用所改变的所有内容。避免了扫描整个数据库，效率比较高。问题是生成DELTA文件的应用并不普遍。
    3. 前后快照文件的方法。
        在上次抽取数据库数据到数据仓库之后及本次将抽取数据库数据之前，对数据库分别做一次快照，然后比较两副快照的不同，从而确定实现数据仓库追加的数据。这种方法需占用大量资源，可能会比较大的影响系统性能，因此并无多大实际意义。
    4. 日志文件。
        利用DB的固有机制，数据只限于日志文件，不用扫描整个数据库。

- **请简述数据仓库的体系结构。**
    数据仓库系统由数据源、集成工具、数据仓库与数据仓库服务器、联机分析处理（OLAP）服务器、元数据与元数据管理工具、数据集市、前端分析工具组成。
    1. 数据源，企业内部信息和外部信息，内部信息一般是存放在操作型数据库中。
    2. 集成工具，包括抽取、清洗、转换、加载、维护的ETL工具。
    3. 数据仓库服务器，负责管理数据仓库中的数据，一般由关系型数据库扩展而成。
    4. OLAP服务器，对分析需要的数据按多维数据模型进行再次重组，已支持用户多角度、多层次的数据分析。具体实现包括ROLAP结构、MOLAP结构、HOLAP结构、特殊SQL服务器。
    5. 数据集市见名词解析
    6. 元数据，是整个数据仓库的所有描述性信息。元数据管理工具由ETL工具来建立和维护。
    7. 前端分析工具，包括多维分析、查询报表、数据挖掘等。

- **什么是 ETL 工具？其主要功能是什么？**
    数据仓库的集成工具，主要功能包括数据的抽取、清洗、转换、加载、维护。
- **在将数据源的数据加载到数据仓库前需要完成哪些工作？**
    1. 抽取数据 从数据源中选择数据仓库需要的数据。
    2. 清洗数据 消除数据不一致性，统一计量单位，估算默认值等。
    3. 数据转换 将清洗后的数据按照数据仓库的主题进行组织。
    4. 数据加载 将数据装入数据仓库中。

- **简述数据仓库与数据库的差别与联系**
    1. 数据仓库对数据库发展的贡献是将操作型数据处理和分析型数据处理区分开来，使得不同类型的数据处理在不同的数据环境中进行。
    2. 数据仓库与数据库是互补的。数据仓库不是要替代联机事务处理数据库，而是由两者共同组成一个企业的数据库体系化环境。

- **什么是数据集市？它有什么作用？**
    名词解析见 “数据集市”
    体现了分工协作，各负其责的管理理念，满足了企业和部门不同层次，不同范围的管理人员对数据的需求。其特点：
    1. 管理较容易：结构简单，数据增长时易管理
    2. 较灵活：不同的数据集市可以分布在不同的，物理平台上或逻辑的分布于同一物理平台上
    3. 可独立实施：企业人员可以快速获取信息

- **数据集市与数据仓库的区别**
    1. 数据集市时为特定部门的主题域而组织起来的一批数据和业务规则
    2. 构成数据集市的软硬件、数据和应用程序都隶属于不同的部门，这种部门拥有权和管辖权会对不同部门的数据进行协调征程不同程度的干扰。
    3. 一个设计正确的数据仓库，在数据的粒度上应当是多层次的。相反，数据集市则一般只包含综合数据，不会有大量的细节信息。
    4. 数据仓库的数据结构本质上是规范化的。反映了整个企业对数据的需求，而不是某个特定的部门对数据的需求。

- **ODS中的数据有什么特点**
    面向主题的、集成的、可更新的、数据是当前的或接近当前的。

- **什么是 ODS? 简述ODS的功能/ODS 的功能主要是什么？/ODS 的作用是什么？/为什么要引入 ODS？**
    ODS见名词解析。
    1. 在ODS上可以实现企业级OLTP
    企业级OLTP，是指在实际数据处理中一个事务同时涉及多个部门的数据。在面向应用的分散数据库系统中，为了获得快速响应，每个数据库中不可能包含整个企业的完整数据。而ODS中的数据已经是面向企业全局集成的，可快速实现对企业中数据的全局集中管理。
    2. 在ODS上可以实现即时OLAP
    即时OLAP，很多情况下公司中层决策过程并不需要参考太多的历史数据，而主要参考和存取当前和接近当前的数据，并且要求有较快的响应速度。由于此类需求不适宜运行在数据仓库上，这就成了建立ODS的一个主要目的

- **什么是“操作型”处理模式？什么是“信息型”处理模式？二者如何切换？**
    见名词解析

    在系统中设置一个状态切换开关，实现二者的动态切换。

- **ODS 和 DW 的区别是什么？**
    1. 存放的数据不同。
        |ODS|DW|
        |--|--|
        |当前或接近当前的数据|历史数据|
        |细节数据|细节数据和综合数据|
        |可联机更新|不可变快照|
    2. 数据量的等级不同。dw中保存着大量的历史数据，数据量远远大于ods
    3. 技术支持不尽相同。ODS要支持面向记录的联机更新，又要随时保证其数据与源数据库系统中的数据一致。DW中需要之策ETL技术和数据快速存取技术。
    4. 两者面向的需求不同。ODS满足两方面需求，一是企业级OLTP和即时OLAP，二是向DW提供一致的数据环境以供抽取。DW则主要用于高层战略决策。
    5. 二者的使用者不同。ODS使用者主要是企业中层管理人员，DW使用者主要是DSS分析员和高层决策层。

-  **DB～ODS～DW 三层体系结构中，存在着哪两级记录系统？**
    ODS记录系统
    DW记录系统

- **什么是OLAP，它的主要特点是什么？**
    OLAP见名词解析
    特点：
    1. 快速性。用户对OALP的反应能力有很高的要求，系统应在很短的时间内对用户的大部分分析要求做出反应
    2. 可分析性。OLAP系统应能处理与应用有关的各种逻辑分析和统计分析
    3. 多维性。系统必须提供对数据的多维视图和分析，包括对维层次和多重维层次的完全支持。
    4. 及时性。不论数据量有多大，也不管数据存储在何处，OLAP系统应能及时获得信息，并且管理海量信息。

- **OLAP的核心技术有哪些**
    多维数据模型、多维分析操作、多维查询及展示、数据方体技术

- **多维数据模型的核心概念有哪些**
    1. 维
    2. 度量
    3. 数据方体
    4. 数据单元

- **三种常用的多维数据模型是什么？之间有什么区别与联系？**
    三种模型的名词解析
    星型模型的维表规范化后形成雪花模型，
    多个事实表共享一组维表，这种类型于星型模型的集合，称为星系模型

- **星型模型的缺点，怎么改进**
    不支持维的层结构。对于层次比较复杂的维，可以用多张表来描述。

- **雪花模型的缺点，怎么改进**
    雪花模型在执行查询时需要较多的连接操作，影响系统性能。
    折中的解决方式是将星型模型和雪花模型结合起来使用，对大的维表进行规范化以节省存储空间，对小的维表仍然采用星型模型中的不规范形式，以避免由于多表连接引起的性能衰减。

- **多维查询语言 MDX 与结构化查询语言 SQL 有什么异同？**
    MDX语言和SQL语言语法类似，具有SELECT、FROM和WHERE结构。
    SQL返回或操纵的都是二维的，MDX返回和操纵都是多维的。

- **数据方体的存储形式有哪些？及其优缺点？ P74**

    1. MOLAP
        基于多维数组存储的
        优点：
        1. 多维数组表达清晰，占用的存储空间少
        2. 多维数组查找速度快，维护代价小
        3. 多维数组有利于多维计算
        4. 多维数组有利于预综合

        缺点：
        1. 数据稀疏问题

        解决方式：
        可以把维分成稀疏维和紧密维，然后区别对待。
    2. ROLAP
        基于关系表存储的
        优点：
        1. 基于已有的成熟的关系数据库技术，开发成本低
        2. 数据存储容量大，支持的维度多

        缺点：
        1. 数据冗余量大
        2. 比较依赖预综合技术

- **数据仓库中常用的索引类型有哪些？**
    1. 树索引
       1. B树、B*树、B+树
       2. R树
       3. CUBE树
    2. 位图索引
        1. 简单位图索引
        2. 编码位图索引
        3. Projection索引 将某个表的某一列按相同的元组顺序冗余存储。
        4. bit-sliced索引 将projection索引按照二进制形式存储再进行按位分割后形成的每一个列。

- **B树索引和R树索引的主要区别是什么**
    1. R树是针对多维数据的
    2. R树中兄弟之间的矩形边框可以相互重叠

- **举例说明简单位图索引（Bitmap Index）的创建、使用过程**
    有下列数据表，表示顾客的信息表
    |顾客号|姓名|性别|重要级别|
    |--|--|--|--|
    |11|王平|男|3|
    |12|李强|男|5|
    |13|张岚|女|5|
    |14|刘行|男|4|

    在性别列上创建的位图索引
    |男|女|
    |--|--|
    |1|0|
    |1|0|
    |0|1|
    |1|0|

    在重要级别列上创建的位图索引
    |1|2|3|4|5|
    |--|--|--|--|--|
    |0|0|1|0|0|
    |0|0|0|0|1|
    |0|0|0|0|1|
    |0|0|0|1|0|

    这样顾客信息表所有行在性别列的取值构成两个位向量。
    如果要查询“有哪些男性顾客的重要级别为5？”
    根据位图索引，性别为男的列位图为“1101”，重要级别为5的列位图为“0110”
    ，将这两列的位图做按位与的操作，得到“0100”，取出结果为1的行，得出有一个顾客，这个顾客的名字是李强。

- **请简要说明数据仓库设计的步骤。**
    分析主题域, 针对每一个选定的当前实施的主题域
    1. 概念模型设计
        1. 界定系统边界
        2. 确定主题域
    2. 技术准备工作
        1. 技术评估
        2. 技术环境准备
    3. 逻辑模型设计
        1. 粒度层次划分
        2. 数据分割策略
        3. 记录系统定义
        4. 关系模式定义
    4. 物理模型设计
        1. 确定存储结构
        2. 确定索引结构
        3. 确定存放位置
        4. 确定存储分配
    5. 数据仓库生成
        1. 接口设计
        2. 数据装入
    6. 数据仓库运行与维护

- **数据仓库的设计方法与操作型环境中系统设计采用的系统生命周期法有什么不同？**
    操作型环境系统的设计一般采取系统生命周期法：SDLC－Systems Development Life Cycle）
    数据仓库的设计方法：CLDS方法(与SDLC相反)

    SDLC的流程是：
    收集应用需求->分析应用需求->构建数据库->应用编程->系统测试->系统实施

    CLDS的流程是：
    数据仓库建模->数据获取集成->构建数据仓库->DSS应用编程->系统测试->理解需求

- **数据仓库的设计中，存在着哪三级数据模型？**
    1. 概念模型
    2. 逻辑模型
    3. 物理模型

- **数据仓库的设计中提高数据仓库性能的方法和技术有哪些?**
    1. 合并表
    2. 建立数据序列
    3. 引入冗余
    4. 进一步细分数据
    5. 生成导出数据
    6. 建立广义索引
    7. 粒度划分
    8. 分割

### 计算题
**在下面的事务数据库中，关联规则 A$\Rightarrow$C 的置信度和支持度是什么？关联规则 C$\Rightarrow$A
的置信度和支持度又是什么？设 min_sup = 60%，min_conf=80%，频繁项集有哪些？**

|事务号| 项目集|
|--|--|
|1| A，B，C|
|2| A，C|
|3| A，D|
|4| B，E，F|

答：
A$\Rightarrow$C的支持度是 $\frac24$
A$\Rightarrow$C的置信度是 $\frac23$

C$\Rightarrow$A的支持度是 $\frac24$
C$\Rightarrow$A的置信度是 $\frac22$