"""
将 Markdown + LaTeX 文件转换为微信公众号兼容的 HTML
用法: python md2wechat.py 103.md
输出: 103_wechat.html (可直接全选复制粘贴到微信公众号编辑器)
"""
import sys
import re
import html
import urllib.parse
import textwrap

# ─── 微信主题样式 ───────────────────────────────────────────
CSS = textwrap.dedent("""\
    /* 全局 */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        max-width: 677px; margin: 0 auto; padding: 20px 16px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                     "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", sans-serif;
        font-size: 15px; line-height: 1.85; color: #2f2f2f;
        background: #fff; -webkit-font-smoothing: antialiased;
    }
    /* 标题 */
    h2 {
        font-size: 22px; font-weight: 700; color: #1a1a1a;
        margin: 36px 0 18px; padding-bottom: 8px;
        border-bottom: 2px solid #1e6fff; text-align: center;
    }
    h3 {
        font-size: 18px; font-weight: 700; color: #1e6fff;
        margin: 28px 0 14px; padding-left: 12px;
        border-left: 4px solid #1e6fff;
    }
    h4 {
        font-size: 16px; font-weight: 700; color: #333;
        margin: 24px 0 12px;
    }
    /* 段落 */
    p { margin: 10px 0; }
    /* 加粗 */
    strong { color: #1e6fff; font-weight: 600; }
    /* 列表 */
    ul, ol { margin: 8px 0; padding-left: 24px; }
    li { margin: 4px 0; }
    /* 引用块 */
    blockquote {
        background: #f7f9fc; border-left: 4px solid #1e6fff;
        margin: 14px 0; padding: 12px 16px; color: #555;
        font-size: 14px; border-radius: 0 6px 6px 0;
    }
    /* 行间公式居中 */
    .display-math { display: block; text-align: center; margin: 16px 0; overflow-x: auto; }
    .display-math img { max-width: 100%; height: auto; }
    /* 行内公式 */
    .inline-math img { vertical-align: middle; max-height: 20px; }
    /* 分割线 */
    hr {
        border: none; height: 1px;
        background: linear-gradient(to right, transparent, #d0d7de, transparent);
        margin: 24px 0;
    }
    /* 加粗标题块 */
    .bold-block {
        font-weight: 700; font-size: 16px; color: #1a1a1a; margin: 16px 0 8px;
    }
""")

# CodeCogs API 渲染 LaTeX → SVG 图片 URL
def latex_to_svg_url(latex_code, inline=True):
    """将 LaTeX 公式转为 CodeCogs SVG 图片 URL"""
    # 去除首尾空白但保留内部结构
    code = latex_code.strip()
    if inline:
        # 行内公式用 \inline
        encoded = urllib.parse.quote(r'\inline ' + code, safe='')
    else:
        # 行间公式不加 \inline
        encoded = urllib.parse.quote(code, safe='')
    # 使用 svg 格式，默认黑色文字
    return f'https://latex.codecogs.com/svg.image?{encoded}'


