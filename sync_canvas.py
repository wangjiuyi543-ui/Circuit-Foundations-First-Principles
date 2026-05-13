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

    # ===================== 核心修复：预先生成全局唯一ID映射 =====================
    # 关键：用Obsidian原生的node_id作为key，每个节点永远对应同一个Mermaid ID
    node_info = {}  # 格式：{ node_id: (mermaid_id, display_name) }
    id_counter = 0

    for node in data.get('nodes', []):
        node_id = node.get('id')
        if not node_id:
            continue
        
        # 提取显示名称
        raw_name = node.get('file', node.get('text', '未命名节点'))
        display_name = raw_name.split('/')[-1].replace('.md', '')
        
        # 生成全局唯一的Mermaid ID（用数字后缀，绝对不会重复）
        mermaid_id = f"node_{id_counter}"
        id_counter += 1
        
        # 保存映射关系
        node_info[node_id] = (mermaid_id, display_name)

    if not node_info:
        print("⚠️  白板中没有找到任何有效节点")
        exit(0)

    # ===================== 优化Mermaid配置 =====================
    mermaid_lines = [
        "%%{init: {"
        "'theme':'neutral', "
        "'flowchart': {"
        "'nodeSpacing': 50, "  # 同级节点间距
        "'rankSpacing': 70, "  # 上下级节点间距
        "'curve': 'basis', "   # 平滑连线
        "'htmlLabels': true"   # 支持HTML换行
        "}"
        "}}%%",
        "graph TD",  # 从上到下布局，完全匹配你的白板
        # 统一节点样式：紫色圆角卡片，和Obsidian风格一致
        "    classDef default fill:#e8e0ff,stroke:#9370db,stroke-width:2px,rx:8px,ry:8px;"
    ]

    # ===================== 第一步：先定义所有节点（只定义一次！） =====================
    for mermaid_id, display_name in node_info.values():
        # 处理长文本自动换行（每15个字符换一行）
        wrapped_name = re.sub(r'(.{15})', r'\1<br>', display_name)
        mermaid_lines.append(f'    {mermaid_id}["{wrapped_name}"]')

    # ===================== 第二步：再添加所有连线 =====================
    for edge in data.get('edges', []):
        from_node_id = edge.get('fromNode')
        to_node_id = edge.get('toNode')
        
        # 跳过无效连线
        if from_node_id not in node_info or to_node_id not in node_info:
            continue
        
        from_mid = node_info[from_node_id][0]
        to_mid = node_info[to_node_id][0]
        
        mermaid_lines.append(f'    {from_mid} --> {to_mid}')

    # 拼接完整代码块
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
    
    print("✅ 流程图已完美生成！节点重复问题已彻底解决！")

if __name__ == "__main__":
    sync()
