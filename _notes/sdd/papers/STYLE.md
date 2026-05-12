# 任务指令：中英对照阅读器 v2

你是一个 LLM，用户会给你一篇英文**论文 PDF**或**博客文章 URL**。你需要在**自己的代码执行环境**里完成从解析到翻译到构建的整个流程，最终**只给用户一个 HTML 文件**。

---

## 任务总览

输入：一篇英文长文，来源有两种——
- **PDF 论文**（arXiv / 期刊 / 会议论文）
- **Blog 或 Web 文章 URL**（个人博客、公司技术博客、Substack、Medium 等）

输出（只给用户这一个文件）：一份单文件 HTML 阅读器 —— 中英对照、响应式、带目录、带明暗主题、带引用弹窗（如原文有引用）。

执行流程：
1. **阶段一**：从源（PDF 或 URL）抽出结构化英文源 `en.md`
2. **阶段二**：翻译成 `zh.md`，段段 1:1 对齐
3. **阶段三**：按本 spec 写一个构建脚本，渲染 HTML
4. **阶段四**：自检（必跑扫描，不过不交付）
5. **阶段五**：交付 HTML

`en.md` / `zh.md` / `build.py` 是中间产物，同步输出给用户备查。

---

## 阶段一：抽取英文源 `en.md`

### 1.1 段落结构

一段一块，块之间用**一个空行**分隔。两份 md 的段数必须严格相等。

### 1.2 块类型标记

| 标记 | 含义 |
|---|---|
| `[[META]] key: value` | 元数据（title/subtitle/source_url）—— 必须在文件最前 |
| `# 标题` | 一级 |
| `## 标题` | 二级 |
| `### 标题` | 三级 |
| `> 文本` | 引用框 / callout（定理、命题、注释等） |
| `[[FIGn]] caption` | 第 n 张图 + 图注 |
| `[[REF]] [N] 引用文本` | 一条参考文献 |
| `[[TABLE]] caption\|h1;h2\|\|r1c1;r1c2\|\|r2c1;r2c2` | 表格 |
| `[[CODE:lang]]...[[/CODE]]` | 代码块 |
| `[[LIST]]...[[/LIST]]` | 有序列表（items 外部带编号，如 1./2./3.） |
| `[[ULIST]]...[[/ULIST]]` | 无序列表（items 自带标号如 (C1)/(i)/• 或无编号） |
| `[[EQARRAY]]...[[/EQARRAY]]` | 编号公式组，每行格式：`LaTeX \| (N)` |
| `[[INFOBOX]] 标题\|主文 @@ 标签\|值 @@ ...` | 灰色信息框 |

### 1.3 列表类型选择规则

- **`[[LIST]]`**：外部顺序编号有意义时使用，如 "Step 1, Step 2, Step 3" 或 "(1)...(2)...(3)..."
- **`[[ULIST]]`**：以下情形用无序列表：
  - items 自带标号（C1/C2/C3、(i)/(ii)/(iii)、bullet 点）
  - items 之间无先后顺序
  - 原文用 bullet points（•/▪/–）

> **一个常见错误**：把自带编号的条目（如 C1-C4、(i)-(vi)）放进 `[[LIST]]`，导致渲染出双重编号（1. (C1) ...）。凡 items 内部已有标号，必须用 `[[ULIST]]`。

### 1.4 编号公式（EQARRAY）规则

- **每条独立编号公式都应放进 `[[EQARRAY]]`**，即使只有一行
- 一个段落里可以有多个 `[[EQARRAY]]` 块，前后可以有散文文字，build.py 必须能处理
- 格式：`LaTeX表达式 | (N)`，若无编号则只写 LaTeX

### 1.5 表格语法

- `|` 分隔 caption 和表头
- `;` 分隔同一行的各单元格
- `||` 分隔表头与行、行与行
- 行数必须与原 PDF 表完全一致，一行都不能少

### 1.6 引用

- 正文用 `[N]`（整数），按原论文次序
- References 段每条 `[[REF]] [N] 作者(年) 标题. 期刊. arXiv:xxxx`，一条一段
- 代码块里的 `[N]` 不算引用