def process_inline_math(text):
    """处理行内公式 $...$，转为带 inline-math 类的 span"""
    pattern = re.compile(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', re.DOTALL)

    def replacer(m):
        latex_code = m.group(1)
        svg_url = latex_to_svg_url(latex_code, inline=True)
        return f'<span class="inline-math"><img src="{svg_url}" alt="{html.escape(latex_code)}" /></span>'

    return pattern.sub(replacer, text)


def process_display_math(text):
    """处理行间公式 $$...$$，转为带 display-math 类的 div"""
    pattern = re.compile(r'\$\$(.+?)\$\$', re.DOTALL)

    def replacer(m):
        latex_code = m.group(1).strip()
        svg_url = latex_to_svg_url(latex_code, inline=False)
        return f'<div class="display-math"><img src="{svg_url}" alt="{html.escape(latex_code)}" /></div>'

    return pattern.sub(replacer, text)


def markdown_to_wechat_html(md_text):
    """将 Markdown 文本转为微信公众号兼容的 HTML"""
    # 跳过 YAML front matter
    lines = md_text.split('\n')
    content_lines = []
    in_frontmatter = False
    fm_count = 0

    for line in lines:
        if line.strip() == '---':
            fm_count += 1
            if fm_count == 1:
                in_frontmatter = True
                continue
            elif fm_count == 2:
                in_frontmatter = False
                continue
        if in_frontmatter:
            continue
        content_lines.append(line)

    md_text = '\n'.join(content_lines)

    # 先处理 LaTeX 公式（在 Markdown 转换之前，避免被转义）
    md_text = process_display_math(md_text)
    md_text = process_inline_math(md_text)

    # 逐行处理剩余 Markdown
    output_lines = []
    in_list = False

    for line in md_text.split('\n'):
        stripped = line.strip()

        # 空行
        if not stripped:
            if in_list:
                output_lines.append('</ul>')
                in_list = False
            continue

        # 标题
        if stripped.startswith('#### '):
            if in_list:
                output_lines.append('</ul>')
                in_list = False
            text = stripped[5:]
            output_lines.append(f'<h4>{text}</h4>')
            continue

        if stripped.startswith('### '):
            if in_list:
                output_lines.append('</ul>')
                in_list = False
            text = stripped[4:]
            output_lines.append(f'<h3>{text}</h3>')
            continue

        if stripped.startswith('## '):
            if in_list:
                output_lines.append('</ul>')
                in_list = False
            text = stripped[3:]
            output_lines.append(f'<h2>{text}</h2>')
            continue

        # 分割线
        if stripped == '---':
            if in_list:
                output_lines.append('</ul>')
                in_list = False
            output_lines.append('<hr />')
            continue

        # 引用块
        if stripped.startswith('> '):
            if in_list:
                output_lines.append('</ul>')
                in_list = False
            text = stripped[2:]
            text = process_bold(text)
            output_lines.append(f'<blockquote><p>{text}</p></blockquote>')
            continue

        # 无序列表
        if stripped.startswith('- '):
            if not in_list:
                output_lines.append('<ul>')
                in_list = True
            text = stripped[2:]
            text = process_bold(text)
            output_lines.append(f'<li>{text}</li>')
            continue

        # 包含 display-math div 的行（已经处理好，直接保留）
        if stripped.startswith('<div class="display-math">'):
            if in_list:
                output_lines.append('</ul>')
                in_list = False
            output_lines.append(stripped)
            continue

        # 普通段落
        if in_list:
            output_lines.append('</ul>')
            in_list = False
        text = process_bold(stripped)
        output_lines.append(f'<p>{text}</p>')

    if in_list:
        output_lines.append('</ul>')

    body = '\n'.join(output_lines)

    # 后处理：修复标题中的 inline-math
    body = re.sub(r'<h([234])>(.*?)</h\1>', lambda m: f'<h{m.group(1)}>{m.group(2)}</h{m.group(1)}>', body)

    return body


def process_bold(text):
    """处理 **加粗** 标记"""
    # 先保护已经处理好的 HTML 标签
    protected = {}

    def protect(m):
        key = f'__PROTECTED_{len(protected)}__'
        protected[key] = m.group(0)
        return key

    # 保护已有 HTML 标签（img, span, div 等）
    text = re.sub(r'<(img|span|div|blockquote|ul|ol|li)[^>]*>.*?</\1>', protect, text, flags=re.DOTALL)
    text = re.sub(r'<(img|span|div|hr)[^>]*/?>', protect, text)

    # 处理 **bold**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    # 还原保护的内容
    for key, val in protected.items():
        text = text.replace(key, val)

    return text


def generate_wechat_html(md_file_path):
    """主函数：读取 Markdown 并生成微信公众号 HTML"""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    body_html = markdown_to_wechat_html(md_text)

    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微信公众号排版</title>
    <style>{CSS}
    </style>
</head>
<body>
{body_html}
</body>
</html>"""

    output_path = md_file_path.replace('.md', '_wechat.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f'[OK] 已生成: {output_path}')
    print('  打开该 HTML 文件 -> 全选(Ctrl+A) -> 复制(Ctrl+C) -> 粘贴到微信公众号编辑器即可。')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python md2wechat.py <markdown文件>')
        sys.exit(1)
    generate_wechat_html(sys.argv[1])
