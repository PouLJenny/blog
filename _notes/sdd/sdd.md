# Spec Driven Development 



## SDD 的历史脉络

SDD 的根源可以追溯到很远。1950 年代，Daniel McCracken 的《Digital Computer Programming》就已经鼓励在写代码之前先处理 checkout 问题。到了 1960 年代，NASA 工程师在 Mercury 项目上使用 test-first 技术。

这个方法论在 2004 年被学术界正式形式化，定位为 TDD（测试驱动开发）和 DbC（契约式设计）的结合体。然后在 2020 年代因为 LLM 驱动的 agentic 工作流迎来了文艺复兴。

简单说就是这条线：

**1950s–1960s**：NASA Mercury 项目的 test-first + 早期形式化方法，先验证逻辑再写代码

**1980s–1990s**：形式化方法成熟期——Z 语言、VDM、B 方法。"先写规范再实现"在航空航天、医疗、金融等安全关键领域是标准做法。Bertrand Meyer 的 **Design by Contract**（1986, Eiffel 语言）是直系祖先

**2000s**：TDD（Kent Beck, 2003）+ BDD（Dan North, 2006）。TDD 让验证变成可执行的——先写测试再写代码。BDD 进一步用 "Given–When–Then" 的自然语言对齐开发者和利益相关者的预期行为。两者都把期望变成了可验证的结果——但它们仍然假设人类是唯一参与者

**2004**：SDD 被学术上形式化为 TDD 和 Design by Contract 的融合

**2010s**：OpenAPI/Swagger 驱动的 API-first 开发。这也是 spec-driven 的一种——先写 API spec 再生成代码。还有 Cucumber/Gherkin 的 BDD 框架

**2024–2025**：AI 编码助手爆发，论文说"AI 编码助手的崛起重新点燃了对一个旧想法的兴趣：如果规范——而不是代码——才是软件开发的主要产物呢？"

**2025–2026**：Superpowers、Spec Kit、OpenSpec、Tessl、Kiro 等工具井喷。SDD 从学术概念变成主流实践

## 这一波和以前有什么本质不同？

"Spec Driven Development 这个名字可能暗示它是一种方法论，类似于 Test Driven Development。但这种定位低估了它的重要性"。在 SDD 中，spec 获得了传统上与源代码相关的属性：技术债务、跨团队耦合、兼容性惯性和架构引力。因此，schema 工程成为一等公民的架构学科，和数据建模与分布式系统设计平起平坐。

如今 AI agent 可以设计、编码、测试和重构整个系统。智能不再是瓶颈——意图才是。没有结构，AI 输出是短暂且不一致的。

**一句话总结区别**：以前的 SDD 是"人写 spec，人写代码，spec 帮人思考更清楚"。现在的 SDD 是"人写 spec，AI 写代码，spec 是唯一持久产物"。核心思想没变，但 **spec 的地位从辅助文档变成了真正的源头真相**，因为代码的生产者变了。


## 相关论文


> 更新日期：2026-04-17
>
> 收录标准：以 "Spec-Driven Development" / "Specification-Driven Development" 为题的论文 + SDD 直系祖先论文 + AI 时代 spec/code generation 相关论文。按时间线组织。



### 一、经典基础（1969–2006）