### 1.7 抽取方式

**情况 A：PDF 论文**

用 `pdfplumber` / `pymupdf` / `pypdf` 提取文本和表格结构。图表如果是栅格图，记录尺寸和 caption 即可——你将在 HTML 里用 SVG 重画（见 §3.6）。

PDF 文本提取常有字符乱码（如 `(cid:104)` 替换 Unicode 符号），需用正则 `re.sub(r'\(cid:\d+\)', '', text)` 过滤，并 ASCII 化后与 en.md 做模糊匹配。

**情况 B：Blog / Web 文章 URL**

1. 先抓网页：用 `requests` + `trafilatura` 或 `readability-lxml` 直接拿到正文
2. 识别规则：`<h1>` → `#`，`<h2>` → `##`，`<h3>` → `###`，`<p>` → 一段一块，`<blockquote>` → `> 文本`，`<pre><code>` → `[[CODE:lang]]`，`<table>` → `[[TABLE]]`，`<figure>` → `[[FIGn]]`
3. 行内 `<strong>`/`<em>`/`<code>`/`<a>` 直接映射到 markdown 语法

### 1.8 顶部元数据段

```
[[META]] title: 原文英文标题
[[META]] subtitle: 作者 · 来源（arXiv:xxxx 或 blog.example.com）· 日期
[[META]] source_url: https://原文地址
```

zh.md 的元数据块对应翻译 title/subtitle，但 source_url 保持不变。

### 1.9 章节顺序必须与 PDF 原文完全一致

PDF 学术论文常见结构：正文 → **附录**（Appendix）→ **参考文献**（References）。
不要把 References 标题提前到 Appendix 之前。务必按 PDF 页码顺序确认每章的位置，再决定 en.md 里的顺序。

---

## 阶段二：翻译成 `zh.md`

### 2.1 术语对照（硬性）

| 英文 | 中文 |
|---|---|
| specification / spec | 规约（不是"规范""规格"） |
| source of truth / ground truth | 事实之源 |
| drift | 漂移 |
| martingale | 鞅 |
| infinitesimal generator | 无穷小生成元 |
| stochastic integral | 随机积分 |
| greenfield / brownfield | 首次出现英文 + 括号翻译 |
| vibe coding, super-prompt, Given/When/Then | 首次出现保留英文 |

风格：直接、技术、克制，匹配论文原作者语气。

### 2.2 零容忍纪律

**做不到就不要交付**，而不是"尽量做"：

**(1) 表格 —— 逐行翻，不补**

长表格拎到 scratch 里，一行一行翻，翻完数 ZH 行数 == EN 行数才能放回 zh.md。严禁"补一条看起来合理的行"。

**(2) 数字 —— 原样搬**

`65%` 就是 `65%`。研究论文的百分比、迭代号、金额、样本数是神圣的，不得改编单位、格式、数值。

**(3) 章节号 / 图号 / 作者名 / 研究数据 —— 不加编辑判断**

原文写 `Section 9` 就翻 `§9`，即便你觉得应该是 §11。作者自己的交叉引用是作者的决定，不是你该改的。

**(4) 长列举段 —— 先数数**

"列了 N 个 bug / N 条原则 / N 个步骤" 这类段：先数清楚 EN 里几项，ZH 项数必须完全相等。漏译不是"总结"。

**(5) 被指出错误后 —— 全文扫同类**

用户指出任何一处错误，不要只补那一处。扫全文所有**同类型**内容一起修。

**(6) 代码块与文献引用 —— 不翻译**

- `[[CODE:lang]]...[[/CODE]]` 块：en.md 和 zh.md 里**完全相同**。
- `[[REF]] [N] ...` 参考文献条目：en.md 和 zh.md 里**完全相同**。
- 唯一例外：`References` 标题本身可翻成"参考文献"，但下面每个 `[[REF]]` 条目保留原文。

**(7) 数学公式块 —— 原样保留**

`[[EQARRAY]]...[[/EQARRAY]]` 块内的 LaTeX 内容和编号，en.md 与 zh.md 里**完全相同**，不得修改任何公式或编号。只有公式**前后的散文文字**需要翻译。

