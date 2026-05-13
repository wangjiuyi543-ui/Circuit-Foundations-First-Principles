import json
import re

# 1. 读取 Canvas 文件
with open('Obsidian Vault/未命名.canvas', 'r', encoding='utf-8') as f:
    canvas_data = json.load(f)

nodes = {node['id']: node.get('file', node.get('text', 'Node')) for node in canvas_data['nodes']}
edges = canvas_data['edges']

# 2. 生成 Mermaid 语法
mermaid_lines = ["graph LR"]
for edge in edges:
    from_node = nodes.get(edge['fromNode'], "Unknown").split('/')[-1].replace('.md', '')
    to_node = nodes.get(edge['toNode'], "Unknown").split('/')[-1].replace('.md', '')
    mermaid_lines.append(f'    {from_node} --> {to_node}')

mermaid_code = "\n".join(mermaid_lines)

# 3. 更新 README.md
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

# 使用正则表达式替换标记之间的内容
new_readme = re.sub(
    r'<!-- START_CANVAS -->.*?<!-- END_CANVAS -->',
    f'<!-- START_CANVAS -->\n```mermaid\n{mermaid_code}\n
```\n<!-- END_CANVAS -->',
    readme,
    flags=re.DOTALL
)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_readme)
