import json
import re
import os
import glob

def sync():
    # 1. 自动寻找白板文件
    vault_path = 'Obsidian Vault'
    canvas_files = glob.glob(os.path.join(vault_path, '*.canvas'))
    
    if not canvas_files:
        print(f"Error: No .canvas file found in {vault_path}")
        return

    target_canvas = canvas_files[0]
    print(f"Found Canvas: {target_canvas}")

    # 2. 深度解析 JSON
    with open(target_canvas, 'r', encoding='utf-8') as f:
        data = json.load(f)

    nodes = {}
    for node in data.get('nodes', []):
        # 提取标题，优先文件名，次选文本
        raw_name = node.get('file', node.get('text', 'Node'))
        display_name = raw_name.split('/')[-1].replace('.md', '')
        nodes[node['id']] = display_name

    # 3. 构造 Mermaid 语法
    mermaid_lines = ["graph LR"]
    for edge in data.get('edges', []):
        f_id, t_id = edge['fromNode'], edge['toNode']
        f_name = nodes.get(f_id, "Unknown")
        t_name = nodes.get(t_id, "Unknown")
        
        # 清洗 ID，只保留字母和汉字，防止 Mermaid 报错
        f_key = re.sub(r'[^\w\u4e00-\u9fa5]', '', f_name)
        t_key = re.sub(r'[^\w\u4e00-\u9fa5]', '', t_name)
        
        mermaid_lines.append(f'    {f_key}["{f_name}"] --> {t_key}["{t_name}"]')

    mermaid_block = "\n```mermaid\n" + "\n".join(mermaid_lines) + "\n
```\n"

    # 4. 精准写入 README
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    s_marker = "<!-- START_CANVAS -->"
    e_marker = "<!-- END_CANVAS -->"

    if s_marker not in content or e_marker not in content:
        print("Error: Markers missing in README.md")
        return

    # 采用正则替换，增强对换行符的兼容性
    pattern = re.escape(s_marker) + r".*?" + re.escape(e_marker)
    replacement = s_marker + mermaid_block + e_marker
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully updated README!")

if __name__ == "__main__":
    sync()