**(8) 翻译完整度 —— 不得缩水**

ZH 块的信息量不得少于 EN 块。常见违规：EN 有 5 段证明步骤，ZH 压缩成 1 行；EN 有 proof sketch 正文，ZH 块为空或只有标题。**必须全量翻译，不得"摘要化"**。

---

## 阶段三：HTML 构建

### 3.1 设计 Token

```css
:root {
  --g-primary: #009f52; --g-secondary: #3eb77a; --g-soft: #e1f5ec; --g-primary-alpha: rgba(0,159,82,0.12);
  --text: #1f2a37; --text-muted: #4b5563;
  --bg: #ffffff; --bg-soft: #f9fafb;
  --border: #e5e7eb; --border-soft: #f1f3f5;
  --code-bg: #0f172a; --code-fg: #e2e8f0;
  --table-head: #f3faf5; --highlight: #fff5c2;
  --fig-bg: #ffffff;
}
@media (prefers-color-scheme: dark) {
  html:not([data-theme]) {
    --g-primary: #3fd18a; --g-secondary: #67c492; --g-soft: #08331f; --g-primary-alpha: rgba(63,209,138,0.18);
    --text: #e5e7eb; --text-muted: #9aa4b2;
    --bg: #0b1220; --bg-soft: #111827;
    --border: #26324a; --border-soft: #1b2335;
    --code-bg: #0a1122; --code-fg: #e5e7eb;
    --table-head: #0c1c12; --highlight: #5b4d18;
    --fig-bg: #111b2e;
  }
}
html[data-theme="dark"] { /* 同上一组值 */ }
```

字体：`-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", system-ui, sans-serif`；基础 `font-size: 15.5px`；`line-height: 1.7`。

代码等宽：`"SF Mono", Menlo, Consolas, monospace`。

### 3.2 整体布局

```
┌─────────────────────────────────────────────────────────┐
│ Topbar (sticky ~50px, backdrop-filter 磨砂)              │
│   左：论文标题                                            │
│   右：.controls（目录按钮 · 语言切换 · 主题切换）          │
├──────────┬──────────────────────────────────────────────┤
│ TOC      │ main                                         │
│ 260px    │   .doc-head                                  │
│ sticky   │   .row × N（EN 左 / ZH 右 双列对照）          │
└──────────┴──────────────────────────────────────────────┘
```

`.layout` 用 flex，容器最大宽 1680px。

### 3.3 双列行 `.row`

```html
<div class="row" id="row-{i}" data-i="{i}">
  <div class="cell en">...</div>
  <div class="cell zh">...</div>
</div>
```

```css
.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-bottom: 1px solid var(--border-soft);
  cursor: pointer;
  scroll-margin-top: 60px;
}
.row:hover { background: var(--bg-soft); }
.row.hl { background: var(--g-primary-alpha); }
.cell { padding: 10px 16px; min-width: 0; border-right: 1px solid var(--border-soft); }
.cell:last-child { border-right: none; }
```

**关键坑**：单语模式必须把 `.row` 的 `grid-template-columns` 覆盖成 `1fr`：

```css
body.mode-en .cell.zh { display: none; }
body.mode-en .row { grid-template-columns: 1fr; }
body.mode-zh .cell.en { display: none; }
body.mode-zh .row { grid-template-columns: 1fr; }
```

### 3.4 行高对齐（双列核心）

双列对照的最大视觉问题是**同一行 EN/ZH 高度不匹配导致跨行错位**。规则：

- **每个 `.row` 内的两个 `.cell` 高度独立**，不强制等高（CSS 自然决定）
- **避免错位的根本方法**：EN 和 ZH 块之间的**信息量和结构必须对等**
  - 如果 EN 块包含两个 `[[EQARRAY]]` + 三段散文，则 ZH 块必须也包含同样两个 `[[EQARRAY]]` + 三段散文
  - 禁止把 EN 的多段内容压缩为 ZH 的一段简短概括

