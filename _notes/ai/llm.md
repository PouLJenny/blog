# LLMs

大语言模型

[wiki](https://en.wikipedia.org/wiki/Large_language_model )
[大语言模型历史-中国人民大学](http://ai.ruc.edu.cn/research/science/20230605100.html )
[大语言模型历史-中国人民大学-论文](https://arxiv.org/abs/2303.18223 )
[大语言模型历史-博客](https://juejin.cn/post/7226541360044556343 )
[Quick Start Guide to Large Language Models](https://archive.org/details/quick-start-guide-to-large-language-models-strategies-and-best-practices-for-usi_202407/page/n5/mode/2up?view=theater)
[quick start llms 作者主页](https://sinanozdemir.ai/#publications)

## 大模型公司列表

### 开源


以下是基于2026年3月初主流开源/开放权重（open-weight）大模型的综合排名表格。我综合了多个来源的数据，包括：
- **Hugging Face Open LLM Leaderboard**（客观基准，如MMLU-Pro、GPQA、MATH等）
- **LMArena / Chatbot Arena Elo**（人类偏好盲测）
- **OpenRouter 调用量 / 市占率**（实际生产使用）
- **SWE-bench / LiveCodeBench**（编程/工程能力）
- **其他专业榜单**（如GPQA Diamond、AIME数学等）
当前格局：中国开源模型在多数维度（尤其是性价比、推理、编程、社区采用）全面领先，Llama 4 等 Meta 模型在长上下文有优势但整体掉队。

| 排名 | 模型名称                  | 开发者/公司       | 主要参数规模（总/活跃） | 上下文长度    | 官方/下载 URL (Hugging Face 或官网)                          | 主要优势 & 依据                                                                 | 综合得分参考（Elo / 基准平均） |
|------|---------------------------|-------------------|--------------------------|---------------|-------------------------------------------------------------|---------------------------------------------------------------------------------|--------------------------------|
| 1    | GLM-5                     | 智谱AI (Zhipu)   | ~744B / MoE             | 200K+        | https://huggingface.co/THUDM/glm-5 (或 z.ai 官网)         | 推理/编程/SWE-bench 极强，常居开源トップ；Elo ~1450+，SWE 高分 | ~1450+ Elo, Top1-2 开源       |
| 2    | Kimi K2.5                 | 月之暗面 (Moonshot) | ~1T / MoE               | 262K         | https://huggingface.co/moonshotai/Kimi-K2.5 (kimi.ai)       | 综合最均衡，数学/编程/人类偏好强；OpenRouter 调用量常第1，GPQA/AIME 高 | ~1445-1447 Elo, Top1-3        |
| 3    | Qwen 3.5                  | 阿里通义千问      | 397B / ~170B active     | 262K         | https://huggingface.co/Qwen/Qwen-3.5-397B (qwen.ai)         | 下载量/社区衍生模型爆炸式增长；多模态+性价比王者，GPQA Diamond 88.4% | Top Hugging Face 下载，强基准  |
| 4    | DeepSeek V3.2             | DeepSeek AI      | 685B / MoE              | 长上下文     | https://huggingface.co/deepseek-ai/DeepSeek-V3.2            | 数学/硬核推理最强（AIME/GPQA/FrontierMath）；性价比高 | Top 数学/推理，Elo 高         |
| 5    | MiniMax M2.5              | MiniMax          | ~230B / MoE             | 长上下文     | https://huggingface.co/MiniMax/MiniMax-M2.5                 | 多模态/编程/Agent 强；OpenRouter 市占高 | Top5 常见，编程榜强           |
| 6    | MiMo-V2-Flash / Step-3.5-Flash | StepFun / 其他  | ~196-309B / MoE active 小 | 128K+        | Hugging Face 搜索对应模型                                   | 超高性价比/速度；AIME 94%+，成本仅顶级闭源1/10-1/50 | 性价比/速度 Top               |
| 7    | Llama 4 Maverick          | Meta             | ~400B / 17B active MoE  | 1M-10M       | https://huggingface.co/meta-llama/Llama-4-Maverick          | 超长上下文王者（10M tokens Scout 版更极致）；多模态原生 | 长上下文唯一强项，但 Elo/基准掉队 |
| 8    | Llama 4 Scout             | Meta             | ~109B / 17B active MoE  | 10M tokens   | https://huggingface.co/meta-llama/Llama-4-Scout             | 同上，部署友好（单 H100 可跑） | 长文档/RAG 专用               |


### 闭源

| 排名 | 模型系列 | 厂商 | 官方网站 / 在线对话 | API 开发者入口 |
| --- | --- | --- | --- | --- |
| **1** | **Claude 4.6** | Anthropic | [claude.ai](https://claude.ai) | [console.anthropic.com](https://console.anthropic.com) |
| **2** | **Gemini 3.1** | Google | [gemini.google.com](https://gemini.google.com) | [ai.google.dev](https://ai.google.dev) (AI Studio) |
| **3** | **GPT-5 / 5.1** | OpenAI | [chatgpt.com](https://chatgpt.com) | [platform.openai.com](https://platform.openai.com) |
| **4** | **Grok 4.20** | xAI | [grok.com](https://grok.com) | [console.x.ai](https://console.x.ai) |
| **5** | **豆包 (Doubao)** | 字节跳动 | [doubao.com](https://www.doubao.com) | [volcengine.com](https://www.volcengine.com/product/doubao) (火山引擎) |
| **6** | **文心一言 (ERNIE)** | 百度 | [yiyan.baidu.com](https://yiyan.baidu.com) | [qianfan.baidu.com](https://www.google.com/search?q=https://qianfan.baidu.com) (千帆平台) |
| **7** | **通义千问 (Qwen)** | 阿里巴巴 | [tongyi.aliyun.com](https://tongyi.aliyun.com) | [dashscope.aliyun.com](https://dashscope.aliyun.com) (灵积/百炼) |


## 定义

Large language models (LLMs) are AI models that are usually (but not necessarily) derived from the Transformer architecture and are designed to understand and generate human language, code, and much more


## 工具

### claude code

### codex

### opencode
[官网](https://opencode.ai/ )

### openclaw
[官网](https://openclaw.ai/ )

### Cline
[官网](https://cline.bot/ )

#### Cli

#### jetbrain

#### vs code


## 概念

### Agent

### MCP

### Skills

## 分类

## 提示词


如何写好大模型的提示词

[langchain](https://python.langchain.com/docs/introduction/)

## 微调

### SFT微调
Supervised Fine-Tuning，监督微调


## 论文

下面列出了一些**重要的 LLM（大型语言模型）相关论文及访问地址**，涵盖基础理论、能力研究、安全性、对齐等多个方面：

---

### 📘 基础与核心组件

* **“Attention Is All You Need”**：Transformer 架构的开创性论文，是 LLM 的技术基础。阅读维基百科可快速了解其核心思想与影响 ([blog.csdn.net][1])。
* **“Emergent Abilities of Large Language Models”** (Jason Wei 等, 2022)：首次分析规模扩展带来的“不可预测的新能力”。论文可在 arXiv 查阅 ([arxiv.org][2])。
* **“Understanding the Capabilities, Limitations, and Societal Impact of Large Language Models”** (Tamkin 等, 2021)：对 GPT‑3 的能力与社会影响进行了系统评估 ([arxiv.org][3])。

---

### 📚 综合性综述与调查

* **“A Survey of Large Language Models”** (Zhao et al., 2023)：涵盖预训练、微调、使用方式及评估方式，附资源列表 ([arxiv.org][4])。
* **“Large Language Models: A Survey”** (Minaee et al., 2024)：对 GPT、LLaMA、PaLM 等模型做横向比较，探讨挑战与未来方向，可在 arXiv 下载 PDF ([arxiv.org][5])。
* **“A Comprehensive Overview of Large Language Models”** (2023)：以长文 PDF 形式介绍体系结构、训练策略、推理效率等 ([arxiv.org][6])。
* **“Large Language Models: A Comprehensive Survey … Applications, Challenges …”** (Usman Hadi et al., 2023)：收录应用、局限与未来展望，并提供 GitHub 链接 ([researchgate.net][7])。

---

### 🔒 安全、隐私与对齐

* **“On Large Language Models’ Resilience to Coercive Interrogation”** (Purdue, 2023)：揭示当攻击者能获取 top‑k 概率时的安全漏洞 ([cs.purdue.edu][8])。
* **“Extracting Training Data from Large Language Models”** (Carlini 等, 2021)：展示从 LLM 中提取训练数据的安全风险 ([usenix.org][9])。
* **“DistillSeq: A Framework for Safety Alignment Testing in LLMs via Knowledge Distillation”** (ShanghaiTech, ISSTA 2024)：提出有效测试 LLM 安全对齐的新方法 ([sist.shanghaitech.edu.cn][10])。

---

### 🔍 上下文与长文理解

* **“Lost in the Middle: How Language Models Use Long Contexts”** (Liu et al., 2023)：研究 LLM 在超长上下文中的理解能力 ([cs.stanford.edu][11])。

---

### 🌐 最新模型与技术发展

* **DeepSeek-V3 / DeepSeek-R1**（2024–2025）：开源中文大模型，性能多项对标 GPT‑4，但训练成本低 ([zh.wikipedia.org][12])。
* **盘古‑Σ（Pangu‑Σ）**（2023）：华为研发的 1 T 参数稀疏模型，支持中英双语与代码任务 ([zh.wikipedia.org][13])。

---

### 🔗 资源入口汇总

* **CSDN博客**整合 RAG 等相关技术论文与资源链接 ([blog.csdn.net][1])；
* **GitHub “Awesome‑LLM”**：一个持续更新的大语言模型论文与工具资源合集 ([github.com][14])；
* **知乎专栏**：\[2025.03–04] 选出 10 篇最新 LLM 研究进展，可直接阅读全文 ([zhuanlan.zhihu.com][15])。

---

### 🗂 表格概览

| 方向          | 论文/资源                                          | 链接           |
| ----------- | ---------------------------------------------- | ------------ |
| 基础架构        | Attention Is All You Need                      | Wiki 页面      |
| Emergent 能力 | Emergent Abilities of LLMs (2022)              | arXiv        |
| 综合综述        | Surveys (Zhao et al. 2023; Minaee et al. 2024) | arXiv        |
| 安全对齐        | DistillSeq (ISSTA 2024)                        | ShanghaiTech |
| 长上下文        | Lost in the Middle (2023)                      | arXiv        |
| 最新 LLMs     | DeepSeek‑V3/R1, Pangu‑Σ                        | Wiki 算法模型概览  |

---

如你需要**具体论文的 PDF 下载地址™**，或某篇论文的**中文摘要、解析与应用案例**，欢迎告诉我，我可以继续帮你深入挖掘！

[1]: https://blog.csdn.net/weixin_44885180/article/details/140368817?utm_source=chatgpt.com "大模型论文、github地址汇总原创 - CSDN博客"
[2]: https://arxiv.org/abs/2206.07682?utm_source=chatgpt.com "Emergent Abilities of Large Language Models"
[3]: https://arxiv.org/abs/2102.02503?utm_source=chatgpt.com "Understanding the Capabilities, Limitations, and Societal Impact of Large Language Models"
[4]: https://arxiv.org/abs/2303.18223?utm_source=chatgpt.com "A Survey of Large Language Models"
[5]: https://arxiv.org/abs/2402.06196?utm_source=chatgpt.com "Large Language Models: A Survey"
[6]: https://arxiv.org/pdf/2307.06435?utm_source=chatgpt.com "[PDF] A Comprehensive Overview of Large Language Models - arXiv"
[7]: https://www.researchgate.net/publication/372258530_Large_Language_Models_A_Comprehensive_Survey_of_its_Applications_Challenges_Limitations_and_Future_Prospects?utm_source=chatgpt.com "(PDF) Large Language Models: A Comprehensive Survey of its ..."
[8]: https://www.cs.purdue.edu/homes/cheng535/static/papers/sp24_lint.pdf?utm_source=chatgpt.com "[PDF] On Large Language Models' Resilience to Coercive Interrogation"
[9]: https://www.usenix.org/system/files/sec21-carlini-extracting.pdf?utm_source=chatgpt.com "[PDF] Extracting Training Data from Large Language Models - USENIX"
[10]: https://sist.shanghaitech.edu.cn/2025/0320/c2858a1108422/page.htm?utm_source=chatgpt.com "科研进展| 信息学院系统与安全中心在大语言模型（LLMs）研究方面 ..."
[11]: https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf?utm_source=chatgpt.com "[PDF] Lost in the Middle: How Language Models Use Long Contexts"
[12]: https://zh.wikipedia.org/wiki/DeepSeek-V3?utm_source=chatgpt.com "DeepSeek-V3"
[13]: https://zh.wikipedia.org/wiki/%E7%9B%98%E5%8F%A4%E5%A4%A7%E6%A8%A1%E5%9E%8B?utm_source=chatgpt.com "盘古大模型"
[14]: https://github.com/Hannibal046/Awesome-LLM?utm_source=chatgpt.com "Awesome-LLM: a curated list of Large Language Model - GitHub"
[15]: https://zhuanlan.zhihu.com/p/1891444022985340495?utm_source=chatgpt.com "论文分享| 大语言模型最新进展 - 知乎专栏"


## 榜单

https://onyx.app/open-llm-leaderboard
https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard#/
https://artificialanalysis.ai/



# EOF