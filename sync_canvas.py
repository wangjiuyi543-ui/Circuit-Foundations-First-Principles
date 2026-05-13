import json
import re
import os

def sync():
    CANVAS_FILE = "Obsidian Vault/未命名.canvas"
    README_FILE = "README.md"

    if not os.path.exists(CANVAS_FILE):
        print(f"❌ 错误：未找到 {CANVAS_FILE}")
        exit(1)
    print(f"✅ 找到白板文件：{CANVAS_FILE}")

    try:
        with open(CANVAS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 读取失败：{str(e)}")
        exit(1)

    # ===================== 核心修复：预先生成全局唯一节点ID =====================
    nodes = {}  # node_id => 显示名称
    node_id_map = {}  # 显示名称 => 全局唯一Mermaid ID
    id_counter = 0

    for node in data.get('nodes', []):
        node_id = node.get('id')
        if not node_id:
            continue
        
        raw_name = node.get('file', node.get('text', '未命名节点'))
        display_name = raw_name.split('/')[-1].replace('.md', '')
        nodes[node_id] = display_name

        # 同一个显示名称永远对应同一个ID，彻底解决节点重复问题
        if display_name not in node_id_map:
            clean_name = re.sub(r'[^\w\u4e00-\u9fa5]', '', display_name) or f"Node{id_counter}"
            node_id_map[display_name] = f"{clean_name}_{id_counter}"
            id_counter += 1

    if not nodes:
        print("⚠️  白板中没有找到任何节点")

    # ===================== 优化Mermaid配置 =====================
    mermaid_lines = [
        "%%{init: {'theme':'neutral', 'flowchart': {'nodeSpacing': 60, 'rankSpacing': 80, 'curve': 'basis'}}}%%",
        "graph TD",  # 从上到下布局，完全匹配你的白板方向
        "    classDef default fill:#e8e0ff,stroke:#9370db,stroke-width:2px,rx:8px,ry:8px;"  # 紫色卡片样式，和Obsidian一致
    ]

    # 生成边（现在同一个节点只会出现一次）
    for edge in data.get('edges', []):
        from_id = edge.get('fromNode')
        to_id = edge.get('toNode')
        
        from_name = nodes.get(from_id, "未知节点")
        to_name = nodes.get(to_id, "未知节点")

        f_key = node_id_map[from_name]
        t_key = node_id_map[to_name]

        mermaid_lines.append(f'    {f_key}["{from_name}"] --> {t_key}["{to_name}"]')

    mermaid_block = "\n```mermaid\n" + "\n".join(mermaid_lines) + "\n```\n"

    # 更新README
    try:
        with open(README_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ 错误：未找到 {README_FILE}")
        exit(1)

    START_MARKER = "<!-- START_CANVAS -->"
    END_MARKER = "<!-- END_CANVAS -->"

    if START_MARKER not in content or END_MARKER not in content:
        print(f"❌ 错误：README中缺少标记")
        exit(1)

    pattern = re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER)
    new_content = re.sub(pattern, START_MARKER + mermaid_block + END_MARKER, content, flags=re.DOTALL)

    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ 优化版流程图已生成！")

if __name__ == "__main__":
    sync()