- **主动拆分**：如果 EN 块渲染后高度 > 约 200px（含 EQARRAY 或多段），必须把它拆成多个更小的块，ZH 同步拆成等数量的对应块

  例：EN 的一个证明块含公式 (37) 和公式 (39)，应拆为：
  - 块 A：前半段 + 公式 (37)  → ZH 块 A：对应翻译 + 公式 (37)
  - 块 B：中间段 + 公式 (39)  → ZH 块 B：对应翻译 + 公式 (39)
  - 块 C：结论段               → ZH 块 C：对应翻译

- **自检**：build.py 可以统计每个块的换行数，若 `abs(en_lines - zh_lines) > 5`，打印警告供人工判断

### 3.5 TOC 侧栏

扫 h1/h2/h3，每项：

```html
<a class="toc-item toc-l{1|2|3}" data-i="{块索引}" href="#row-{索引}">
  <span class="toc-zh">{ZH 标题}</span>
  <span class="toc-en">{EN 标题}</span>
</a>
```

- `aside.toc`：260px 宽，`position: sticky; top: 54px`，自身 `overflow-y: auto`
- 根据 `body.mode-*` 自动显隐中/英/双语
- 当前项 `.active`：`border-left: 2px solid var(--g-primary); background: var(--g-soft)`
- 滚动更新 active：rAF 节流，"最近一个 top ≤ 160px 的标题"

### 3.6 响应式

| 断点 | 行为 |
|---|---|
| `≤1100px` | TOC 变 drawer，汉堡按钮显示，左滑入 + 半透明 backdrop |
| `≤768px` | 默认 `mode-zh`；双语模式 EN 栈在 ZH 下（小字灰色）；lightbox close 44×44 圆形 |

### 3.7 组件

**标题**：h1 `color: var(--g-primary)` 22px；h2 `color: var(--g-secondary)` 18px；h3 16px 正常色。

**Figure**：

```html
<figure class="fig">
  <div class="fig-body" data-fig="{n}">{inline SVG}</div>
  <figcaption><span class="fig-num">Fig. {n}</span> {caption}</figcaption>
</figure>
```

SVG 内部颜色**忠于原论文**——原图里什么类别配什么色就保留。绿主题只用于 UI chrome，不要涂图表内容。背景 `var(--fig-bg)` 跟随主题。点击打开 lightbox。

PDF 图表无法直接提取时，必须根据 PDF 原文的**实际数据**用 SVG 重绘：
- 柱状图：用 PDF 文本层或附近数字还原数值
- 折线图：用 PDF 内坐标轴标注还原数据点
- 热图：用 PDF 文本提取每个格子的数值
- 禁止凭空编造数据，禁止用占位符 `[图N]` 交付

**Table**：包 `.table-wrap` 实现 `overflow-x: auto`，`caption` 浅灰背景，`thead` 用 `--table-head`。

**Infobox**：左侧 4px 绿边，背景 `--g-soft`；`.info-title` 绿色加粗。

**引用上标**：`<sup class="cite" tabindex="0" data-ref="N">[N]</sup>`，绿色。

**Code**：块级 `<pre class="code" data-lang="...">` 深色底；行内 `<code>` 浅色底等宽。

**Ref row**：`<div class="ref-row" id="ref-{lang}-{n}">`，`scroll-margin-top: 64px`，跳转时临时 `.hl-ref` 背景 `--highlight` 3 秒。

**编号公式（EQARRAY）渲染**：

```python
def render_eq_array(eqs_raw, cite_dict):
    rows = []
    for line in eqs_raw.strip().splitlines():
        line = line.strip()
        if not line: continue
        if ' | ' in line:
            eq_part, num_part = line.rsplit(' | ', 1)
        else:
            eq_part, num_part = line, ''
        eq_tex = '$$' + eq_part.strip() + '$$'
        num_html = f'<span class="eq-num">{num_part.strip()}</span>' if num_part.strip() else ''
        rows.append(f'<div class="eq-row"><div class="eq-math">{eq_tex}</div>{num_html}</div>')
    return f'<div class="eq-array">{"".join(rows)}</div>'
```

**关键**：`render_block` 的 EQARRAY 分支必须支持**段落内多个 EQARRAY 块**：

