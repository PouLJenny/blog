import re
import os
from html import escape
from markdown import markdown
from bs4 import BeautifulSoup


def _extract_fenced_blocks(md_content):
    """
    手动提取所有顶层围栏代码块，替换为占位符。
    支持嵌套：```markdown 内含 ```java 也能正确识别，不会被提前截断。
    返回: (替换后的md文本, {占位符: (lang, content)})
    """
    blocks = {}
    result = []
    lines = md_content.split('\n')
    i = 0
    count = 0

    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(`{3,}|~{3,})(\S*)\s*$', line)
        if m:
            fence_char = m.group(1)[0]
            fence_len = len(m.group(1))
            lang = m.group(2)
            # 关闭围栏：相同字符、至少相同数量、行内无其他内容
            closing = re.compile(
                r'^' + re.escape(fence_char) + r'{' + str(fence_len) + r',}\s*$'
            )
            content_lines = []
            i += 1
            # 用栈追踪嵌套代码块，避免内层的 ``` 被误判为外层的关闭围栏
            nest_stack = []
            while i < len(lines):
                current = lines[i]
                if nest_stack:
                    # 当前在嵌套块内，检查是否关闭嵌套块
                    _, _, inner_closing = nest_stack[-1]
                    if inner_closing.match(current):
                        nest_stack.pop()
                    else:
                        # 嵌套块内还可以继续嵌套（理论上）
                        nm = re.match(r'^(`{3,}|~{3,})(\S+)\s*$', current)
                        if nm:
                            nc, nl = nm.group(1)[0], len(nm.group(1))
                            nest_stack.append((nc, nl, re.compile(
                                r'^' + re.escape(nc) + r'{' + str(nl) + r',}\s*$'
                            )))
                    content_lines.append(current)
                else:
                    # 在外层块内
                    if closing.match(current):
                        # 真正关闭外层块
                        i += 1
                        break
                    # 检查是否开启了一个嵌套块（有语言标识符，否则无法区分开启/关闭）
                    nm = re.match(r'^(`{3,}|~{3,})(\S+)\s*$', current)
                    if nm:
                        nc, nl = nm.group(1)[0], len(nm.group(1))
                        nest_stack.append((nc, nl, re.compile(
                            r'^' + re.escape(nc) + r'{' + str(nl) + r',}\s*$'
                        )))
                    content_lines.append(current)
                i += 1
            placeholder = f'FENCED_BLOCK_PLACEHOLDER_{count}'
            count += 1
            blocks[placeholder] = (lang, '\n'.join(content_lines))
            result.append(placeholder)
        else:
            result.append(line)
            i += 1

    return '\n'.join(result), blocks


def _restore_fenced_blocks(html_content, blocks):
    """将占位符还原为 <pre><code> 或 <div class="mermaid"> HTML（内容已 HTML 转义）"""
    for placeholder, (lang, content) in blocks.items():
        if lang == 'mermaid':
            code_html = f'<div class="mermaid">{escape(content)}</div>'
        else:
            lang_attr = f' class="language-{lang}"' if lang else ''
            code_html = f'<pre><code{lang_attr}>{escape(content)}</code></pre>'
        # markdown 库可能把孤立的占位符包进 <p>，一并替换
        html_content = html_content.replace(f'<p>{placeholder}</p>', code_html)
        html_content = html_content.replace(placeholder, code_html)
    return html_content


def md_to_html_with_toc(md_file_path, html_file_path=None, title="Markdown转换结果"):
    """
    将Markdown文件转换为带左侧固定可折叠目录（隐藏后保留唤起按钮）、图片懒加载、回到顶部按钮的HTML文件
    :param md_file_path: Markdown文件路径
    :param html_file_path: 输出HTML文件路径（默认同目录同名）
    :param title: HTML页面标题
    """
    # 默认输出路径
    if not html_file_path:
        base_name = os.path.splitext(md_file_path)[0]
        html_file_path = f"{base_name}.html"

    # 1. 读取Markdown文件
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 2. 预处理：手动提取所有围栏代码块（支持嵌套），避免 markdown 库提前截断
    md_safe, fenced_blocks = _extract_fenced_blocks(md_content)

    # 3. 将 Markdown 转换为 HTML（extra 已含 fenced_code/tables/md_in_html）
    html_content = markdown(
        md_safe,
        extensions=['extra', 'toc'],
    )

    # 4. 还原代码块（内容已 HTML 转义，不会被浏览器渲染）
    html_content = _restore_fenced_blocks(html_content, fenced_blocks)

    # 5. 解析HTML，提取标题+处理图片懒加载
    soup = BeautifulSoup(html_content, 'html.parser')

    # ========== 处理标题：添加锚点 + 修复跳转偏移 ==========
    headings = soup.find_all(re.compile(r'^h[1-6]$'))
    toc_items = []
    anchor_id = 1
    for heading in headings:
        heading_text = heading.get_text(strip=True)
        current_id = f"heading-{anchor_id}"
        anchor_id += 1
        heading['id'] = current_id
        # 添加锚点偏移修复的样式类
        heading['class'] = heading.get('class', []) + ['anchor-heading']
        level = int(heading.name[1])
        toc_items.append((level, heading_text, current_id))

    # ========== 处理图片：添加懒加载 + 统一样式 ==========
    images = soup.find_all('img')
    for img in images:
        # 添加原生懒加载属性
        img['loading'] = 'lazy'
        # 添加样式类
        img['class'] = img.get('class', []) + ['content-img']
        # 补充alt属性（避免空值）
        if not img.get('alt'):
            img['alt'] = f"图片{images.index(img)+1}"
        # 补充width/height（保持比例）
        if not img.get('width') and not img.get('height'):
            img['style'] = img.get('style', '') + 'object-fit: cover;'

    # ========== 生成目录HTML（修复嵌套缩进） ==========
    toc_html = """
    <div class="toc-header">
        <h2>目录</h2>
        <button class="toc-toggle-btn" id="tocToggleBtn">≡</button>
    </div>
    <ul class="toc-list">
    """
    # 修复目录层级计算逻辑
    level_stack = [1]
    for level, text, anchor_id in toc_items:
        # 处理层级增加
        while level > level_stack[-1]:
            toc_html += f"\n{'    '*len(level_stack)}<ul class='toc-sublist'>"
            level_stack.append(level_stack[-1] + 1)
        # 处理层级减少
        while level < level_stack[-1]:
            toc_html += f"\n{'    '*(len(level_stack)-1)}</ul></li>"
            level_stack.pop()
        # 添加当前目录项
        indent = '    ' * (len(level_stack)-1)
        toc_html += f"\n{indent}<li class='toc-item toc-level-{level}'>"
        toc_html += f"<a href='#{anchor_id}' class='toc-link'>{text}</a></li>"
    # 闭合剩余的ul标签
    while len(level_stack) > 1:
        toc_html += f"\n{'    '*(len(level_stack)-2)}</ul></li>"
        level_stack.pop()
    toc_html += """
    </ul>
    """

    # ========== 完整HTML模板（修复隐藏后无唤起按钮） ==========
    full_html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* ========== CSS 变量：#009f52 清新绿主色调 ========== */
        :root {{
            --accent:            #009f52;
            --accent-dark:       #007a3f;
            --accent-deeper:     #005c30;
            --accent-light:      #e6f7ef;
            --accent-light2:     #c8eeda;
            --sidebar-bg:        #ffffff;
            --sidebar-border:    #d4ede1;
            --sidebar-text:      #4a7060;
            --sidebar-heading:   #007a3f;
            --sidebar-hover-bg:  #f0faf5;
            --sidebar-hover-text:#009f52;
            --page-bg:           #f4fbf7;
            --card-bg:           #ffffff;
            --text-primary:      #1a2e22;
            --text-muted:        #5a7a68;
            --border:            #d8eee3;
            --code-bg:           #1a1527;
            --code-text:         #e2d9f3;
            --shadow-sm:         0 1px 4px rgba(0,159,82,0.08);
            --shadow-md:         0 4px 20px rgba(0,159,82,0.10), 0 1px 4px rgba(0,0,0,0.04);
        }}

        /* 全局重置 */
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; scroll-padding-top: 20px; }}

        body {{
            font-family: "PingFang SC", "Microsoft YaHei", -apple-system, Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background-color: var(--page-bg);
            max-width: 100%;
            margin: 0;
            padding-left: 240px;
            transition: padding-left 0.3s ease;
        }}
        body.toc-hidden {{ padding-left: 50px; }}

        /* ========== 左侧目录 ========== */
        .toc-wrapper {{
            position: fixed;
            top: 0; left: 0;
            width: 240px;
            height: 100vh;
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--sidebar-border);
            z-index: 999;
            overflow-y: auto;
            transition: transform 0.3s ease;
            padding: 0 0 20px;
            transform: translateX(0);
        }}
        .toc-wrapper.hidden {{ transform: translateX(-100%); }}

        /* 目录滚动条 */
        .toc-wrapper::-webkit-scrollbar {{ width: 4px; }}
        .toc-wrapper::-webkit-scrollbar-track {{ background: transparent; }}
        .toc-wrapper::-webkit-scrollbar-thumb {{ background: var(--accent-light2); border-radius: 2px; }}

        /* ========== 目录头部 ========== */
        .toc-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 18px 16px 14px;
            border-bottom: 1px solid var(--sidebar-border);
            margin-bottom: 8px;
            background: linear-gradient(135deg, #e6f7ef 0%, #ffffff 100%);
        }}
        .toc-header h2 {{
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--accent);
            margin: 0;
        }}
        .toc-toggle-btn {{
            width: 28px; height: 28px;
            border-radius: 6px;
            background: var(--accent-light);
            color: var(--accent);
            border: 1px solid var(--accent-light2);
            cursor: pointer;
            font-size: 14px;
            display: flex; align-items: center; justify-content: center;
            transition: all 0.2s ease;
        }}
        .toc-toggle-btn:hover {{
            background: var(--accent);
            color: #fff;
            border-color: var(--accent);
        }}

        /* ========== 目录列表 ========== */
        .toc-list, .toc-sublist {{ list-style: none; padding-left: 0; }}
        .toc-sublist {{ padding-left: 12px; margin-top: 2px; }}
        .toc-item {{ margin: 2px 0; padding: 0 8px; }}
        .toc-link {{
            text-decoration: none;
            color: var(--sidebar-text);
            font-size: 0.875rem;
            transition: all 0.15s ease;
            display: block;
            padding: 4px 8px;
            border-radius: 5px;
            border-left: 2px solid transparent;
        }}
        .toc-link:hover {{
            color: var(--sidebar-hover-text);
            background-color: var(--sidebar-hover-bg);
            border-left-color: var(--accent);
            padding-left: 10px;
        }}
        .toc-level-1 .toc-link {{
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--accent-deeper);
        }}
        .toc-level-2 .toc-link {{ color: #2d6e4e; }}
        .toc-level-3 .toc-link {{ color: #4e8a6a; }}
        .toc-level-4 .toc-link,
        .toc-level-5 .toc-link,
        .toc-level-6 .toc-link {{ color: #7aab92; font-size: 0.82rem; }}

        /* ========== 目录唤起按钮 ========== */
        .toc-reveal-btn {{
            position: fixed;
            top: 20px; left: 8px;
            width: 36px; height: 36px;
            border-radius: 8px;
            background: var(--accent);
            color: white;
            border: none;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0 2px 12px rgba(99,102,241,0.4);
            z-index: 998;
            opacity: 0; visibility: hidden;
            transition: all 0.3s ease;
            display: flex; align-items: center; justify-content: center;
        }}
        .toc-reveal-btn.show {{ opacity: 1; visibility: visible; }}
        .toc-reveal-btn:hover {{ background: var(--accent-dark); transform: scale(1.05); }}

        /* ========== 正文容器 ========== */
        .content-wrapper {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px 24px;
        }}
        .content {{
            background-color: var(--card-bg);
            padding: 24px 32px;
            border-radius: 10px;
            box-shadow: var(--shadow-md);
            border: 1px solid var(--border);
            margin-bottom: 20px;
        }}

        /* 标题 + 锚点偏移修复 */
        .anchor-heading {{
            position: relative;
            padding-top: 80px;
            margin-top: -80px;
        }}
        .content h1 {{
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--accent-deeper);
            margin: 20px 0 10px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--accent-light2);
            position: relative;
        }}
        .content h1::before {{
            content: '';
            position: absolute;
            bottom: -2px; left: 0;
            width: 56px; height: 2px;
            background: var(--accent);
        }}
        .content h2 {{
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--accent-dark);
            margin: 18px 0 8px;
            padding-left: 10px;
            position: relative;
        }}
        .content h2::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 80px;
            width: 3px;
            height: calc(100% - 80px);
            background: var(--accent);
            border-radius: 2px;
        }}
        .content h3 {{
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 14px 0 6px;
        }}
        .content h4, .content h5, .content h6 {{
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-muted);
            margin: 12px 0 6px;
        }}

        /* 图片样式 */
        .content-img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: var(--shadow-md);
            margin: 10px auto;
            display: block;
            opacity: 0;
            transition: opacity 0.5s ease;
            cursor: zoom-in;
        }}
        .content-img.loaded {{ opacity: 1; }}

        /* 段落/列表 */
        .content p {{ margin: 6px 0; font-size: 1rem; line-height: 1.7; color: var(--text-primary); }}
        .content ul, .content ol {{ padding-left: 20px; margin: 6px 0 6px 10px; }}
        .content li {{ margin: 4px 0; }}
        .content a {{ color: var(--accent); text-decoration: none; border-bottom: 1px solid var(--accent-light2); transition: all 0.15s; }}
        .content a:hover {{ color: var(--accent-dark); border-bottom-color: var(--accent); }}

        /* 行内代码 */
        .content code {{
            font-family: "JetBrains Mono", "Fira Code", "Consolas", "Monaco", monospace;
            font-size: 0.875rem;
            background: #fff4e6;
            color: #b45309;
            padding: 1px 5px;
            border-radius: 4px;
            border: 1px solid #fde8c0;
        }}

        /* 代码块 */
        .content pre {{
            background: var(--code-bg);
            color: var(--code-text);
            padding: 14px 16px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 10px 0;
            border: 1px solid rgba(255,255,255,0.06);
            border-left: 3px solid #a78bfa;
            box-shadow: 0 4px 20px rgba(26,21,39,0.25);
        }}
        .content pre code {{
            background: none;
            color: inherit;
            padding: 0;
            border: none;
            font-size: 0.875rem;
        }}

        /* 表格 */
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            overflow-x: auto;
            display: block;
            border-radius: 8px;
            box-shadow: var(--shadow-sm);
        }}
        .content th, .content td {{
            border: 1px solid var(--border);
            padding: 10px 14px;
            text-align: left;
            font-size: 0.95rem;
        }}
        .content th {{
            background: linear-gradient(135deg, var(--accent-light), #f0faf5);
            font-weight: 600;
            color: var(--accent-deeper);
            white-space: nowrap;
        }}
        .content tr:nth-child(even) {{ background-color: #f9fdfb; }}
        .content tr:hover {{ background-color: var(--accent-light); }}

        /* 引用块 */
        .content blockquote {{
            border-left: 4px solid var(--accent);
            background: var(--accent-light);
            margin: 10px 0;
            padding: 10px 16px;
            border-radius: 0 8px 8px 0;
            color: var(--text-muted);
            font-style: italic;
        }}

        /* ========== Mermaid ========== */
        .mermaid {{
            margin: 16px 0;
            text-align: center;
            overflow-x: auto;
            cursor: zoom-in;
            padding: 16px;
            background: var(--accent-light);
            border-radius: 8px;
            border: 1px solid var(--accent-light2);
        }}

        /* ========== Lightbox ========== */
        .lightbox-svg {{
            display: none;
            width: 92vw; max-height: 88vh;
            transform-origin: center center;
            will-change: transform;
            background: #fff;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 25px 60px rgba(0,0,0,0.6);
            overflow: hidden;
            cursor: default;
            box-sizing: border-box;
        }}
        .lightbox-svg svg {{ width: 100% !important; height: auto !important; min-height: 400px; display: block; }}
        .lightbox-close {{
            position: fixed;
            top: 16px; right: 20px;
            width: 36px; height: 36px;
            border-radius: 8px;
            background: rgba(255,255,255,0.12);
            color: #fff;
            border: 1px solid rgba(255,255,255,0.25);
            font-size: 15px;
            cursor: pointer;
            z-index: 100000;
            display: flex; align-items: center; justify-content: center;
            transition: background 0.2s;
            backdrop-filter: blur(4px);
        }}
        .lightbox-close:hover {{ background: rgba(255,255,255,0.25); }}
        .lightbox-overlay {{
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,30,15,0.88);
            backdrop-filter: blur(2px);
            z-index: 99999;
            cursor: zoom-out;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}
        .lightbox-overlay.active {{ display: flex; }}
        .lightbox-img {{
            max-width: 90vw; max-height: 90vh;
            border-radius: 10px;
            box-shadow: 0 25px 60px rgba(0,0,0,0.6);
            object-fit: contain;
            cursor: default;
            transform-origin: center center;
            will-change: transform;
        }}

        /* ========== 回到顶部 ========== */
        .back-to-top {{
            position: fixed;
            bottom: 24px; right: 24px;
            background: linear-gradient(135deg, var(--accent), var(--accent-dark));
            color: white;
            width: 44px; height: 44px;
            border-radius: 10px;
            text-align: center;
            line-height: 44px;
            font-size: 18px;
            cursor: pointer;
            box-shadow: 0 4px 16px rgba(0,159,82,0.35);
            transition: all 0.3s ease;
            opacity: 0; visibility: hidden;
            z-index: 9999;
            touch-action: manipulation;
            border: none; outline: none;
        }}
        .back-to-top.show {{ opacity: 1; visibility: visible; }}
        .back-to-top:hover {{ transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,159,82,0.5); }}

        /* ========== 移动端 ========== */
        @media (max-width: 992px) {{
            body {{ padding-left: 0; }}
            body.toc-hidden {{ padding-left: 0; }}
            .toc-wrapper {{ width: 260px; transform: translateX(-100%); }}
            .toc-wrapper.hidden {{ transform: translateX(-100%); }}
            .toc-mobile-trigger {{ display: block !important; }}
            .toc-reveal-btn {{ display: none; }}
            .content-wrapper {{ padding: 16px 12px; }}
            .content {{ padding: 18px; }}
        }}

        /* ========== 移动端触发按钮 ========== */
        .toc-mobile-trigger {{
            position: fixed;
            top: 20px; left: 20px;
            width: 40px; height: 40px;
            border-radius: 8px;
            background: var(--accent);
            color: white;
            border: none;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0 2px 12px rgba(0,159,82,0.35);
            z-index: 9998;
            display: none;
        }}

        /* ========== 小屏 ========== */
        @media (max-width: 576px) {{
            .back-to-top {{ width: 38px; height: 38px; line-height: 38px; font-size: 15px; bottom: 16px; right: 16px; }}
            .content h1 {{ font-size: 1.5rem; }}
            .content h2 {{ font-size: 1.25rem; }}
            .content h3 {{ font-size: 1.1rem; }}
        }}

        .toc-wrapper.show {{ transform: translateX(0); }}
    </style>
</head>
<body>
    <!-- 左侧固定目录 -->
    <div class="toc-wrapper" id="tocWrapper">
        {toc_html}
    </div>

    <!-- 目录唤起按钮（隐藏后显示） -->
    <button class="toc-reveal-btn" id="tocRevealBtn">≡</button>

    <!-- 移动端目录触发按钮 -->
    <button class="toc-mobile-trigger" id="tocMobileTrigger">≡</button>

    <!-- 正文容器 -->
    <div class="content-wrapper">
        <div class="content">
            {soup.prettify()}
        </div>
    </div>

    <!-- 图片放大遮罩 -->
    <div class="lightbox-overlay" id="lightboxOverlay">
        <button class="lightbox-close" id="lightboxClose">✕</button>
        <img class="lightbox-img" id="lightboxImg" src="" alt="">
        <div class="lightbox-svg" id="lightboxSvg"></div>
    </div>

    <!-- 回到顶部按钮 -->
    <button class="back-to-top" id="backToTop">↑</button>

    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        // ========== 核心变量 ==========
        const tocWrapper = document.getElementById('tocWrapper');
        const tocToggleBtn = document.getElementById('tocToggleBtn');
        const tocRevealBtn = document.getElementById('tocRevealBtn');
        const tocMobileTrigger = document.getElementById('tocMobileTrigger');
        const body = document.body;

        // ========== 目录切换核心逻辑（修复隐藏后唤起） ==========
        function toggleToc() {{
            // 切换目录显示/隐藏
            tocWrapper.classList.toggle('hidden');
            // 切换body的padding（适配空间）
            body.classList.toggle('toc-hidden');
            // 显示/隐藏唤起按钮
            tocRevealBtn.classList.toggle('show');
            
            // 移动端特殊处理
            if (window.innerWidth <= 992) {{
                tocWrapper.classList.toggle('show');
            }}
        }}

        // 绑定点击事件
        tocToggleBtn.addEventListener('click', toggleToc); // 目录内隐藏按钮
        tocRevealBtn.addEventListener('click', toggleToc); // 隐藏后唤起按钮
        tocMobileTrigger.addEventListener('click', toggleToc); // 移动端触发按钮

        // ========== 回到顶部按钮逻辑 ==========
        const backToTopBtn = document.getElementById('backToTop');
        // 节流函数（优化滚动性能）
        function throttle(fn, delay) {{
            let timer = null;
            return function() {{
                if (!timer) {{
                    timer = setTimeout(() => {{
                        fn.apply(this, arguments);
                        timer = null;
                    }}, delay);
                }}
            }};
        }}
        // 滚动监听
        window.addEventListener('scroll', throttle(function() {{
            if (window.pageYOffset > 300) {{
                backToTopBtn.classList.add('show');
            }} else {{
                backToTopBtn.classList.remove('show');
            }}
        }}, 100));
        // 点击回到顶部
        backToTopBtn.addEventListener('click', function() {{
            window.scrollTo({{
                top: 0,
                behavior: 'smooth'
            }});
        }});

        // ========== 图片懒加载增强（兼容旧浏览器） ==========
        document.addEventListener('DOMContentLoaded', function() {{
            const lazyImages = document.querySelectorAll('.content-img[loading="lazy"]');
            // 检测图片是否进入视口
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        const img = entry.target;
                        // 加载完成后添加样式
                        img.onload = function() {{
                            img.classList.add('loaded');
                        }};
                        // 兼容：手动触发加载
                        if (img.complete) {{
                            img.classList.add('loaded');
                        }}
                        // 停止观察已加载的图片
                        observer.unobserve(img);
                    }}
                }});
            }}, {{
                rootMargin: '200px 0px', // 提前200px开始加载
                threshold: 0.01
            }});
            // 观察所有懒加载图片
            lazyImages.forEach(img => {{
                observer.observe(img);
            }});

            // 初始触发滚动检查
            window.dispatchEvent(new Event('scroll'));

            // 初始化：大屏显示目录，小屏隐藏
            if (window.innerWidth > 992) {{
                tocWrapper.classList.remove('hidden');
                body.classList.remove('toc-hidden');
                tocRevealBtn.classList.remove('show');
            }} else {{
                tocWrapper.classList.add('hidden');
                tocRevealBtn.classList.remove('show');
            }}
        }});

        // ========== 修复目录链接点击平滑滚动 ==========
        document.querySelectorAll('.toc-link').forEach(link => {{
            link.addEventListener('click', function(e) {{
                e.preventDefault();
                const targetId = this.getAttribute('href').slice(1);
                const target = document.getElementById(targetId);
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                    // 移动端点击目录后自动隐藏目录
                    if (window.innerWidth <= 992) {{
                        tocWrapper.classList.remove('show');
                        tocWrapper.classList.add('hidden');
                        body.classList.remove('toc-hidden');
                    }}
                }}
            }});
        }});

        // ========== 图片 & Mermaid 点击放大 ==========
        const lightboxOverlay = document.getElementById('lightboxOverlay');
        const lightboxImg = document.getElementById('lightboxImg');
        const lightboxSvg = document.getElementById('lightboxSvg');

        // 缩放/平移状态
        let lbScale = 1, lbX = 0, lbY = 0, lbActiveEl = null;

        function clampPan() {{
            // 根据当前缩放和容器尺寸限制平移范围，避免内容完全移出可视区
            if (!lbActiveEl) return;
            const rect = lbActiveEl.getBoundingClientRect();
            // 内容实际尺寸（未变换）
            const elW = rect.width / lbScale;
            const elH = rect.height / lbScale;
            // 可视区尺寸
            const vw = window.innerWidth;
            const vh = window.innerHeight;
            // 允许平移的最大幅度：至少保留 20% 内容在视窗内
            const maxX = (elW * lbScale * 0.8 + vw * 0.5) / 2;
            const maxY = (elH * lbScale * 0.8 + vh * 0.5) / 2;
            lbX = Math.min(maxX, Math.max(-maxX, lbX));
            lbY = Math.min(maxY, Math.max(-maxY, lbY));
        }}

        function applyTransform() {{
            if (!lbActiveEl) return;
            clampPan();
            lbActiveEl.style.transform = `translate(${{lbX}}px, ${{lbY}}px) scale(${{lbScale}})`;
        }}

        function resetTransform() {{
            lbScale = 1; lbX = 0; lbY = 0;
            applyTransform();
        }}

        function openLightboxImg(src, alt) {{
            lightboxImg.src = src;
            lightboxImg.alt = alt;
            lightboxImg.style.display = 'block';
            lightboxSvg.style.display = 'none';
            lightboxSvg.innerHTML = '';
            lbActiveEl = lightboxImg;
            resetTransform();
            lightboxOverlay.classList.add('active');
        }}

        function openLightboxSvg(svgEl) {{
            const clone = svgEl.cloneNode(true);
            if (!clone.getAttribute('viewBox')) {{
                const rect = svgEl.getBoundingClientRect();
                const w = rect.width || parseFloat(svgEl.getAttribute('width'));
                const h = rect.height || parseFloat(svgEl.getAttribute('height'));
                if (w && h) clone.setAttribute('viewBox', `0 0 ${{w}} ${{h}}`);
            }}
            clone.removeAttribute('width');
            clone.removeAttribute('height');
            clone.setAttribute('preserveAspectRatio', 'xMidYMid meet');
            clone.style.cssText = 'width:100%;height:auto;display:block;transform-origin:center center;will-change:transform;';
            lightboxSvg.innerHTML = '';
            lightboxSvg.appendChild(clone);
            lightboxImg.style.display = 'none';
            lightboxSvg.style.display = 'block';
            // 变换目标是白卡内部的 svg 元素，白卡本身保持不动
            lbActiveEl = lightboxSvg.querySelector('svg');
            resetTransform();
            lightboxOverlay.classList.add('active');
        }}

        function closeLightbox() {{
            lightboxOverlay.classList.remove('active');
            lightboxImg.style.display = 'none';
            lightboxSvg.style.display = 'none';
            lightboxSvg.innerHTML = '';
            resetTransform();
            lbActiveEl = null;
        }}

        // ===== 触控板捏合缩放 & 双指平移 =====
        // 挂在 document 捕获阶段，lightbox 开启时拦截所有 wheel 事件
        document.addEventListener('wheel', function(e) {{
            if (!lightboxOverlay.classList.contains('active')) return;
            e.preventDefault();
            if (!lbActiveEl) return;
            // 校正 deltaMode：0=像素(触控板), 1=行(鼠标滚轮), 2=页
            const lineH = 16;
            const dx = e.deltaMode === 1 ? e.deltaX * lineH : e.deltaX;
            const dy = e.deltaMode === 1 ? e.deltaY * lineH : e.deltaY;
            if (e.ctrlKey) {{
                // 捏合缩放：ctrlKey + deltaY
                const factor = dy < 0 ? 1.08 : 0.93;
                lbScale = Math.min(Math.max(0.2, lbScale * factor), 20);
            }} else {{
                // 双指平移
                lbX -= dx;
                lbY -= dy;
            }}
            applyTransform();
        }}, {{ passive: false, capture: true }});

        // 双击还原
        lightboxOverlay.addEventListener('dblclick', function(e) {{
            if (e.target === lightboxOverlay) return;
            resetTransform();
        }});

        document.querySelectorAll('.content-img').forEach(img => {{
            img.addEventListener('click', function() {{
                openLightboxImg(this.src, this.alt);
            }});
        }});

        // 用 MutationObserver 监听 Mermaid SVG 插入，确保渲染后再绑定
        document.querySelectorAll('.mermaid').forEach(function(el) {{
            // 5s 超时兜底：Mermaid 语法错误时渲染结果为文字而非 SVG，永不触发
            const timer = setTimeout(function() {{ obs.disconnect(); }}, 5000);
            const obs = new MutationObserver(function(mutations, observer) {{
                const svg = el.querySelector('svg');
                if (svg) {{
                    clearTimeout(timer);
                    observer.disconnect();
                    el.addEventListener('click', function() {{
                        const s = this.querySelector('svg');
                        if (s) openLightboxSvg(s);
                    }});
                }}
            }});
            obs.observe(el, {{ childList: true, subtree: true }});
        }});

        lightboxOverlay.addEventListener('click', function(e) {{
            if (e.target === lightboxOverlay) closeLightbox();
        }});
        document.getElementById('lightboxClose').addEventListener('click', closeLightbox);
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') closeLightbox();
        }});

        // ========== Mermaid 初始化 ==========
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});

        // ========== 窗口大小变化时适配 ==========
        window.addEventListener('resize', function() {{
            if (window.innerWidth > 992) {{
                // 大屏：恢复目录显示，隐藏唤起按钮
                tocWrapper.classList.remove('hidden', 'show');
                body.classList.remove('toc-hidden');
                tocRevealBtn.classList.remove('show');
            }} else {{
                // 小屏：隐藏目录，显示移动端触发按钮
                tocWrapper.classList.add('hidden');
                tocWrapper.classList.remove('show');
                body.classList.remove('toc-hidden');
                tocRevealBtn.classList.remove('show');
            }}
        }});
    </script>
</body>
</html>
    """

    # 6. 写入HTML文件
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"转换完成！HTML文件已保存至：{html_file_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="将Markdown文件转换为带目录的HTML文件")
    parser.add_argument("input", help="输入的Markdown文件路径")
    parser.add_argument("-o", "--output", help="输出的HTML文件路径（默认同目录同名）", default=None)
    parser.add_argument("-t", "--title", help="HTML页面标题（默认为Markdown转换结果）", default="Markdown转换结果")
    args = parser.parse_args()
    md_to_html_with_toc(args.input, args.output, title=args.title)