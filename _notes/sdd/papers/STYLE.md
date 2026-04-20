# 任务指令：中英对照阅读器

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
4. **阶段四**：自检（5 个必跑扫描）
5. **阶段五**：交付 HTML

`en.md` / `zh.md` / `build.py` 是中间产物，用户不需要看到。

---

## 阶段一：抽取英文源 `en.md`

### 段落结构

一段一块，块之间用**一个空行**分隔。两份 md 的段数必须严格相等。

### 块类型标记

| 标记 | 含义 |
|---|---|
| `[[META]] key: value` | 元数据（title/subtitle/source_url）—— 必须在文件最前 |
| `# 标题` | 一级 |
| `## 标题` | 二级 |
| `### 标题` | 三级 |
| `> 文本` | 引用框 / callout |
| `[[FIGn]] caption` | 第 n 张图 + 图注 |
| `[[REF]] [N] 引用文本` | 一条参考文献 |
| `[[TABLE]] caption\|h1;h2\|\|r1c1;r1c2\|\|r2c1;r2c2` | 表格 |
| `[[CODE:lang]]...[[/CODE]]` | 代码块 |
| `[[INFOBOX]] 标题\|主文 @@ 标签\|值 @@ ...` | 灰色信息框 |

### 表格语法

- `|` 分隔 caption 和表头
- `;` 分隔同一行的各单元格
- `||` 分隔表头与行、行与行
- 行数必须与原 PDF 表完全一致，一行都不能少

### 引用

- 正文用 `[N]`（整数），按原论文次序
- References 段每条 `[[REF]] [N] 作者(年) 标题. 期刊. arXiv:xxxx`，一条一段
- 代码块里的 `[N]` 不算引用

### 抽取方式

**情况 A：PDF 论文**

用 `pdfplumber` / `pymupdf` / `pypdf` 提取文本和表格结构。图表如果是栅格图，记录尺寸和 caption 即可——你将在 HTML 里用 SVG 重画（见 §3.6）。

**情况 B：Blog / Web 文章 URL**

1. 先抓网页：用 `requests` + `trafilatura` 或 `readability-lxml` 直接拿到正文（自动剥掉导航、侧栏、评论、footer）
2. 也可以直接 BeautifulSoup 解析。识别规则：
   - `<h1>` → `#`（通常只有一个，全文主标题）
   - `<h2>` → `##`
   - `<h3>` → `###`
   - `<p>` → 一段一块
   - `<blockquote>` → `> 文本`
   - `<pre><code>` 或 `<pre class="language-xxx">` → `[[CODE:lang]]...[[/CODE]]`
   - `<table>` → `[[TABLE]]` 格式（§1.3），HTML 表格的 `<thead>` 是表头、`<tbody>` 的每个 `<tr>` 是一行
   - `<figure>` 或 `<img alt="...">` → `[[FIGn]] alt 或最近的 caption 文本`
   - `<ul>/<ol>` → 保留为散文式的"(1) ... (2) ..."，或按段落分开（取决于语义——每条短就合成一段，每条长就分段）