```python
if '[[EQARRAY]]' in b:
    parts = re.split(r'(\[\[EQARRAY\]\].*?\[\[/EQARRAY\]\])', b, flags=re.DOTALL)
    if len(parts) == 3 and not parts[0].strip() and not parts[2].strip():
        # 简单情形：只有一个 EQARRAY，无前后文字
        eqs_raw = parts[1][len('[[EQARRAY]]'):parts[1].rfind('[[/EQARRAY]]')]
        return render_eq_array(eqs_raw, cite_dict)
    # 通用情形：文字与 EQARRAY 交替
    out = []
    for part in parts:
        if part.startswith('[[EQARRAY]]'):
            eqs_raw = part[len('[[EQARRAY]]'):part.rfind('[[/EQARRAY]]')]
            out.append(render_eq_array(eqs_raw, cite_dict))
        elif part.strip():
            out.append(f'<p>{render_inline(part.strip(), cite_dict)}</p>')
    return ''.join(out)
```

同样的多 EQARRAY 处理逻辑必须也出现在 **blockquote** 的渲染分支里（`> **Theorem...**` 后带公式的情形）。

### 3.8 内联 markdown 解析（按顺序）

1. `html.escape()` 转义
2. 反引号 `` `x` `` 内容用占位符 `\x00CODE{N}\x00` 替换（防后续步骤误处理）
3. `**粗体**` → `<strong>`
4. `_斜体_` → `<em>`（lookbehind 确保不在单词中间）
5. URL 自动 linkify
6. `[N]` → `<sup class="cite">`（如果 N 在引用字典里）
7. 占位符还原为 `<code>`

**坑**：不先做步骤 2，代码里的 `**` 或 `[1]` 会被误解析。

### 3.9 Topbar 交互

**语言切换**：三按钮 `双语 / 中文 / English`，点击更新 `body` class 为 `mode-bi` / `mode-zh` / `mode-en`。初始：移动端默认 `mode-zh`。切换后对含 MathJax 公式的页面调用 `MathJax.typesetPromise()` 重新排版。

**主题切换**：

```html
<!-- <head> 里，必须在 CSS link 之前 -->
<script>
  (function() {
    try {
      var t = localStorage.getItem('paper-theme');
      if (t === 'light' || t === 'dark') {
        document.documentElement.setAttribute('data-theme', t);
      }
    } catch (e) {}
  })();
</script>
```

（这段预执行脚本**必须**在 CSS 之前，否则刷新会闪白。）

**MathJax 加载方式**：用 `async` 而非 `defer`，`defer` 在某些浏览器环境会导致公式不渲染：

```html
<script>
  MathJax = {
    tex: { inlineMath: [['$','$']], displayMath: [['$$','$$']], processEscapes: true,
           skipHtmlTags: ['pre', 'code'] },
    svg: { fontCache: 'global' }
  };
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>
```

**TOC 跳转**：

```js
const toolbar = document.querySelector('.topbar');
const offset = toolbar.getBoundingClientRect().height + 8;
const targetY = row.getBoundingClientRect().top + window.scrollY - offset;
window.scrollTo({ top: targetY, behavior: 'smooth' });
```

**引用弹窗**：

- 桌面：hover / focus 显示 `.cite-pop`；智能定位（默认下方，超出视口改上方；左右边距 10px 内）
- 移动端（`matchMedia('(hover: none)')`）：**两段点击** —— 第一次显示弹窗，第二次跳到 `#ref-{lang}-{n}`

**Lightbox**：点 `.fig-body`，克隆 SVG、去掉固定 width/height、`style.width='100%'`，容器 `min(95vw, 1600px)`。ESC 或点遮罩关闭。`stopPropagation` 防冒泡到 row。

### 3.10 数学公式

MathJax v3 tex-svg，**async**（不是 defer）：

独立公式：md 里整段 `$$...$$`，build 时识别并输出 `<div class="math-display">`（居中、overflow-x auto）。行内 `$x$`。代码块里的 Unicode 数学符号（∀≤•）保持原样。

### 3.11 打印