| 年份 | 论文 | 作者 | 核心贡献 | PDF |
|------|------|------|----------|-----|
| 1969 | An Axiomatic Basis for Computer Programming | C.A.R. Hoare | 霍尔逻辑：前置/后置条件证明程序正确性 | [PDF](https://www.cs.cmu.edu/~crary/819-f09/Hoare69.pdf) |
| 1978 | The Algebraic Specification of Abstract Data Types | J. Guttag, J.J. Horning | 代数规范方法 | — |
| 1980 | A Discipline of Programming | E.W. Dijkstra | 程序推导方法，从规范演绎出代码 | — (书籍) |
| 1985 | The B-Book: Assigning Programs to Meanings | J.R. Abrial | B 方法，从规范逐步精化到代码 | — (书籍) |
| 1988 | The Z Notation: A Reference Manual | J.M. Spivey | Z 语言形式化规范 | — (书籍) |
| 1986 | Design by Contract (Eiffel language) | B. Meyer | 契约式设计：前置条件、后置条件、类不变量 | — |
| 1992 | Applying Design by Contract | B. Meyer | DbC 系统化应用指南，IEEE Computer 25(10) | [PDF](https://se.inf.ethz.ch/~meyer/publications/computer/contract.pdf) |
| 1997 | Object-Oriented Software Construction (2nd ed.) | B. Meyer | DbC 经典教材 | — (书籍) |
| 2000 | Combining Formal Specifications with Design by Contract | Helm, Murillo et al. | 形式化规范与 DbC 结合 | [PDF](https://www.researchgate.net/publication/242104581) |
| 2003 | Test-Driven Development: By Example | K. Beck | TDD 经典：先写测试再写代码 | — (书籍) |
| **2004** | **Agile Specification-Driven Development** | **J.S. Ostroff, D. Makalsky, R.F. Paige** | **🏴 SDD 开山论文：TDD + DbC 融合** | [PDF](https://www.eecs.yorku.ca/~jonathan/publications/2004/xp2004.pdf) |
| 2004 | JML: A Notation for Detailed Design | G.T. Leavens, A.L. Baker, C. Ruby | Java 的 Design by Contract 规范语言 | — |
| 2004 | Spec# for C# | M. Barnett et al. | 微软 C# 契约规范系统 | — |
| 2006 | Introducing BDD | D. North | 行为驱动开发，Given/When/Then | [原文](https://dannorth.net/introducing-bdd/) |



### 二、API-First / Contract-First 实践（2011–2025）

| 年份 | 工具/规范 | 核心贡献 | 链接 |
|------|-----------|----------|------|
| 2011 | Swagger (后更名 OpenAPI) | API 先写规范再实现 | [spec](https://spec.openapis.org/oas/v3.1.0) |
| 2011 | Cucumber / Gherkin | BDD 框架，可执行规范 | [docs](https://cucumber.io/docs/) |
| 2020 | Pact Foundation | 消费者驱动的契约测试 | [docs](https://docs.pact.io/) |
| 2025 | Specmatic | 从 API spec 自动生成测试的契约驱动开发 | [site](https://specmatic.io/) |



### 三、AI + 规范的新浪潮（2023–2025）

| 年份 | 论文 | 作者 | 核心贡献 | PDF |
|------|------|------|----------|-----|
| 2023 | nl2spec: Interactively Translating Unstructured Natural Language to Temporal Logics with LLMs | M. Cosler, C. Hahn, D. Mendoza, F. Schmitt, C. Trippel | 用 LLM 把自然语言转成形式化时序逻辑规范 | [PDF](https://arxiv.org/pdf/2303.04864) |
| 2023 | Large Language Models Based Automatic Synthesis of Software Specifications | S. Mandal, A. Chethan et al. | LLM 自动合成软件规范 | — |
| 2024 | Formal Specification Generation with LLMs | Luo et al. | LLM 生成形式化规范 | — |
| 2025 | Evaluating the Ability of LLMs to Generate Verifiable Specifications in VeriFast | W. Fan, M. Rego et al. | 评估 LLM 生成可验证规范的能力 | [PDF](https://arxiv.org/pdf/2411.02318) |
| 2025 | A Short Survey on Formalising Software Requirements with LLMs | VERIFAI 项目 | 35 篇论文综述：Dafny、C、Java 规范生成 | [PDF](https://arxiv.org/pdf/2506.11874) |
| 2025 | Towards Formal Verification of LLM-Generated Code from Natural Language Prompts | A. Councilman et al. | 提出 Formal Query Language 表达用户意图 | [PDF](https://arxiv.org/pdf/2507.13290) |
| 2025 | Leveraging LLMs for Formal Software Requirements: Challenges and Prospects | — | LLM 做形式化需求工程的挑战与前景 | [PDF](https://arxiv.org/pdf/2507.14330) |
| 2025 | Spec2RTL-Agent: Automated Hardware Code Generation from Complex Specifications Using LLM Agent Systems | — | 从硬件 spec 到 RTL 代码的多 agent 系统 | [PDF](https://arxiv.org/pdf/2506.13905) |


### 四、SDD 爆发期（2026.01–2026.04）

| 日期 | 论文 | 作者 | 核心贡献 | PDF |
|------|------|------|----------|-----|
| 2026.01.07 | Understanding Specification-Driven Code Generation with LLMs: An Empirical Study Design | — | TDD 工作流下 LLM 代码生成实验设计，SANER 2026 Registered Report | [PDF](https://arxiv.org/pdf/2601.03878) |
| 2026.01.20 | On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents | — | AGENTS.md 文件对 AI agent 效率的实证影响 | [PDF](https://arxiv.org/pdf/2601.20404) |
| **2026.01.30** | **Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants** | **Deepak Babu Piskala** | **🏴 SDD 系统综述：spec-first / spec-anchored / spec-as-source 三级严格度 + 四阶段工作流 + 决策框架** | [PDF](https://arxiv.org/pdf/2602.00180) |
| **2026.01.31** | **Constitutional Spec-Driven Development: Enforcing Security by Construction in AI-Assisted Code Generation** | **Srinivas Rao Marri** | **🏴 安全约束嵌入 spec 层的 Constitution 概念；CWE/MITRE Top 25 + 监管框架；银行微服务案例** | [PDF](https://arxiv.org/pdf/2602.02584) |
| 2026.02–03 | Codified Context: Infrastructure for AI Agents in a Complex Codebase | — | 复杂代码库中 AI agent 的上下文基础设施 | [PDF](https://arxiv.org/pdf/2602.20478) |
| 2026.02.25 | Agent Behavioral Contracts: Formal Specification and Runtime Enforcement for Reliable Autonomous AI Agents | — | 将 Design by Contract 引入 AI agent：(P, I, G, R) 契约元组 + (p, δ, k)-satisfaction 概率合规框架 | [PDF](https://arxiv.org/pdf/2602.22302) |
| **2026.03.26** | **The Kitchen Loop: User-Spec-Driven Development for a Self-Evolving Codebase** | **Yannick Roy** | **🔥 spec-as-source 的生产验证：specification surface + "As a User ×1000" + Unbeatable Tests + Drift Control。285 迭代、1094 PR、零回归** | [PDF](https://arxiv.org/pdf/2603.25697) |


### SDD 论文阅读清单(2026.05–07 补充)

排序 = 阅读顺序,非时间线。原则:先拿判据,再读方案。

| 序 | 日期 | 论文 | 作者 | 核心贡献 | PDF |
|---|---|---|---|---|---|
| **1** | 2026.07.29 | **SpecFirst: Behavioral Specification Elicitation as a First-Class Step in Agent-Based Program Synthesis from Scratch** | **Yihao Chen 等(Ahmed E. Hassan 组)** | **🔥 唯一有不可伪造 oracle 的:ProgramBench 只给 NL 文档 + 只能执行的二进制当行为判据,前沿模型解出率 &lt;1%。行为规约抽取作为先于实现的一等阶段** | [PDF](https://arxiv.org/pdf/2607.27167) |
| **2** | 2026.06 | **Citation Discipline in Spec-Driven Development: A Cross-Model Empirical Study of Output Determinism and Automated Hallucination Detection** | — | **🔥 这批唯一的跨模型受控实验(Sonnet 4.6 × 240 + GLM-5-turbo × 600)。强制 inline citation 显著降低确定性(d = −0.720);但仅 cited 条件支持自动幻觉检测,TDR 86–88% / FPR 0%,其余三条件全 0** | [PDF](https://arxiv.org/pdf/2606.30689) |
| 3 | 2026.06 | From Prompt to Process: a Process Taxonomy and Comparative Assessment of Frameworks Supporting AI Software Development Agents | — | SDD 框架流程分类学 + 横向对比(Kiro / Spec Kit / BMAD / OpenSpec / Spec-Flow / Spec Kitty)。用于定位坐标系,快速过 | [PDF](https://arxiv.org/pdf/2606.04967) |
| 4 | 2026.05 | LLM-Assisted Repository-Level Generation with Structured Spec-Driven Engineering | Shuzhao Feng, Boqi Chen, Brett H. Meyer, Gunter Mussbacher | 🏴 **唯一过同行评审**(FSE Companion '26)。domain model + Gherkin 规约做仓库级生成;论点:NL prompt 在 SDE 工作流中本身是有损信道 | [PDF](https://arxiv.org/pdf/2605.02455) |
| 5 | 2026.06 | How Much Static Structure Do Code Agents Need? A Study of Deterministic Anchoring | Zhihao Lin, Mingyi Zhou, Yizhuo Yang, Li Li | 🏴 ISSTA 2026 收录。静态锚点的边际收益衰减点 | [PDF](https://arxiv.org/pdf/2606.26979) |
| 6 | 2026.06.25 | The Spec Growth Engine: Spec-Anchored, Code-Coupled, Drift-Enforced Architecture | Hartwig Grabowski(Hochschule Offenburg) | 只读 §5.4 drift 验证 + §5.5 治理闸门分级。spec-code 分歧作为阻塞性合并条件而非自主循环,人力开销远低于 Kitchen Loop。**自出版无验证,仅当设计参考** | [PDF](https://arxiv.org/pdf/2606.27045) |
| 7 | 2026.05 | Reversa: A Reverse Documentation Engineering Framework for Converting Legacy Software into Operational Specifications for AI Agents | Sanderson Oliveira de Macedo, Ronaldo Martins da Costa | 搁置。仅当需要从存量代码反向抽规约时再读 | [PDF](https://arxiv.org/pdf/2605.18684) |

**跳过**:Constitutional SDD(2602.02584,银行微服务安全约束,场景不匹配)、Piskala 综述(2602.00180,分类框架已被 #3 覆盖且更新)

**贯穿七篇的追问**:这套方法的 oracle 从哪来,谁能伪造它?
- Kitchen Loop(2603.25697)→ 作者自己定义 → 零引用的技术原因
- SpecFirst → 不可修改的二进制
- 我的答案必须是:**什么算一个 skill 真的按声明工作,且判据不能由写 skill 的人提供**


ChatGPT补充的

| 序 | 日期 | 论文 | 作者 | 核心贡献 | PDF |
|---:|:---:|---|---|---|:---:|
| **1** | 2026.07.29 | **SpecFirst: Behavioral Specification Elicitation as a First-Class Step in Agent-Based Program Synthesis from Scratch** | Yihao Chen 等<br>Ahmed E. Hassan 组 | 🔥 **目前最直接验证 SDD 核心假设的受控实验。**把“行为规格提取”和“代码实现”拆成两个 Agent 阶段；在 ProgramBench 全部 **200 个任务**、4 个模型上评测。测试通过率提升 **6.9%–21.3%**，行为探索覆盖率提升 **9.4%–18.5%**。 | [PDF](https://arxiv.org/pdf/2607.27167) |
| **2** | 2026.05.28 | **SpecBench: Evaluating Specification-Level Reasoning for Software Engineering LLM Agents** | — | 🔥 **首个面向规格推理能力的真实项目 Benchmark。**基于 Kubernetes、React、Rust、TVM、vLLM 的真实 RFC 和专家 Review，测试 Agent 能否发现规格中的遗漏、歧义和矛盾；最佳 Agent 准确率仅 **44.4%**。 | [PDF](https://arxiv.org/pdf/2605.30314) |
| **3** | 2026.02.10 | **SWE-AGI: Benchmarking Specification-Driven Software Construction with MoonBit** | — | 🔥 **大型端到端规格驱动软件构建基准。**包含 22 个系统级任务，每个任务约需实现 **1,000–10,000 行代码**；覆盖解析器、解释器、二进制解码器和 SAT Solver。最佳结果完成 **19/22** 个任务。 | [PDF](https://arxiv.org/pdf/2602.09447) |
| **4** | 2026.06.28 | **Citation Discipline in Spec-Driven Development: A Cross-Model Empirical Study of Output Determinism and Automated Hallucination Detection** | — | 🔥 **少见的预注册跨模型受控实验。**比较 traceSDD、GitHub Spec Kit 和 OpenSpec；包含 Sonnet 4.6 与 GLM-5-turbo，共 **840 次实现**。强制需求引用后，自动幻觉检测率达到约 **86.4%–88.0%**。 | [PDF](https://arxiv.org/pdf/2606.30689) |
| **5** | 2026.04 | **Does Spec-Driven Development Reduce Defects? An Empirical Test Across 119 Open-Source Repositories** | — | 🔥 **目前样本规模最大的现实项目研究之一。**分析 **119 个仓库、100,247 个 PR**，结合 SZZ 和作者固定效应；没有发现“存在规格即可减少缺陷”的可靠证据，提醒规格可能只是任务复杂度的代理变量。 | [PDF / SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6515898) |
| **6** | 2026.04.07 | **Spec Kit Agents: Context-Grounded Agentic Workflows** | — | 在 Spec Kit 的 Specify、Plan、Tasks、Implement 阶段加入代码库探测和验证 Hook，减少 Agent 编造 API 或违反架构约束。在 **5 个仓库、32 个功能、128 次运行**中评测，并在 SWE-bench Lite 上提升至 **58.2% Pass@1**。 | [PDF](https://arxiv.org/pdf/2604.05278) |
| **7** | 2026.05.01 | **The Productivity-Reliability Paradox: Specification-Driven Governance for AI-Augmented Software Development** | — | 综合 **67 个来源**，提出“生产力—可靠性悖论”：AI 可能提高局部编码速度，却增加 Review、集成和维护成本；提出 SGM 规格治理模型，并进行了四个月的小型试点。 | [PDF](https://arxiv.org/pdf/2605.01160) |
| **8** | 2026.06.03 | **From Prompt to Process: A Process Taxonomy and Comparative Assessment of Frameworks Supporting AI Software Development Agents** | — | 对 Spec Kit、OpenSpec、BMAD、GSD、Spec Kitty、Reversa 进行流程分类和横向比较；提出 Specification、Context、Roles、Execution、Validation、Portability 六维评估框架。 | [PDF](https://arxiv.org/pdf/2606.04967) |
| **9** | 2026.03.17 | **Intent Formalization: A Grand Challenge for Reliable Coding in the Age of AI Agents** | — | 从理论层面提出：AI 编程的核心瓶颈不是生成更多代码，而是把自然语言意图转化为可检查、可验证的规格；连接了 SDD、形式化方法、程序验证和人机交互。 | [PDF](https://arxiv.org/pdf/2603.17150) |
| **10** | 2026.01.31 | **Constitutional Spec-Driven Development: Enforcing Security by Construction** | — | 将不可违反的安全原则写入机器可读的“Constitution”，建立需求—安全原则—代码位置之间的追踪关系；在银行微服务案例中覆盖 10 类 CWE，并报告安全缺陷下降 **73%**。 | [PDF](https://arxiv.org/pdf/2602.02584) |
| **11** | 2026.03.26 | **The Kitchen Loop: User-Spec-Driven Development for a Self-Evolving Codebase** | — | 提出规格表面、合成用户、不可欺骗测试和漂移控制机制；报告在两个生产系统、**285+ 次迭代、1,094+ 个 PR** 中运行。工程案例丰富，但缺少严格对照组。 | [PDF](https://arxiv.org/pdf/2603.25697) |
| **12** | 2026.06.25 | **The Spec Growth Engine** | — | 提出 spec graph、ownership path、vertical slice 增长协议，以及将 spec-code drift 设为阻塞合并条件的 drift gate；架构设计完整，但大规模实证证据较少。 | [PDF](https://arxiv.org/pdf/2606.27045) |
| **13** | 2026.01.30 | **Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants** | — | 提出三种规格严格程度：**Spec-first、Spec-anchored、Spec-as-source**；讨论 BDD、API、企业系统、嵌入式系统和 GitHub Spec Kit，适合作为 SDD 入门综述。 | [PDF](https://arxiv.org/pdf/2602.00180) |
| **14** | 2026.07.18 | **Specification-Driven Development as the Foundation of AI-Native Enterprise Software Engineering** | — | 提出 Specification Governance Reference Model，将规格合同、确定性验证和治理闭环映射到 ISO/IEC 25010；偏企业治理参考模型，原创实证结果有限。 | [PDF](https://arxiv.org/pdf/2607.16680) |
| **15** | 2026.07 | **From Code Review to Spec-Driven Contracts: A Vision for Auditable AIWare Systems** | — | ACM AIware 2026 Vision Paper。提出 specification、execution、audit 三个平面，把规格合同贯穿 CI/CD、运行时和事后审计；已同行评审，但属于短篇愿景论文，暂无系统实证。 | [论文页面](https://openreview.net/forum?id=WC7WAcgZul) |




### 五、重要行业文章（非学术，无 PDF）

| 日期 | 来源 | 标题 | 链接 |
|------|------|------|------|
| 2025.10 | Red Hat Developer | How Spec-Driven Development Improves AI Coding Quality | [链接](https://developers.redhat.com/articles/2025/10/22/how-spec-driven-development-improves-ai-coding-quality) |
| 2025.11 | **Thoughtworks Radar** | Spec-Driven Development（列入 Assess 阶段） | [链接](https://www.thoughtworks.com/radar/techniques/spec-driven-development) |
| 2026.01 | InfoQ | Spec Driven Development: When Architecture Becomes Executable（提出 SpecOps） | [链接](https://www.infoq.com/articles/spec-driven-development/) |
| 2026.02 | InfoQ | Spec-Driven Development – Adoption at Enterprise Scale | [链接](https://www.infoq.com/articles/enterprise-spec-driven-development/) |
| 2026.03 | Martin Fowler's blog | Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl | [链接](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) |



### 六、推荐阅读顺序

针对 sif.com 的目标（spec-as-source + 可重新生成代码），优先级排序：

1. **The Kitchen Loop** (arXiv:2603.25697) — 最新、最接近目标、有生产数据
2. **Piskala 综述** (arXiv:2602.00180) — 全景图 + 三级严格度定义 + 决策框架
3. **Ostroff 2004** (XP 2004) — SDD 开山之作，理解根基
4. **Constitutional SDD** (arXiv:2602.02584) — Constitution 概念直接可用于 sif 安全约束
5. **Agent Behavioral Contracts** (arXiv:2602.22302) — 与 Sentinel QA agent 设计对接
6. **AGENTS.md 效率实证** (arXiv:2601.20404) — 验证 CLAUDE.md/AGENTS.md 方法的有效性
7. **Meyer 1992** — DbC 原文，永恒经典




## 我已经读过的Paper

1. [Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl](./papers/sdd-3-tools-bilingual.html)
    - 这个是Birgitta Böckeler在MartinFowler.com上面发表的文章，定义了三种不同的Spec级别
    - spec-first、spec-anchored、spec-as-source 三个级别
    - 讨论了kiro、spec kit、tessl 三个工具的特点
2. [Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants](./papers/spec-driven-development-bilingual.html)
    - EARS 语法，写单条需求 [ears 定义](https://alistairmavin.com/ears/)
        - [ears语法定义](./papers/ears-bilingual.html)
        - ears提出时的论文 [Easy Approach to Requirements Syntax (EARS)](./papers/EARS_bilingual.html)
    - Gherkin 语法 BDD写用户故事的语法 [cucumber](https://cucumber.io/docs/) 
    - Specify -> Plan -> Implement -> Validate
        - Specify: 软件应该做什么？
        - Plan: 我们该怎么构建它？
        - Implement: 拆解成一个个小任务实现
        - Validate: 在单元、集成和验收三个层级运行自动化测试
3. [Kitchen Loop](./papers/kitchen-loop-bilingual.html)
    - 这个论文讲述了一种自动迭代产品的方法论，我个人觉得很好。
    - 3层策略模式 Foundation 30% 简单的基线 -- Composition 50% 把两个或更多的功能以创造性的方式组合起来 -- Frontier 20% 故意触碰产品当前能力边界外的事
    - 4层测试框架 unit 孤立的逻辑、计算 -> api/adapter  -> integration 完整执行流水线  -> e2e scenario 完整用户旅程
    - 覆盖矩阵 N个功能 、M个平台、K种动作类型
    - 反信号哨兵： 测试本身的测试 anti-signal canaries
      1. 明显错误的 任何门都应该抓到的明显结构或事实错误
      2. 影子型 事实上是真的，但是已过期、新颖度低或低于阈值
      3. 对抗型 真实数据 + 错误结论 -- 能骗过确定性检查和LLM检查
      4. 真假混合 一条信号里掺真假数据
4. [XP 2004 sdd 开山之作](./papers/sdd-xp2004-bilingual.html)
    - 其实这个论文就是说了怎么使用sdd，但是这个想法很早就提出来了，AI之前没什么人用，AI来了之后这个想法直接起飞
5. [SpecFirst](./papers/spec-first_bilingual.html)
    - 这个论文讲的是提供二进制程序+描述文件，让ai根据这些条件再写一个相同的程序的方法。对我来说没啥用
6. [Citation Discipline in Spec-Driven Development](./papers/citation-discipline-sdd-bilingual.html)
    - 这个论文讲的是我们如何验证智能体写出的代码确实实现了规约所要求的内容?并对比了traceSDD、Spec Kit、OpenSpec这三种框架
    - 结论是OpenSpec貌似更牛逼一些，这个到时候我得看看
7. [Test-Driven AI Agent Definition (TDAD): Compiling Tool-Using Agents from Behavioral Specifications](./papers/TDAD_bilingual.html)
    - 这个是通过测试驱动的方式生成AI Agent的感觉对我没啥用

## sdd落地方案

### 需求讨论阶段

#### 四层规范法：术语表 / 规则层 / 例子层 / 测试用例层

用于 AI + 人协作编码的需求确认阶段。分层依据是**逻辑形式不同**，一种记法只能高效表达一种形式。

| 层 | 逻辑形式 | 回答 | 记法 |
|---|---|---|---|
| 术语表 | 定义 | 名词指什么 | 谓词式定义 |
| 规则层 | 全称 ∀ | 任何情况下必须成立什么 | EARS |
| 例子层 | 存在 ∃ | 具体输入下是什么样 | Gherkin |
| 测试用例层 | 验证（∀ 的有限证据） | 跑哪些才算验过 | 结构化用例表 |

前三层是**声明**，第四层是**穷举**——∀ 无法直接执行，只能靠一组有限的实例去逼近。因此前三层由人写、是源头真相，第四层由 AI 从前三层机械展开、人评审后冻结。

贯穿示例：优惠券下单。

---

#### 一、术语表

AI 的猜测有一大半来自名词歧义，不是逻辑缺失。

##### 定义形式：种差 + 属

定义是**名词短语，不是句子**。中文里属是中心语、永远在最后，种差在前面做定语：

```
可用优惠券
  ①状态为未使用、②当前时刻处于有效期内且③未被占用的 优惠券
  └────────────────── 种差 ──────────────────┘  └── 属 ──┘
```

- **属**：最近的上位概念。必须是本表已有术语，或显式声明为根概念
- **种差**：在同属的兄弟中把本概念划出来所需的**最少**条件

判据：删掉某条种差，会不会有别的东西被误收进来？不会 → 它是描述，进注释，不进定义。

##### 三条硬约束

| 约束 | 理由 |
|---|---|
| 属链 ≤ 3 层 | 模型需累加各层种差才得到完整内涵，链一深就漏继承项 |
| 种差逐条编号 ①②③ | 供规则层引用，把"漏实现某条种差"变成可检查 |
| 属必须是表内术语 | 挡住 AI 偏好抽象属（"对象""信息"）导致的种差膨胀与重复 |

##### 样例

```
优惠券
  ①由营销活动发放、②归属指定用户、③可在下单时抵扣订单金额的 电子凭证【根】
  例（非穷举）：满 100 减 10 的品类券
  注 1：本表中优惠券均为一次性使用。
  注 2：平台直降、限时折扣作用于商品价格，不属于优惠券。

可用优惠券
  ①状态为未使用、②当前时刻处于有效期内且③未被占用的 优惠券
  注 1：有效期为左闭右开区间。
  注 2：金额门槛不属于本概念的种差，见「可核销」。

优惠券占用（允许：锁券；弃用：冻结）
  ①施加于下单流程期间、②具有超时时限的、作用于可用优惠券的 排他锁【根】
  注 1：占用期间券的状态字段仍为未使用。

可核销
  ①券本身可用、②订单实付前金额不低于其门槛金额的 性质【根】
  注 1：可用是券的单方属性，可核销是券与订单的二元关系。
  例（非穷举）：门槛 100 的券对 99.99 元订单不可核销。

核销
  ①将可核销优惠券的面额从订单金额中扣减、②将其状态置为已使用的 不可逆操作【根】
```

##### 外延补充：两种写法不可混用

判据：**增加一个成员，算不算改定义？**

| | 开放概念 | 封闭枚举 |
|---|---|---|
| 权威源 | 种差 + 属 | 受控列表 |
| 外延的写法 | `例（非穷举）：…` | 注释中给**完整**列表 + 变更控制句 |
| 漏写的后果 | 模型把例子当成完整值域 | 模型自行归纳内涵、补出不存在的值 |

```
支付状态
  取值于固定集合的、标识订单资金流转所处阶段的 状态标识【根】
  注 1：取值为 待支付 / 支付中 / 支付成功 / 支付失败 / 已关闭。
  注 2：取值集合固定，新增须修订本条目。
```

"例"在标准里是**取样**，天然不完备，不得用于承载封闭枚举的值域。

##### 注释的边界

注释存在的唯一理由是**保护定义**——把有用但不划界的信息挡在定义之外。三问筛选：

1. 删了会有东西被误收进来吗？会 → 它是种差，该进定义
2. 说的是"这个词指什么"还是"系统该怎么做"？后者 → **出词表，进规则层**
3. 在帮读者区分本词与某个近邻词吗？是 → 留，这是注释最高价值的用法

第 2 条最常被违反：注释是自由文本，词表会慢慢变成需求的垃圾抽屉。"超时后占用自动失效""退款不撤销核销"这类都是规则，不是定义。

---

#### 二、规则层（EARS）

五个句式模板，主语固定为系统：

| 类型 | 模板 | 用途 |
|---|---|---|
| Ubiquitous | The `<系统>` shall `<响应>` | 无条件不变式 |
| State-driven | While `<状态>`, the `<系统>` shall `<响应>` | 状态持续期间 |
| Event-driven | When `<触发>`, the `<系统>` shall `<响应>` | 事件触发 |
| Unwanted | If `<异常>`, then the `<系统>` shall `<响应>` | 非期望路径 |
| Optional | Where `<特性启用>`, the `<系统>` shall `<响应>` | 可选特性 |

主语被钉死为系统、`shall` 后只能跟可验证响应，句子里没有叙事余地——这是它能表达 ∀ 而 Gherkin 不能的原因。

```
R-001 [Ubiquitous]   系统应保证订单实付金额不小于 0。
R-002 [Ubiquitous]   系统应保证一张优惠券在任一时刻至多被一个订单占用。
R-003 [Event-driven] 当用户提交订单时，系统应校验所携优惠券为"可用优惠券"且满足其门槛。
R-004 [Unwanted]     若优惠券已被其他订单占用，系统应拒绝下单并返回 COUPON_LOCKED。
R-005 [Unwanted]     若支付超时未回调，系统应释放优惠券占用并将订单置为已取消。
R-006 [State-driven] 在订单处于"支付中"期间，系统应拒绝对该订单的任何优惠券变更请求。
```

##### 三个要点

1. **Unwanted 型是最大收益点。** 异常与非法路径是 AI 漏得最多的地方（训练数据中 happy path 占绝对多数）。单独给它一个模板，等于强制逐条列举"什么情况下不能做什么"。
2. **不变式必须显式带时间量词。** R-002 的"任一时刻"不能省；省掉后 AI 会实现成"下单时检查一次"，并发下直接超卖。
3. **每条规则一个 ID。** 与第三层的连接件，也是覆盖率检查的基础。

##### 最常见的失败模式

规则层写成伪代码。`shall` 后面必须是**外部可观测行为**。一旦出现"系统应遍历优惠券列表逐个校验"，就已经在做设计而非写规范——这会锁死 AI 的实现空间，且通常锁错。

---

#### 三、例子层（Gherkin）

职责限定为一件事：**消歧**。完整性由规则层负责，例子层不承担。

##### 英文关键词 + 中文描述

关键词一律用英文，描述、场景标题、数据一律用中文。三条理由：

1. **中文关键词是 i18n 方言，靠文件首行 `# language: zh-CN` 声明才生效**——漏写一行，整个文件解析失败，且报错信息指向的是步骤而不是缺失的声明
2. **工具真正消费的结构本就与语言无关**：`@tag`、`<占位符>`、`Examples` 表头、Data Table 分隔符在任何方言下都是同一套符号。关键词换成中文只是在这套骨架上多加一层映射，徒增出错面
3. **英文关键词在模型语料中占绝对多数**，AI 对 `Given/When/Then` 的结构识别远稳于「假如/当/那么」

中文该出现的地方是领域名词——那是术语表的落点，不是关键词的位置。

##### 完整语法模版

注意模版里所有注释都**独占一行**。Gherkin 没有行尾注释——`When 用户提交订单   # 说明` 会把 `# 说明` 整段吞进步骤文本，而不是被忽略。

```gherkin
# 文件：features/coupon_redeem.feature
# 无 language 声明即默认 en。中文只出现在描述、标题与数据里。

# Feature 级 tag，向下继承给所有 Rule 与 Scenario
@domain-coupon
# 一个文件恰好一个 Feature，标题是名词短语，取自术语表
Feature: 优惠券核销
  # Feature 描述：自由文本，不被解析器消费，只给人读
  作为 下单用户
  我希望 在提交订单时抵扣优惠券
  以便 减少实付金额

  # 所有 Scenario 的公共前置，只放 Given
  Background:
    Given 存在用户"张三"
    And 存在一张"可用优惠券"C1，面额 10

  # Rule 是 Gherkin 6+ 的规则分组，一个 Rule 承载一条 EARS 规则
  Rule: R-003 提交订单时校验优惠券可用且满足门槛

    # Example 是 Scenario 的同义词，全文件只用其中一个
    Example: 门槛恰好满足
      Given 优惠券 C1 的门槛为 100
      # 每个 Scenario 恰好一个 When
      When 用户提交实付前金额为 100 的订单
      Then 核销成功
      # And 续接上一步的类型，此处仍是 Then
      And 订单实付金额为 90

    # Scenario 级 tag，用于筛选执行
    @boundary
    # 同一逻辑、多组数据时才用 Outline
    Scenario Outline: 门槛边界
      Given 一张"可用优惠券"，门槛为 <门槛>，面额 10
      When 用户提交实付前金额为 <金额> 的订单
      Then 结果应为 <结果>

      # Examples 表头必须与 <占位符> 逐字一致；第二行取等号成立
      Examples: 门槛取等号与其两侧
        | 门槛 | 金额   | 结果       |
        | 100  | 99.99  | 门槛不满足 |
        | 100  | 100    | 核销成功   |
        | 100  | 100.01 | 核销成功   |

  Rule: R-004 券被其他订单占用时拒绝下单

    @unwanted
    Scenario: 券已被其他订单占用
      Given 优惠券 C1 已被订单 O9 占用
      When 用户提交携带 C1 的订单
      Then 下单被拒绝
      And 错误码为 COUPON_LOCKED
      # But 语义完全等同 And，仅供人读出转折
      But 优惠券 C1 的状态仍为未使用

  Rule: R-005 支付超时释放优惠券占用

    Scenario: 支付超时后释放占用
      Given 订单 O1 处于"支付中"且已占用 C1
      When 支付回调超时
      # DocString：多行文本参数，缩进以起始三引号为基准
      Then 收到如下事件:
        """
        {"event": "coupon.released", "coupon": "C1"}
        """
      # Data Table：步骤级表格参数，与 Examples 不是一回事
      And 订单状态变更如下:
        | 字段     | 变更前 | 变更后 |
        | 订单状态 | 支付中 | 已取消 |
```

##### 关键词对照

| 关键词 | 作用 | 约束 |
|---|---|---|
| `Feature:` | 文件根节点 | 一文件恰好一个；标题是名词短语，取自术语表 |
| `Rule:` | 规则分组（Gherkin 6+） | 一个 Rule 对应一条 EARS 规则，标题以 R-ID 开头 |
| `Background:` | 公共前置 | 只放 `Given`；超过 4 行说明领域没抽干净 |
| `Scenario:` ｜ `Example:` | 单个例子 | 同义词，全文件统一用其中一个 |
| `Scenario Outline:` ｜ `Scenario Template:` | 参数化例子 | 必须配 `Examples`，否则解析失败 |
| `Examples:` ｜ `Scenarios:` | 数据表 | 表头与 `<占位符>` 逐字一致，空格也算 |
| `Given` / `When` / `Then` | 前置 / 动作 / 断言 | 每个 Scenario 恰好一个 `When` |
| `And` / `But` | 续接上一步的类型 | `But` 语义等同 `And`，只为可读性 |
| `*` | 通配步骤 | 仅列表式步骤用，不推荐——它抹掉了前置与断言的区分 |
| `"""` ｜ ` ``` ` | DocString | 多行文本参数，缩进以起始引号为基准 |
| `\|` | Data Table | 步骤级表格参数，与 `Examples` 不是一回事 |
| `@` | 标签 | 可打在 Feature / Rule / Scenario / Examples 上，向下继承 |
| `#` | 注释 | 必须独占一行，行尾注释不被识别 |

##### 四条写作约束

1. **R-ID 主挂在 `Rule:` 块上**（`Rule: R-003 …`）。一个场景跨多条规则时，才额外补 `@R-004` 这样的 tag——`Rule:` 关键词天然就是规则分组，比给每个 scenario 打 tag 更不易漏
2. **一条规则至少三个例子**：典型值、边界值、越界值
3. **一个 Scenario 恰好一个 `When`**。一个 When = 一个被测行为；出现第二个 When，说明这里其实是两个场景，或者你在描述流程而不是举例
4. **步骤里不出现 UI 词与实现词**（「点击提交按钮」「调用 CouponService」）。只写外部可观测行为——与规则层「写成伪代码」是同一个病

**反向诊断**：一条规则举不出边界例子 → 该规则本身有歧义，回第二层改。

上面 `100` 取等号那一行，是"满足门槛"四个字唯一的消歧手段。

---

#### 四、测试用例层

规则层给**义务**，例子层给**样本**，用例层给**清单**——回答"跑哪些才算验过"。

**唯一的硬约束：用例层不引入任何新需求。** 展开过程中冒出了前三层没有的信息，说明规则层漏了，回第二层补，而不是在用例表里就地补一行。这条守不住，用例表就变成需求的第二个垃圾抽屉（与术语表「注释三问」的第 2 条同构）。

##### 三个来源：生成是机械的，不是创作的

| 来源 | 展开动作 |
|---|---|
| 例子层直采 | 每个 `Scenario` → 1 条用例；`Scenario Outline` 的 `Examples` **每一行** → 1 条用例 |
| 规则层展开 | 每条 R-ID 按下方 EARS 矩阵逐格补齐 |
| 术语表展开 | 封闭枚举的每个取值 ≥ 1 条；每条编号种差 ①②③ ≥ 1 条「违反该种差」的负向用例 |

第三条是最容易被跳过、收益却最高的：「可用优惠券」有三条种差，就必然存在三种「不可用」——已使用、已过期、被占用。不逐条展开，AI 通常只实现第一条。

##### 按 EARS 类型的展开矩阵

这张表把"生成完整用例"从判断题变成查表动作：

| EARS 类型 | 必须展开出的用例 |
|---|---|
| Ubiquitous | 正向 1 + 试图破坏该不变式的负向 ≥ 1（含并发、重试路径） |
| State-driven | 状态内 1 + 状态外 1 + 进入/离开状态的边界各 1 |
| Event-driven | 触发 1 + 未触发 1 + 重复触发（幂等）1 |
| Unwanted | 异常触发 1 + 错误码断言 1 + 异常后系统状态未被污染 1 |
| Optional | 特性开 1 + 特性关 1 |

Unwanted 那一行的第三格最容易漏：拒绝了不等于没留下脏数据。

##### 用例表字段

| 字段 | 含义 | 约束 |
|---|---|---|
| TC-ID | `TC-<R-ID>-<序号>` | 全局唯一；规则内容改了，ID 不变 |
| R-ID | 所验证的规则 | 必填，可多条 |
| 来源 | 例子直采 / 规则展开 / 术语展开 | 评审时据此定位"哪些是 AI 补的" |
| 类型 | 典型 / 边界 / 越界 / 并发 / 异常 / 幂等 | 与展开矩阵对应 |
| 层级 | 单元 / 集成 / 验收 | 决定谁跑、多久跑一次 |
| 前置 | 用术语表名词描述的初态 | 不写实现细节 |
| 输入 | 触发动作 + 参数 | — |
| 期望 | 外部可观测结果，含错误码或状态字段 | 一条用例一个期望簇 |

##### 样例

| TC-ID | R-ID | 来源 | 类型 | 层级 | 前置 | 输入 | 期望 |
|---|---|---|---|---|---|---|---|
| TC-002-1 | R-002 | 规则展开 | 并发 | 集成 | 可用优惠券 C1 未被占用 | 两个订单同时提交并携带 C1 | 恰好一个成功占用，另一个返回 COUPON_LOCKED |
| TC-002-2 | R-002 | 规则展开 | 典型 | 单元 | C1 未被占用 | 单订单提交携带 C1 | 占用成功，C1 状态仍为未使用 |
| TC-003-1 | R-003 | 例子直采 | 越界 | 单元 | C1 门槛 100、面额 10 | 实付前金额 99.99 | 门槛不满足，不核销 |
| TC-003-2 | R-003 | 例子直采 | 边界 | 单元 | 同上 | 实付前金额 100 | 核销成功，实付 90 |
| TC-003-3 | R-003 | 例子直采 | 典型 | 单元 | 同上 | 实付前金额 100.01 | 核销成功 |
| TC-003-4 | R-003 | 术语展开 | 异常 | 单元 | C1 状态为已使用（违反种差①） | 提交订单携带 C1 | 拒绝，券不可用 |
| TC-003-5 | R-003 | 术语展开 | 边界 | 单元 | C1 有效期右端点恰好到达（违反种差②） | 提交订单携带 C1 | 拒绝——有效期为左闭右开 |
| TC-004-1 | R-004 | 例子直采 | 异常 | 集成 | C1 已被订单 O9 占用 | 提交订单携带 C1 | 下单被拒，错误码 COUPON_LOCKED |
| TC-004-2 | R-004 | 规则展开 | 异常 | 集成 | 同上 | 同上 | 拒绝后 C1 仍归 O9 占用，未产生新占用记录 |
| TC-005-1 | R-005 | 例子直采 | 异常 | 验收 | 订单 O1 支付中且占用 C1 | 支付回调超时 | 释放占用，O1 置为已取消，C1 恢复可用 |
| TC-005-2 | R-005 | 规则展开 | 幂等 | 集成 | O1 已因超时取消 | 超时事件重复投递 | 无二次状态变更，C1 不被重复释放 |

##### 三个失败模式

1. **用例写成实现步骤**（`调用 CouponService.check()`）——与规则层写成伪代码是同一个病。前置和期望都必须停在外部可观测的层面
2. **AI 一次生成后不评审**。模型稳定漏 Unwanted 与并发两类。评审不必通读——只盯「来源 = 规则展开」的那些行，这是设「来源」字段的全部理由
3. **期望写成"成功 / 失败"**。必须写到具体错误码或状态字段，否则用例无法证伪，跑绿了也不说明任何事

---

#### 五、可机械检查的连接

把"规范质量"变成 CI 能跑的东西——这是整套方法的真正价值。

1. **词汇闭包**：规则层 + 例子层 + 用例层的领域名词 ⊆ 术语表
2. **规则覆盖**：每条规则 ID ≥ 1 个 scenario 引用
3. **无孤儿场景**：每个 scenario ≥ 1 条规则引用
4. **用例覆盖**：每条规则 ID ≥ 1 条 TC；Unwanted 型规则额外要求 ≥ 1 条带错误码断言的 TC
5. **例子直采完整性**：每个 `Examples` 数据行 ≥ 1 条对应 TC——漏采就是悄悄砍掉了一个已经写好的边界
6. **无孤儿用例**：每条 TC ≥ 1 条规则 ID

第 3 条是反向的：人写例子比写规则自然，孤儿场景意味着**存在一条你没写出来的规则**，会持续暴露规则层的空洞。

第 6 条是"用例层不引入新需求"的机械形式。孤儿用例和孤儿场景指向同一件事——你脑子里有一条规则，但它没被写下来。

---

#### 六、交给 AI 时

**明说优先级**：术语 > 规则 > 例子 > 用例。冲突一律以规则为准；例子是规则的**实例**、用例是规则的**投影**，两者都不是**补充**。不说这句，模型会把例子和用例当成需求全集。

**第一步不要写代码**，先让它输出两样：

1. 规则层中发现的歧义
2. 它准备自行假设的点

这份假设清单就是规范的漏洞报告，比自查有效——它暴露的正是模型实际会填的坑。

**前三份文件 AI 只读不写。** 改由人来改。第四份（用例表）由 AI 生成、人评审后冻结——评审通过之前，不得据其写实现。

---

#### 七、适用边界

判据：**改错的代价 > 写规范的代价** 才做。一个中等复杂度领域约需 2–3 小时起步。

| | 场景 |
|---|---|
| 不值得 | CRUD、表单、后台列表、内部工具 |
| 值得 | 计费、权限、状态机、库存/额度、对账，以及任何涉及并发或涉及钱的地方 |

不值得的部分直接口头描述让 AI 写，返工一次也比写规范便宜。


### 需求工程

进入AI时代，想跟AI讨论清楚需求就得用一些方法论的东西把需求梳理清楚。
1. 把需求探索清楚、明白，从人脑子里面把需求挖掘明白
2. 输出结构化的文档，方便AI分析


#### 相关论文

1. [Four Dark Corners of Requirements Engineering](./papers/four-dark-corners-of-requirements-engineering.html)


### 测试的作用

1. [文章-Mutation Testing for AI-Generated Code: A Practical Guide](./papers/mutation-testing-ai-generated-code-bilingual.html) 原文 https://www.augmentcode.com/guides/mutation-testing-ai-generated-code
  - 主要讲变异测试在AI中的作用，但是这个对算法密度比较高的场景比较适用，如果链接DB、Redis、HTTP场景的话
2. [文章-Reviewing AI-Generated Code: A Verification Discipline for the Loop](./papers/reviewing-ai-generated-code-bilingual.html)  原文 https://www.augmentcode.com/guides/reviewing-ai-generated-code
  - 在loop里面加入渐进式交付
  - 在loop里面加入裁判 （编译器、diff、测试套件）
  - 把验证当作工程循环内部的一项正式纪律，而不是合并前的一次扫读
  - 一个初级工程师生成代码的速度，已经快过一个资深工程师批判性审计它的速度
  - Diff-scoped SAST  静态应用安全测试

# EOF