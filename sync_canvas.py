import json
import re
import os
import glob

# 1. 自动定位 Canvas 文件
vault_path = 'Obsidian Vault'
canvas_files = glob.glob(os.path.join(vault_path, '*.canvas'))

if not canvas_files:
    print(f"Error: No .canvas file found in {vault_path}")
    exit(1)

target_canvas = canvas_files[0]
print(f"Processing: {target_canvas}")

# 2. 读取数据
with open(target_canvas, 'r', encoding='utf-8') as f:
    canvas_data = json.load(f)

# 提取节点，只保留文件名
nodes = {}
for node in canvas_data.get('nodes', []):
    name = node.get('file', node.get('text', 'Node'))
    nodes[node['id']] = name.split('/')[-1].replace('.md', '')

# 3. 生成 Mermaid 语法
mermaid_lines = ["graph LR"]
for edge in canvas_data.get('edges', []):
    from_name = nodes.get(edge['fromNode'], "Unknown")
    to_name = nodes.get(edge['toNode'], "Unknown")
    # 清洗特殊字符，防止 Mermaid 渲染失败
    clean_from = re.sub(r'[^\w\u4e00-\u9fa5]', '_', from_name)
    clean_to = re.sub(r'[^\w\u4e00-\u9fa5]', '_', to_name)
    mermaid_lines.append(f'    {clean_from}["{from_name}"] --> {clean_to}["{to_node}"]')

mermaid_content = "\n```mermaid\n" + "\n".join(mermaid_lines) + "\n
```\n"

# 4. 更新 README.md
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

marker_start = "<!-- START_CANVAS -->"
marker_end = "<!-- END_CANVAS -->"

if marker_start not in readme:
    print("Error: Markers not found in README.md")
    exit(1)

# 使用切片方式替换，比正则更稳
parts = readme.split(marker_start)
rest = parts[1].split(marker_end)
new_readme = parts[0] + marker_start + mermaid_content + marker_end + rest[1]

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_readme)

print("Success: README logic tree updated!")
