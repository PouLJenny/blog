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




# EOF