```css
@media print {
  .topbar, .lightbox, .cite-pop, .toc, .toc-backdrop { display: none !important; }
  body { font-size: 11pt; line-height: 1.5; }
  .row, figure.fig { break-inside: avoid; page-break-inside: avoid; }
}
```

---

## 阶段四：自检（交付前必跑）

任何一条不过就不得交付。

### (1) 段数对齐

```python
assert len(en_blocks) == len(zh_blocks), f"Block count mismatch: EN={len(en_blocks)}, ZH={len(zh_blocks)}"
```

### (2) 表格行数对齐

```python
for i, (e, z) in enumerate(zip(en_blocks, zh_blocks)):
    if e.startswith('[[TABLE]]'):
        assert e.count('||') == z.count('||'), f'Table row mismatch at block {i}'
```

### (3) 引用 [N] 位置对齐

```python
import re
for i, (e, z) in enumerate(zip(en_blocks, zh_blocks)):
    if e.startswith(('[[CODE:', '[[REF]]')): continue
    assert sorted(re.findall(r'\[(\d+)\]', e)) == sorted(re.findall(r'\[(\d+)\]', z)), \
           f'Ref mismatch at block {i}'
```

### (4) 数字与实体保留

对正文段提取 EN 里的：百分比、迭代号、金额、`` `backtick` `` 代码、`ALL_CAPS` 标识符、`CamelCase` 专名。每一项都应该出现在对应 ZH 段里。

### (5) 代码块与文献引用 byte-level 相同

```python
for i, (e, z) in enumerate(zip(en_blocks, zh_blocks)):
    if e.startswith('[[CODE:') or e.startswith('[[REF]]'):
        assert e == z, f'Block {i} should be identical in EN/ZH:\nEN: {e[:200]}\nZH: {z[:200]}'
```

### (6) EQARRAY 公式 byte-level 相同

```python
import re
for i, (e, z) in enumerate(zip(en_blocks, zh_blocks)):
    en_eqs = re.findall(r'\[\[EQARRAY\]\](.*?)\[\[/EQARRAY\]\]', e, re.DOTALL)
    zh_eqs = re.findall(r'\[\[EQARRAY\]\](.*?)\[\[/EQARRAY\]\]', z, re.DOTALL)
    assert len(en_eqs) == len(zh_eqs), f'EQARRAY count mismatch at block {i}'
    for j, (eq_e, eq_z) in enumerate(zip(en_eqs, zh_eqs)):
        assert eq_e.strip() == eq_z.strip(), \
               f'EQARRAY content differs at block {i}, eq {j}:\nEN: {eq_e[:100]}\nZH: {eq_z[:100]}'
```

### (7) HTML 标记泄漏检查

```python
html_content = open('output.html').read()
leaked = re.findall(r'\[\[(?:LIST|ULIST|EQARRAY|TABLE|REF|CODE|FIG|META)[^\]]*\]\]', html_content)
assert not leaked, f'Unrendered block markers in HTML: {leaked[:5]}'
```

### (8) 结构对齐扫描

```python
for i, (e, z) in enumerate(zip(en_blocks, zh_blocks)):
    # 标题级别必须匹配
    en_is_h = e.startswith('#')
    zh_is_h = z.startswith('#')
    assert en_is_h == zh_is_h, f'Heading mismatch at block {i}: EN={e[:40]}, ZH={z[:40]}'
    # REF 必须匹配
    assert e.startswith('[[REF]]') == z.startswith('[[REF]]'), f'REF mismatch at block {i}'
```

### (9) 行高差异检查（警告级，不中断）

```python
for i, (e, z) in enumerate(zip(en_blocks, zh_blocks)):
    en_lines = len(e.split('\n'))
    zh_lines = len(z.split('\n'))
    if abs(en_lines - zh_lines) > 5:
        print(f'WARNING: Block {i} line count mismatch (EN={en_lines}, ZH={zh_lines}): {e[:50]}')
```

行高差距 > 5 行时，考虑将该块拆分为多个更小的对齐块（见 §3.4）。

---

## 阶段五：交付

