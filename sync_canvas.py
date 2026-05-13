import json
import re
import os
import glob

# 1. 自动定位 Canvas 文件（防止文件名或路径微小偏差）
vault_path = 'Obsidian Vault'
canvas_files = glob.glob(os.path.join(vault_path, '*.canvas'))

if not canvas_files:
    print(f"错误：在 {vault_path} 文件夹中没有找到任何 .canvas 文件！")
    exit(1)

target_canvas = canvas_files[0]
print(f"正在解析白板文件: {target_canvas}")

# 2. 读取数据
with open(target_canvas, 'r', encoding='utf-8') as f:
    canvas_data = json.load(f)

# 提取节点信息
nodes = {}
for node in canvas_data.get('nodes', []):
    # 优先获取文件名，如果没有则是文字节点
    name = node.get('file', node.get('text', 'Node'))
    nodes[node['id']] = name.split('/')[-1].replace('.md', '')

# 3. 生成 Mermaid 语法
mermaid_lines = ["graph LR"]
for edge in canvas_data.get('edges', []):
    from_node = nodes.get(edge['fromNode'], "Unknown")
    to_node = nodes.get(edge['toNode'], "Unknown")
    # 清洗一下名称中的特殊字符
    clean_from = re.sub(r'[^\w\u4e00-\u9fa5]', '_', from_node)
    clean_to = re.sub(r'[^\w\u4e00-\u9fa5]', '_', to_node)
    mermaid_lines.append(f'    {clean_from}["{from_node}"] --> {clean_to}["{to_node}"]')

mermaid_code = "\n".join(mermaid_lines)

# 4. 更新 README.md
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

# 检查标记是否存在
if '' not in readme:
    print("错误：在 README.md 中没找到 标记")
    exit(1)

new_readme = re.sub(
    r'.*?',
    f'\n```mermaid\n{mermaid_code}\n```\n',
    readme,
    flags=re.DOTALL
)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_readme)

print("成功：README 中的逻辑树已更新！")

