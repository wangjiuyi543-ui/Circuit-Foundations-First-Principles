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

    # ===================== 节点信息：ID => (MermaidID, 显示名称, 文件路径) =====================
    node_info = {}
    id_counter = 0

    for node in data.get('nodes', []):
        node_id = node.get('id')
        if not node_id:
            continue
        
        # 提取显示名称
        raw_name = node.get('file', node.get('text', '未命名节点'))
        display_name = raw_name.split('/')[-1].replace('.md', '')
        
        # 生成全局唯一Mermaid ID
        mermaid_id = f"node_{id_counter}"
        id_counter += 1
        
        # ✅ 新增：提取并转换文件路径（用于点击跳转）
        file_path = node.get('file')
        github_file_path = None
        if file_path:
            # 转换为GitHub仓库的相对路径（从根目录出发）
            github_file_path = f"./Obsidian Vault/{file_path}"
        
        # 保存所有信息
        node_info[node_id] = (mermaid_id, display_name, github_file_path)

    if not node_info:
        print("⚠️  白板中没有找到任何有效节点")
        exit(0)

    # ===================== Mermaid 配置 =====================
    mermaid_lines = [
        "%%{init: {"
        "'theme':'neutral', "
        "'flowchart': {"
        "'nodeSpacing': 50, "
        "'rankSpacing': 70, "
        "'curve': 'basis', "
        "'htmlLabels': true"
        "}"
        "}}%%",
        "graph TD",
        "    classDef default fill:#e8e0ff,stroke:#9370db,stroke-width:2px,rx:8px,ry:8px;"
    ]

    # 第一步：定义所有节点
    for mermaid_id, display_name, _ in node_info.values():
        # 长文本自动换行
        wrapped_name = re.sub(r'(.{15})', r'\1<br>', display_name)
        mermaid_lines.append(f'    {mermaid_id}["{wrapped_name}"]')

    # 第二步：添加所有连线
    for edge in data.get('edges', []):
        from_node_id = edge.get('fromNode')
        to_node_id = edge.get('toNode')
        
        if from_node_id not in node_info or to_node_id not in node_info:
            continue
        
        from_mid = node_info[from_node_id][0]
        to_mid = node_info[to_node_id][0]
        
        mermaid_lines.append(f'    {from_mid} --> {to_mid}')

    # ✅ 第三步：给有文件的节点添加点击跳转
    for mermaid_id, display_name, file_path in node_info.values():
        if file_path:
            # Mermaid 点击跳转语法：click 节点ID "URL" "鼠标悬停提示"
            mermaid_lines.append(f'    click {mermaid_id} "{file_path}" "点击打开对应笔记"')

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
    
    print("✅ 流程图已生成！所有关联笔记的节点都支持点击跳转！")

if __name__ == "__main__":
    sync()