**给用户这三个文件**：HTML 阅读器、en.md、zh.md（后两个供后续修改复用）。

- HTML 文件名：`{slug}-bilingual.html`（slug 来自论文标题，小写、连字符分隔）
- 单文件，所有 CSS/JS 内联
- 外部依赖仅 MathJax CDN（原文有公式时）

用户若要求修改译文，在本次对话里改 zh.md 并重 build。

---

## 常见坑清单（真实踩过）

### 内容完整性
1. **PDF 段落大量缺失** → 必须用 PDF 原文逐章核对，不能只依赖之前的翻译存档。每章提取后与 en.md 用关键词匹配验证。
2. **翻译"摘要化"** → 严禁把 EN 的多段证明/实验描述压缩成 ZH 的一行概括（§2.2 (8)）。
3. **附录证明内容大量缺失** → 附录章节必须和正文一样逐块提取和翻译，不能因为内容密集就跳过。

### 块结构对齐
4. **参考文献标题与内容分离** → References 标题块必须紧邻第一个 `[[REF]]` 块，中间不能插入附录等其他章节。章节顺序必须严格按 PDF 原文页码。
5. **附录块数 EN ≠ ZH** → 每次修改附录后必须重跑段数对齐检查（§阶段四(1)）。ZH 和 EN 的附录如果块数不同，从第一个不匹配的地方开始后续全部错位。
6. **行高不匹配导致视觉错位** → 含多个 EQARRAY 的长块必须拆分（§3.4），ZH 同步拆成相同数量的块，且每块都包含对应的公式标记。

### 列表类型
7. **自带编号的条目放进 `[[LIST]]`** → 导致双重编号（1. (C1) ...）。自带 C1-C4、(i)-(vi)、bullet 的条目必须用 `[[ULIST]]`。
8. **有序列表用了无序** → 步骤顺序有意义时（Step 1/2/3、F1/F2/F3/F4 对照实验控制）必须用 `[[LIST]]`。

### 数学公式渲染
9. **段落内多个 EQARRAY 只渲染第一个** → `render_block` 的 EQARRAY 分支必须用 `re.split` 处理所有 EQARRAY，不能只用 `partition` 取第一个（§3.7）。
10. **blockquote 内 EQARRAY 也需同样处理** → blockquote 分支和普通段落分支都要做多 EQARRAY 支持。
11. **MathJax 用 defer 不渲染** → 必须用 `async`（§3.9）。
12. **语言切换后公式不刷新** → 切换模式后调用 `MathJax.typesetPromise()`。

### 图表
13. **图表用占位符 `[图N]` 交付** → 严禁。必须根据 PDF 原文数据用 SVG 重绘（§3.7）。
14. **图表配色用绿主题** → 错，图表内部忠于原论文，绿色只用于 UI chrome（§3.7）。

### 经典 UI 坑
15. **单语模式 .row 卡半宽** → 必须改 `grid-template-columns: 1fr`（§3.3）
16. **主题切换刷新闪白** → head 预执行脚本必须在 CSS 前（§3.9）
17. **TOC 跳转位置偏** → 单次 `scrollTo` 加 offset，不要 `scrollIntoView + scrollBy`（§3.9）
18. **内联代码里的 `**` 或 `[N]` 被二次解析** → 占位符保护（§3.8）
19. **长表格凭感觉补行** → 严禁（§2.2）
20. **用户指出一个错只修一个** → 错，全文扫同类（§2.2）

---

## 执行建议

- 长论文分步来：
  1. 先交 en.md 的**所有 h1/h2/h3 标题**给用户确认结构
  2. 分批翻 zh.md，每 20-30 段一批，当场跑阶段四全部 9 个扫描
  3. 最后一次性 build HTML + 交付
- 翻长表格时单独拎到 scratch，row-by-row，翻完数完再塞回
- 不确定某个数字/引用/专名时，**保留原文英文** —— 原样搬永远比"猜着翻"安全
- 遇到含 2+ 个 EQARRAY 的长块，**立刻主动拆分**，不要等用户反馈错位再修
- 附录章节与正文等同对待，不因内容复杂就降低翻译完整度要求