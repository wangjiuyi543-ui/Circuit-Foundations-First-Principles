import json
import re
import os

def sync():
    # ✅ 保持路径完全一致
    CANVAS_FILE = "Obsidian Vault/未命名.canvas"
    README_FILE = "README.md"

    if not os.path.exists(CANVAS_FILE):
        print(f"❌ 错误：未找到 {CANVAS_FILE}")
        exit(1)
    print(f"✅ 找到白板文件：{CANVAS_FILE}")

    with open(CANVAS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. 建立全局节点字典 (键: 原生UUID, 值: 显示名称)
    nodes = {}
    for node in data.get('nodes', []):
        node_id = node.get('id')
        if not node_id:
            continue
        raw_name = node.get('file', node.get('text', '未命名节点'))
        display_name = raw_name.split('/')[-1].replace('.md', '')
        nodes[node_id] = display_name

    if not nodes:
        print("⚠️  白板中没有找到任何节点")

    # 2. 生成 Mermaid (核心修正：基于底层节点ID实现物理拓扑连接)
    mermaid_lines = ["graph LR"]
    
    for edge in data.get('edges', []):
        from_id = edge.get('fromNode')
        to_id = edge.get('toNode')

        # 确保节点确实存在于字典中
        if from_id not in nodes or to_id not in nodes:
            continue

        from_name = nodes[from_id]
        to_name = nodes[to_id]

        # 【关键修复】直接将 Obsidian 原生的一长串 UUID 转换为 Mermaid 锚点
        # 无论它连接多少次，同一个卡片永远映射到同一个锚点上，彻底实现树状闭环
        f_key = "id_" + re.sub(r'\W', '', from_id)
        t_key = "id_" + re.sub(r'\W', '', to_id)

        mermaid_lines.append(f'    {f_key}["{from_name}"] --> {t_key}["{to_name}"]')

    mermaid_block = "\n```mermaid\n" + "\n".join(mermaid_lines) + "\n
```\n"

    # 3. 写入 README
    with open(README_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    START_MARKER = "<!-- START_CANVAS -->"
    END_MARKER = "<!-- END_CANVAS -->"

    pattern = re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER)
    new_content = re.sub(pattern, START_MARKER + mermaid_block + END_MARKER, content, flags=re.DOTALL)

    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ 完美的树状图已生成！")

if __name__ == "__main__":
    sync()