3. 行内 `<strong>`/`<em>`/`<code>`/`<a>` 直接映射到 markdown 的 `**/_/`/`` ` ``/URL 语法

**图的特殊处理（Blog 版）**

Blog 的图通常已经是可渲染的 `<img>`，不用重画 SVG。策略：
- 小尺寸（< 200KB）：fetch 后 base64 内嵌到 HTML，保证离线可用
- 大尺寸：保留原始 URL 外链（注释里说明）
- 渲染时 `<figure class="fig"><div class="fig-body"><img src="..." /></div><figcaption>...</figcaption></figure>`，替代内联 SVG。Lightbox 点击放大同样适用（克隆 img 节点并设 `style.width=100%`）

**引用的特殊处理（Blog 版）**

Blog 文章不一定有编号引用。如果有：
- 脚注风格（`<sup><a href="#fn1">1</a></sup>` + 页末 `<li id="fn1">`）→ 映射到 `[N]` + `[[REF]]`
- 没有的话：`[[REF]]` 段整体省略，正文里也没有 `[N]` 标记需要处理

### 1.5 内容类型适配（HTML 页面上的差别）

| 差别点 | PDF 论文 | Blog 文章 |
|---|---|---|
| 顶部标题区 | 显示 arXiv ID、作者、日期 | 显示博客标题、作者、原文链接 |
| 引用 | 通常有，走 [N] + [[REF]] | 常常没有或只有脚注 |
| 图 | 重画成 SVG | `<img>` 外链或 base64 内嵌 |
| TOC | 多为 h1/h2 多级 | 可能只有 h2，或干脆没有 —— 若少于 3 个 h1/h2，隐藏 TOC 栏 |
| 章节编号 | 原文带 "1 / 1.1 / 1.1.1" | 多为纯文字标题，不加编号 |

### 1.6 顶部元数据段

在 `en.md` 第一段前插入一个特殊的元数据块（用于 HTML 顶部 `.doc-head` 渲染）：

```
[[META]] title: 原文英文标题
[[META]] subtitle: 作者 · 来源（arXiv:xxxx 或 blog.example.com）· 日期
[[META]] source_url: https://原文地址
```

zh.md 的元数据块对应翻译 title/subtitle，但 source_url 保持不变。

---

## 阶段二：翻译成 `zh.md`

### 2.1 术语对照（硬性）

| 英文 | 中文 |
|---|---|
| specification / spec | 规约（不是"规范""规格"） |
| source of truth / ground truth | 事实之源 |
| drift | 漂移 |
| greenfield / brownfield | 首次出现英文 + 括号翻译 |
| vibe coding, super-prompt, Given/When/Then | 首次出现保留英文 |

风格：直接、技术、克制，匹配论文原作者语气。

### 2.2 零容忍纪律

**做不到就不要交付**，而不是"尽量做"：

**(1) 表格 —— 逐行翻，不补**

长表格拎到 scratch 里，一行一行翻，翻完数 ZH 行数 == EN 行数才能放回 zh.md。严禁"补一条看起来合理的行"。

**(2) 数字 —— 原样搬**

`65%` 就是 `65%`，不是 "65 分"。研究论文的百分比、迭代号、金额、样本数是神圣的。不得改编单位、格式、数值。

**(3) 章节号 / 图号 / 作者名 / 研究数据 —— 不加编辑判断**

原文写 `Section 9` 就翻 `§9`，即便你觉得应该是 §11。作者自己的交叉引用是作者的决定，不是你该改的。

**(4) 长列举段 —— 先数数**

"列了 N 个 bug / N 条原则 / N 个步骤" 这类段：先数清楚 EN 里几项，ZH 项数必须完全相等。漏译不是"总结"。

**(5) 被指出错误后 —— 全文扫同类**

用户指出任何一处错误，不要只补那一处。扫全文所有**同类型**内容一起修。

**(6) 代码块与文献引用 —— 不翻译**

- `[[CODE:lang]]...[[/CODE]]` 块：en.md 和 zh.md 里**完全相同**。代码、注释、字符串全部保留原样，翻了就会报错或语义漂移。
- `[[REF]] [N] ...` 参考文献条目：en.md 和 zh.md 里**完全相同**。学术引用原样保留（作者、期刊、标题、arXiv 编号都不译），这是学术规范。
- 唯一例外：`References` / `Bibliography` 这个 h1/h2 标题本身可以翻成"参考文献"（或保留英文均可），但下面每个 `[[REF]]` 条目保留原文。
- 自检时这两类块必须 byte-level 相同，不同就是 bug。

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
  scroll-margin-top: 60px;  /* anchor 跳转避让 toolbar */
}
.row:hover { background: var(--bg-soft); }
.row.hl { background: var(--g-primary-alpha); }
.cell { padding: 10px 16px; min-width: 0; border-right: 1px solid var(--border-soft); }
.cell:last-child { border-right: none; }
```

**关键坑**：单语模式必须把 `.row` 的 `grid-template-columns` 覆盖成 `1fr`。只 `display: none` 掉另一列，grid track 仍占位，导致可见列卡在半宽：

```css
body.mode-en .cell.zh { display: none; }
body.mode-en .row { grid-template-columns: 1fr; }
body.mode-zh .cell.en { display: none; }
body.mode-zh .row { grid-template-columns: 1fr; }
```

### 3.4 TOC 侧栏

