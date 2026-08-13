# Transformer



## 论文

以下是关于 **Self-Attention 与 Transformer** 的核心论文及其访问地址，涵盖原始理论、效率提升与解释性研究：



### 1. Transformer 基石

* **Attention Is All You Need**（Vaswani 等，2017）
  提出 Transformer 架构，首次使用 self-attention 完全替代 RNN/CNN。原文 PDF 可读于 NeurIPS 资源库。
  👉 arXiv/NeurIPS PDF (paper) ([arxiv.org][1], [papers.neurips.cc][2])
* 中文维基/翻译介绍与解读文章：

  * 中文 Wiki“注意力就是你所需要的一切” ([zh.wikipedia.org][3])
  * 英文 Wiki 概览 Transformer 架构 ([blog.csdn.net][4])


[讲解注意力的视频](https://www.bilibili.com/video/BV1TZ421j7Ke/?spm_id_from=333.1387.search.video_card.click&vd_source=973c7d5ced4869eb290f9a3842143b40)



### 2. 视觉化与解读资源

* **The Illustrated Transformer / Self‑Attention**
  较直观展示 Transformer 架构与 self‑attention 机制，深受社区推崇。多位网友推荐 “Illustrated: Self-Attention” ([reddit.com][5])
* 各类中文详细解读与博文：

  * CSDN 与 知乎 等平台详解 Transformer 结构与 self‑attention ([blog.csdn.net][4])



### 3. 升效与扩展方向研究

* **Linformer: Self-Attention with Linear Complexity**（Wang 等，2020）
  提出通过低秩近似，将 self-attention 的复杂度由 $O(n^2)$ 降为 $O(n)$。很适合处理长序列 ([arxiv.org][6])
* **Nyströmformer**（Xiong 等，2021）
  基于 Nyström 方法推进近似 self-attention，同样达成线性时间复杂度，适应长文本 ([arxiv.org][7])
* **Theoretical Limitations of Self-Attention**（Hahn，2019）
  探讨 self-attention 在表达形式语言结构上的理论边界，例如其对层数/head 数的依赖 ([arxiv.org][8])



### 4. 可解释与因果视角

* **Causal Interpretation of Self-Attention in Pre‑Trained Transformers**（2023）
  从结构方程模型（SEM）的角度解析 pre-trained transformers 中 self-attention 的因果意义 ([arxiv.org][9])



### 📚 附加背景阅读

* **Wired 长文** 融合了 Transformer 团队在 Google 成立和 self-attention 概念起源的精彩描述 ([wired.com][10])
* **TechRadar 科普文章** 总览了 Transformer 在 AI 中如何脱颖而出 ([techradar.com][11])

### karpathy课程

https://karpathy.ai/zero-to-hero.html

- The spelled-out intro to neural networks and backpropagation: building micrograd → https://youtu.be/VMj-3S1tku0
  - [micrograd](https://github.com/karpathy/micrograd)

- The spelled-out intro to language modeling: building makemore → https://youtu.be/PaCmpygFfXo

- Building makemore Part 2: MLP → https://youtu.be/TCH_1BHY58I

- Let's build GPT: from scratch, in code, spelled out. → https://www.youtube.com/watch?v=kCc8FmEb1nY

- Let's build the GPT Tokenizer → https://youtu.be/zduSFxRajkE


### 神经网络的课

[3Blue1Brown Neural Network](https://www.3blue1brown.com/?topic=neural-networks)


[1]: https://arxiv.org/abs/1706.03762?utm_source=chatgpt.com "Attention Is All You Need"
[2]: https://papers.neurips.cc/paper/7181-attention-is-all-you-need.pdf?utm_source=chatgpt.com "[PDF] Attention is All you Need - NIPS"
[3]: https://zh.wikipedia.org/wiki/%E6%B3%A8%E6%84%8F%E5%8A%9B%E5%B0%B1%E6%98%AF%E4%BD%A0%E6%89%80%E9%9C%80%E8%A6%81%E7%9A%84%E4%B8%80%E5%88%87?utm_source=chatgpt.com "注意力就是你所需要的一切"
[4]: https://blog.csdn.net/DeliaPu/article/details/136527834?utm_source=chatgpt.com "Transformer中Self-Attention的详细解读 - CSDN博客"
[5]: https://www.reddit.com/r/deeplearning/comments/k5wn5k/resourcespapers_to_understand_transformers_and/?utm_source=chatgpt.com "Resources/papers to understand transformers and attention - Reddit"
[6]: https://arxiv.org/abs/2006.04768?utm_source=chatgpt.com "Linformer: Self-Attention with Linear Complexity"
[7]: https://arxiv.org/abs/2102.03902?utm_source=chatgpt.com "Nyströmformer: A Nyström-Based Algorithm for Approximating Self-Attention"
[8]: https://arxiv.org/abs/1906.06755?utm_source=chatgpt.com "Theoretical Limitations of Self-Attention in Neural Sequence Models"
[9]: https://arxiv.org/abs/2310.20307?utm_source=chatgpt.com "Causal Interpretation of Self-Attention in Pre-Trained Transformers"
[10]: https://www.wired.com/story/eight-google-employees-invented-modern-ai-transformers-paper?utm_source=chatgpt.com "8 Google Employees Invented Modern AI. Here's the Inside Story"
[11]: https://www.techradar.com/pro/what-are-transformer-models?utm_source=chatgpt.com "What are transformer models?"
