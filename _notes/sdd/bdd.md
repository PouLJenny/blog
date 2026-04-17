## BDD：读这 4 篇就够了

BDD 比较特殊——它是 Daniel Terhorst-North 在 2000 年代初期开创的，2006 年通过一篇博客文章 "Introducing BDD" 正式发表。原始文献不是学术论文，是杂志文章和博客。

### 1. 开山原文（必读）

**Dan North, "Introducing BDD", Better Software Magazine, March 2006**
- 链接：https://dannorth.net/blog/introducing-bdd/
- 无 PDF，是网页文章
- 从 TDD 的困惑出发（不知道从哪开始测、测什么、测试叫什么名字），提出用 "behaviour" 替代 "test"，引入 Given/When/Then 模式

这篇非常短，10 分钟就能读完，但它是整个 BDD 生态的起源。

### 2. BDD 系统综述（推荐，省你读 166 篇的时间）

**Binamungu & Maro, "Behaviour Driven Development: A Systematic Mapping Study", 2023**
- arXiv：2305.05567
- PDF：https://arxiv.org/pdf/2305.05567
- 也发表在 Information and Software Technology (ScienceDirect)
- 覆盖 2006–2021 年发表的 BDD 研究，识别出 166 篇论文做了系统映射

这篇最省时间——读完它你就知道 BDD 这 15 年的学术全景，不用自己去翻那 166 篇。

### 3. BDD 的 IEEE 系统文献综述（补充视角）

**"Behavior Driven Development: A Systematic Literature Review", IEEE Access, 2023**
- DOI：10.1109/ACCESS.2023.3302356
- 系统调查 BDD 对软件开发过程和产品质量的影响，综合近年来 BDD 使用和应用的最新进展
- 精选了 31 篇论文深入分析

### 4. BDD 实证研究（工业界数据）

**Pereira et al., "Behavior-Driven Development benefits and challenges: Reports from an industrial study"**
- 被多篇综述引用的工业实证
- 如果你想知道 BDD 在真实团队里到底好不好使，这篇有工业数据

---

**这篇是你的 BDD/DbC 阅读清单里优先级最高的一篇**——因为它直接把 DbC 的经典概念桥接到了你正在做的事情（Sentinel QA agent、AI agent 行为规范）。Meyer 1992 定义了"软件组件之间的契约"，这篇论文定义了"人类和 AI agent 之间的契约"。

---

## 精简推荐阅读顺序

如果你时间有限，这样排优先级：

**第一梯队（必读，共约 3 小时阅读量）**：

1. **Meyer 1992** "Applying Design by Contract" — DbC 原文，14 页，30 分钟
2. **Dan North 2006** "Introducing BDD" — BDD 原文，网页文章，10 分钟
3. **arXiv:2602.22302** "Agent Behavioral Contracts" — DbC → AI Agent，2026 最新，和你的 Sentinel 直接对接

**第二梯队（省时间的综述）**：

4. **arXiv:2305.05567** "BDD: A Systematic Mapping Study" — 一篇顶 166 篇
5. **Ostroff 2004** "Agile SDD" — TDD + DbC = SDD 的开山之作

**第三梯队（按需深入）**：

6. JML 文档 — 如果想在 Java 里实践 DbC
7. Meyer 1997 书 Part C — 如果想完整理解 DbC 理论
8. IEEE Access 2023 BDD SLR — 如果想要 BDD 的另一个综述视角

对你来说，**Meyer 1992 + Dan North 2006 + Agent Behavioral Contracts 2026** 这三篇构成了一条完整的线：DbC 定义了组件间契约 → BDD 把契约变成人类可读的规范 → ABC 把契约扩展到 AI agent。读完这三篇，你对 sif-dev-kit 的 spec 格式设计会有非常清晰的理论支撑。