扫 h1/h2，每项：

```html
<a class="toc-item toc-l{1|2}" data-i="{块索引}" href="#row-{索引}">
  <span class="toc-zh">{ZH 标题}</span>
  <span class="toc-en">{EN 标题}</span>
</a>
```

- `aside.toc`：260px 宽，`position: sticky; top: 54px`，自身 `overflow-y: auto`
- 根据 `body.mode-*` 自动显隐中/英/双语
- 当前项 `.active`：`border-left: 2px solid var(--g-primary); background: var(--g-soft)`
- 滚动更新 active：rAF 节流，"最近一个 top ≤ 160px 的标题"

### 3.5 响应式

| 断点 | 行为 |
|---|---|
| `≤1100px` | TOC 变 drawer，汉堡按钮显示，左滑入 + 半透明 backdrop |
| `≤768px` | 默认 `mode-zh`；双语模式 EN 栈在 ZH 下（小字灰色）；lightbox close 44×44 圆形 |

### 3.6 组件

**标题**：h1 `color: var(--g-primary)` 22px；h2 `color: var(--g-secondary)` 18px（比 h1 浅一档）；h3 16px 正常色。

需要在 CSS 变量里加一条：
- Light：`--g-secondary: #3eb77a`
- Dark：`--g-secondary: #67c492`

**Figure**：

```html
<figure class="fig">
  <div class="fig-body" data-fig="{n}">{inline SVG}</div>
  <figcaption><span class="fig-num">Fig. {n}</span> {caption}</figcaption>
</figure>
```

SVG 内部颜色**忠于原论文**——原图里什么类别配什么色就保留。绿主题只用于 UI chrome，不要涂图表内容。背景 `var(--fig-bg)` 跟随主题。点击打开 lightbox。

**Table**：包 `.table-wrap` 实现 `overflow-x: auto`，`caption` 浅灰背景，`thead` 用 `--table-head`。

**Infobox**：左侧 4px 绿边，背景 `--g-soft`；`.info-title` 绿色加粗。

**引用上标**：`<sup class="cite" tabindex="0" data-ref="N">[N]</sup>`，绿色。

**Code**：块级 `<pre class="code" data-lang="...">` 深色底；行内 `<code>` 浅色底等宽。

**Ref row**：`<div class="ref-row" id="ref-{lang}-{n}">`，`scroll-margin-top: 64px`，跳转时临时 `.hl-ref` 背景 `--highlight` 3 秒。

### 3.7 内联 markdown 解析（按顺序）

1. `html.escape()` 转义
2. 反引号 `` `x` `` 内容用占位符 `\x00CODE{N}\x00` 替换（防后续步骤误处理）
3. `**粗体**` → `<strong>`
4. `_斜体_` → `<em>`（lookbehind 确保不在单词中间）
5. URL 自动 linkify
6. `[N]` → `<sup class="cite">`（如果 N 在引用字典里）
7. 占位符还原为 `<code>`

**坑**：不先做步骤 2，代码里的 `**` 或 `[1]` 会被误解析。

### 3.8 Topbar 交互

**语言切换**：三按钮 `双语 / 中文 / English`，点击更新 `body` class 为 `mode-bi` / `mode-zh` / `mode-en`。初始：移动端默认 `mode-zh`。

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

按钮 click 切换 `<html>` 的 `data-theme` 属性在 `light`/`dark` 两态循环，并写入 localStorage。图标两个 SVG（moon/sun），用 CSS 根据 data-theme 显隐。

**TOC 跳转** —— 别踩这个坑：

❌ 错误：
```js
row.scrollIntoView({behavior: 'smooth'});
setTimeout(() => window.scrollBy({top: -60}), 0);  // 打断平滑滚动
```

✅ 正确：
```js
const toolbar = document.querySelector('.topbar');
const offset = toolbar.getBoundingClientRect().height + 8;
const targetY = row.getBoundingClientRect().top + window.scrollY - offset;
window.scrollTo({ top: targetY, behavior: 'smooth' });
```

移动端跳转后自动关闭 drawer。

**引用弹窗**：

