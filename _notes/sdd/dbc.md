



## DbC：读这 5 篇就够了

DbC 的文献链比 BDD 清晰得多——从 Meyer 的原始论文一直到 2026 年的 AI agent 版本，一条直线。

### 1. DbC 原始论文（必读）

**Bertrand Meyer, "Applying Design by Contract", IEEE Computer, vol.25(10), 1992**
- PDF：https://se.inf.ethz.ch/~meyer/publications/computer/contract.pdf
- 这是 DbC 的正式定义：前置条件、后置条件、类不变量。14 页，半小时可以读完

### 2. DbC 经典教材（选读，如果想深入）

**Bertrand Meyer, "Object-Oriented Software Construction", 2nd Edition, Prentice Hall, 1997**
- 书籍，1200+ 页，不用全读
- 重点看 Part C "Doing It Right"（第 11–16 章），这里是 DbC 理论的完整展开
- 如果只想快速了解精华，读 1992 论文就够

### 3. DbC for Java（JML，和你的技术栈相关）

**Leavens, Baker & Ruby, "JML: A Notation for Detailed Design", 1999/2006**
- 链接：https://www.cs.ucf.edu/~leavens/JML/
- JML 是 Java 的 Design by Contract 实现
- 你用 JDK 17，虽然 JML 在现代 Java 不主流了，但它的**思想**（用注解表达前置/后置条件）直接可以映射到你的 spec 设计

### 4. 形式化方法综述（帮你理解 DbC 在更大图景中的位置）

**"Formal Methods in Requirements Engineering: Survey and Future Directions"**
- PDF：https://lorchrob.github.io/publications/re_survey_paper.pdf
- 把 DbC 放在形式化方法的大谱系里，帮你理解 DbC、Z 语言、B 方法、模型检测之间的关系

### 5. DbC → AI Agent（2026 最新，强烈推荐）

**"Agent Behavioral Contracts: Formal Specification and Runtime Enforcement for Reliable Autonomous AI Agents", arXiv:2602.22302, 2026.02**
- PDF：https://arxiv.org/pdf/2602.22302
- 把 Design by Contract（Meyer, 1992）原则引入自治 AI agent。定义了 C = (P, I, G, R) 契约元组——前置条件、不变量、治理策略、修复策略。引入 (p, δ, k)-satisfaction 概率合规框架来处理 LLM 的非确定性
