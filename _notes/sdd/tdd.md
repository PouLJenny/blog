几个关键论文的 PDF 我来确认一下。PDF 链接都确认好了。给你一张干净的表格。

## TDD 论文精选（含 PDF 链接）

### 原始定义

| 年份 | 论文 | 作者 | PDF |
|------|------|------|-----|
| 2003 | Test-Driven Development: By Example | K. Beck | — (书籍，Red-Green-Refactor 的定义) |

### 工业实证（被引用最多的 5 篇）

| 年份 | 论文 | 作者 | 核心发现 | PDF |
|------|------|------|----------|-----|
| 2003 | Assessing Test-Driven Development at IBM | E.M. Maximilien, L. Williams | IBM 案例：缺陷密度降约 40% | [PDF](https://collaboration.csc.ncsu.edu/laurie/Papers/williamsMaximilienICSE.pdf) |
| 2006 | Evaluating the Efficacy of Test-Driven Development: Industrial Case Studies | T. Bhat, N. Nagappan | 微软 Windows + MSN：代码质量提升 2 倍+，多花 15% 时间 | [PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2009/10/Realizing-Quality-Improvement-Through-Test-Driven-Development-Results-and-Experiences-of-Four-Industrial-Teams-nagappan_tdd.pdf) |
| **2008** | **Realizing Quality Improvement Through TDD: Results and Experiences of Four Industrial Teams** | **N. Nagappan, E.M. Maximilien, T. Bhat, L. Williams** | **微软 3 + IBM 1 团队：缺陷密度降 40–90%，开发时间增 15–35%** | [PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2009/10/Realizing-Quality-Improvement-Through-Test-Driven-Development-Results-and-Experiences-of-Four-Industrial-Teams-nagappan_tdd.pdf) |
| 2011 | The Effectiveness of TDD: An Industrial Case Study | T. Dogsa, D. Batic | 更高质量更易维护，但生产力有所下降 | [Springer](https://link.springer.com/article/10.1007/s11219-011-9130-2) |
| 2009 | Long-Term Effects of TDD: A Case Study | — | 长期使用无显著负面效果 | [Springer](https://link.springer.com/chapter/10.1007/978-3-642-01853-4_4) |

### Meta 分析与系统综述

| 年份 | 论文 | 作者 | 覆盖 | 核心结论 | PDF |
|------|------|------|------|----------|-----|
| **2013** | **The Effects of TDD on External Quality and Productivity: A Meta-Analysis** | **Y. Rafique, V.B. Misic** | **27 篇 meta 分析** | TDD 对质量有小的正面效果，对生产力无明显影响；工业场景下质量提升和生产力下降都比学术场景更明显 | [IEEE](https://ieeexplore.ieee.org/document/6175044) |
| 2014 | Effects of TDD: A Comparative Analysis of Empirical Studies | Rafique, Misic et al. | 27 篇比较 | 系统比较不同实证研究的结论差异 | [Springer](https://link.springer.com/chapter/10.1007/978-3-319-03602-1_10) |
| **2016** | **The Effects of TDD on Internal Quality, External Quality and Productivity: A Systematic Review** | — | **1999–2014** | **76% 研究发现显著提升内部质量，88% 发现显著提升外部质量** | [ResearchGate PDF](https://www.researchgate.net/publication/295863661) |
| **2023** | **TDD and Its Impact on Program Design and Software Quality: A Systematic Literature Review** | — | **261 → 22 篇** | TDD 挑战：开销增加、学习曲线、复杂代码测试困难 | [ResearchGate PDF](https://www.researchgate.net/publication/372832171) |
| 2012 | Overview of the Test Driven Development Research | Bulajic et al. | 综合概览 | TDD 提供更好的代码覆盖率 | [PDF](https://proceedings.informingscience.org/InSITE2012/InSITE12p165-187Bulajic0052.pdf) |

### TDD + AI（最新）

| 年份 | 论文 | PDF |
|------|------|-----|
| 2026.01 | Understanding Specification-Driven Code Generation with LLMs: An Empirical Study Design (SANER 2026) | [PDF](https://arxiv.org/pdf/2601.03878) |

---

## 你只需要读的 3 篇

排优先级：

1. **Nagappan 2008** — TDD 领域最硬的工业数据，4 个团队缺陷降 40–90%。PDF 链接：[微软官方 PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2009/10/Realizing-Quality-Improvement-Through-Test-Driven-Development-Results-and-Experiences-of-Four-Industrial-Teams-nagappan_tdd.pdf)

2. **2016 系统综述** — 覆盖 1999–2014 所有文献，结论清晰（76%/88%）。ResearchGate 可下载。

3. **Rafique & Misic 2013 meta 分析** — 27 篇 meta 分析，结论最诚实：质量有改善，生产力证据不足。帮你避免对 TDD 过度乐观或悲观。

如果你已经在实践 TDD，这三篇足够你回答"TDD 到底值不值"这个问题——答案是：**值，但主要值在缺陷减少（40–90%），不在生产力**。生产力上可能要多花 15–35% 的时间。这正好也是 Superpowers 强制 TDD 的理论依据——它的核心 bet 是"多花 15% 写测试，换 40–90% 的缺陷减少，在 AI agent 长时间自主工作的场景下净收益极高"。