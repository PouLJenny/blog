import re
import os
from markdown import markdown
from bs4 import BeautifulSoup

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

    # 2. 将Markdown转换为HTML（启用扩展）
    html_content = markdown(
        md_content,
        extensions=[
            'extra',       # 支持表格、列表等扩展语法
            'toc',         # 基础TOC（备用）
            'fenced_code', # 代码块
            'tables',      # 表格
            'md_in_html'   # 支持HTML混合
        ]
    )

    # 3. 解析HTML，提取标题+处理图片懒加载
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
        /* 全局重置 + 基础样式 */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        html {{
            scroll-behavior: smooth; /* 平滑滚动 */
            scroll-padding-top: 20px; /* 修复锚点跳转偏移 */
        }}
        body {{
            font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background-color: #f8f9fa;
            padding: 0;
            max-width: 100%;
            margin: 0;
            /* 为左侧目录+唤起按钮预留空间 */
            padding-left: 280px;
            transition: padding-left 0.3s ease;
        }}
        /* 目录隐藏时，减少左侧预留空间（只留唤起按钮宽度） */
        body.toc-hidden {{
            padding-left: 60px;
        }}

        /* ========== 左侧目录容器（核心修复） ========== */
        .toc-wrapper {{
            position: fixed;
            top: 0;
            left: 0;
            width: 280px;
            height: 100vh;
            background-color: #fff;
            box-shadow: 2px 0 12px rgba(0,0,0,0.08);
            z-index: 999;
            overflow-y: auto; /* 目录过长时滚动 */
            transition: transform 0.3s ease;
            padding: 20px 0;
            transform: translateX(0); /* 默认显示 */
        }}
        /* 目录隐藏状态（滑出左侧，但保留唤起按钮） */
        .toc-wrapper.hidden {{
            transform: translateX(-220px); /* 只隐藏主体，留60px给唤起按钮 */
        }}

        /* ========== 目录唤起按钮（隐藏后显示） ========== */
        .toc-reveal-btn {{
            position: fixed;
            top: 50%;
            left: 20px;
            transform: translateY(-50%);
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 18px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            z-index: 998;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        /* 目录隐藏时显示唤起按钮 */
        .toc-reveal-btn.show {{
            opacity: 1;
            visibility: visible;
        }}

        /* ========== 目录头部（标题+切换按钮） ========== */
        .toc-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px 15px;
            border-bottom: 2px solid #e9ecef;
            margin-bottom: 15px;
        }}
        .toc-header h2 {{
            font-size: 1.3rem;
            color: #2c3e50;
            margin: 0;
        }}
        /* 目录内部隐藏按钮 */
        .toc-toggle-btn {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }}
        .toc-toggle-btn:hover {{
            background-color: #0056b3;
            transform: scale(1.05);
        }}

        /* ========== 目录列表样式 ========== */
        .toc-list, .toc-sublist {{
            list-style: none;
            padding-left: 0;
        }}
        .toc-sublist {{
            padding-left: 18px;
            margin-top: 4px;
        }}
        .toc-item {{
            margin: 6px 0;
            line-height: 1.5;
            padding: 0 20px;
        }}
        .toc-link {{
            text-decoration: none;
            color: #007bff;
            font-size: 0.95rem;
            transition: all 0.2s ease;
            display: block;
            padding: 2px 4px;
            border-radius: 4px;
        }}
        .toc-link:hover {{
            color: #0056b3;
            background-color: #f0f7ff;
            text-decoration: none;
            padding-left: 6px;
        }}
        .toc-level-1 {{
            font-size: 1.05rem !important;
            font-weight: 600;
        }}
        .toc-level-2 {{ color: #2d3748; }}
        .toc-level-3 {{ color: #4a5568; }}
        .toc-level-4, .toc-level-5, .toc-level-6 {{ 
            color: #718096;
            font-size: 0.9rem !important;
        }}

        /* ========== 正文容器样式 ========== */
        .content-wrapper {{
            max-width: 900px;
            margin: 0 auto;
            padding: 30px 20px;
        }}
        .content {{
            background-color: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            margin-bottom: 40px; /* 给回到顶部按钮留空间 */
        }}

        /* 标题样式 + 锚点偏移修复 */
        .anchor-heading {{
            position: relative;
            padding-top: 80px; /* 修复跳转偏移 */
            margin-top: -80px;
        }}
        .content h1 {{
            font-size: 2rem;
            color: #2c3e50;
            margin: 40px 0 20px;
            border-bottom: 3px solid #e9ecef;
            padding-bottom: 12px;
        }}
        .content h2 {{
            font-size: 1.7rem;
            color: #2c3e50;
            margin: 35px 0 18px;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 10px;
        }}
        .content h3 {{
            font-size: 1.4rem;
            color: #2c3e50;
            margin: 30px 0 15px;
        }}
        .content h4, .content h5, .content h6 {{
            font-size: 1.2rem;
            color: #2c3e50;
            margin: 25px 0 12px;
        }}

        /* 图片样式 + 懒加载过渡 */
        .content-img {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 20px auto;
            display: block; /* 居中显示 */
            /* 懒加载过渡效果 */
            opacity: 0;
            transition: opacity 0.5s ease;
        }}
        /* 图片加载完成后显示 */
        .content-img.loaded {{
            opacity: 1;
        }}

        /* 段落/列表样式 */
        .content p {{
            margin: 12px 0;
            font-size: 1rem;
            line-height: 1.8;
        }}
        .content ul, .content ol {{
            padding-left: 25px;
            margin: 10px 0 10px 15px;
        }}
        .content li {{
            margin: 8px 0;
        }}

        /* 代码块样式（修复响应式） */
        .content pre {{
            background-color: #f8f9fa;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            border: 1px solid #e9ecef;
        }}
        .content code {{
            font-family: "Consolas", "Monaco", "Menlo", monospace;
            font-size: 0.9rem;
        }}
        .content pre code {{
            background: none;
            padding: 0;
        }}

        /* 表格样式（修复溢出） */
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            overflow-x: auto;
            display: block; /* 响应式滚动 */
        }}
        .content th, .content td {{
            border: 1px solid #dee2e6;
            padding: 12px 15px;
            text-align: left;
        }}
        .content th {{
            background-color: #f8f9fa;
            font-weight: 600;
            white-space: nowrap; /* 表头不换行 */
        }}
        .content tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}

        /* ========== 回到顶部按钮样式 ========== */
        .back-to-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #007bff;
            color: white;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            text-align: center;
            line-height: 48px;
            font-size: 18px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
            opacity: 0;
            visibility: hidden;
            z-index: 9999;
            /* 修复点击区域 */
            touch-action: manipulation;
            border: none;
            outline: none;
        }}
        .back-to-top.show {{
            opacity: 1;
            visibility: visible;
        }}
        .back-to-top:hover {{
            background-color: #0056b3;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        }}

        /* ========== 移动端适配（≤992px） ========== */
        @media (max-width: 992px) {{
            body {{
                padding-left: 0; /* 取消左侧预留空间 */
            }}
            body.toc-hidden {{
                padding-left: 0; /* 移动端取消偏移 */
            }}
            /* 移动端目录改为悬浮层 */
            .toc-wrapper {{
                width: 260px;
                transform: translateX(-100%); /* 默认隐藏 */
                box-shadow: 4px 0 15px rgba(0,0,0,0.15);
            }}
            .toc-wrapper.hidden {{
                transform: translateX(-100%); /* 移动端完全隐藏 */
            }}
            /* 移动端唤起按钮 */
            .toc-mobile-trigger {{
                display: block !important;
            }}
            /* 隐藏桌面端唤起按钮 */
            .toc-reveal-btn {{
                display: none;
            }}
            /* 正文容器适配 */
            .content-wrapper {{
                padding: 20px 15px;
            }}
            .content {{
                padding: 20px;
            }}
        }}

        /* ========== 移动端目录触发按钮 ========== */
        .toc-mobile-trigger {{
            position: fixed;
            top: 20px;
            left: 20px;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 18px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            z-index: 9998;
            display: none; /* 大屏隐藏 */
        }}

        /* ========== 小屏适配（≤576px） ========== */
        @media (max-width: 576px) {{
            .back-to-top {{
                width: 40px;
                height: 40px;
                line-height: 40px;
                font-size: 16px;
                bottom: 15px;
                right: 15px;
            }}
            .content h1 {{
                font-size: 1.8rem;
            }}
            .content h2 {{
                font-size: 1.5rem;
            }}
            .content h3 {{
                font-size: 1.3rem;
            }}
        }}

        /* ========== 目录显示状态 ========== */
        .toc-wrapper.show {{
            transform: translateX(0);
        }}
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

    <!-- 回到顶部按钮 -->
    <button class="back-to-top" id="backToTop">↑</button>

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


# 示例调用
if __name__ == "__main__":
    # 替换为你的Markdown文件路径
    md_file = "/home/poul/workspace/src/private_log/mba_study/zuzhixingwei/zuzhixingwei.md"
    # 可选：指定输出HTML路径，不指定则默认同目录同名
    html_file = "/home/poul/workspace/src/private_log/mba_study/zuzhixingwei/zuzhixingwei.html"
    # 转换
    md_to_html_with_toc(md_file, html_file, title="组织行为")