- 桌面：hover / focus 显示 `.cite-pop`；智能定位（默认下方，超出视口改上方；左右边距 10px 内）
- 移动端（`matchMedia('(hover: none)')`）：**两段点击** —— 第一次显示弹窗，第二次跳到 `#ref-{lang}-{n}`
- 跳转后目标行 `.hl-ref` 高亮 3 秒

**Lightbox**：点 `.fig-body`，克隆 SVG、`removeAttribute('width')`/`removeAttribute('height')`、`style.width='100%'`，容器 `min(95vw, 1600px)`。ESC 或点遮罩关闭。`stopPropagation` 防止冒泡到 row。

**行点击高亮**：点 `.row` 加 `.hl`。不能拦截 `<a>` 或 `.cite` 的点击：

```js
row.addEventListener('click', e => {
  if (e.target.closest('a') || e.target.closest('.cite')) return;
  document.querySelectorAll('.row.hl').forEach(x => x.classList.remove('hl'));
  row.classList.add('hl');
});
```

### 3.9 数学公式

MathJax v3 tex-svg，defer：

```html
<script>
  MathJax = { tex: { inlineMath: [['$','$']], displayMath: [['$$','$$']] }, svg: { fontCache: 'global' } };
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" defer></script>
```

独立公式：md 里整段 `$$...$$`，build 时识别并输出 `<div class="math-display">`（居中、overflow-x auto）。行内 `$x$`。代码块里的 Unicode 数学符号（∀≤•）保持原样。

### 3.10 打印

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
assert len(en_blocks) == len(zh_blocks)
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

对正文段提取 EN 里的：百分比、迭代号、金额、`` `backtick` `` 代码、`ALL_CAPS` 标识符、`CamelCase` 专名。每一项都应该出现在对应 ZH 段里（原样或合理翻译形式）。差异打印出来人工判定是"合理翻译差异"还是"漏译/捏造"。

### (5) 代码块与文献引用 byte-level 相同

```python
for i, (e, z) in enumerate(zip(en_blocks, zh_blocks)):
    if e.startswith('[[CODE:') or e.startswith('[[REF]]'):
        assert e == z, f'Block {i} should be identical in EN/ZH but differs:\nEN: {e[:200]}\nZH: {z[:200]}'
```

代码块与 `[[REF]]` 条目在 en.md 和 zh.md 里必须**完全一样**。有任何差异就是 bug（常见误翻：把英文 `return 0` 翻成中文、把引用里的作者名音译、把 arXiv 编号改格式）。

---

## 阶段五：交付

**只给用户一个 HTML 文件**。

- 文件名：`{slug}-bilingual.html`（slug 来自论文标题或博客文章标题，小写、连字符分隔）
- 单文件，所有 CSS/JS 内联
- 外部依赖仅 MathJax CDN（原文有公式时）；blog 大图若用原 URL 外链需注明

不要主动暴露 en.md / zh.md / build.py 的存在。用户若要求修改译文，在本次对话里改 zh.md 并重 build。

---

## 常见坑清单（真实踩过）

1. **内联代码里的 `**` 或 `[N]` 被二次解析** → 占位符保护（§3.7）
2. **单语模式 .row 卡半宽** → 必须改 `grid-template-columns: 1fr`（§3.3）
3. **主题切换刷新闪白** → head 预执行脚本必须在 CSS 前（§3.8）
4. **TOC 跳转位置偏** → 单次 `scrollTo` 加 offset，不要 `scrollIntoView + scrollBy`（§3.8）
5. **图表配色用绿主题** → 错，图表内部忠于原论文（§3.6）
6. **长表格凭感觉补行** → 严禁（§2.2）
7. **擅改原文 Section 号** → 严禁（§2.2）
8. **用户指出一个错只修一个** → 错，全文扫同类（§2.2）

---

## 执行建议

- 长论文分步来，一步一汇报：
  1. 先交 `en.md` 的**所有 h1/h2 标题**给用户确认结构
  2. 分批翻 zh.md，每 20-30 段一批，当场跑 §阶段四 的 5 个扫描
  3. 最后一次性 build HTML + 交付
- 翻长表格时单独拎到 scratch，row-by-row，翻完数完再塞回 zh.md
- 不确定某个数字/引用/专名时，**保留原文英文** —— 原样搬永远比"猜着翻"安全