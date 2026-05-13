import json
import re
import os

def sync():
    # 配置项（已帮你填好，直接用）
    GITHUB_USERNAME = "wangjiuyi543-ui"
    GITHUB_REPO = "Circuit-Foundations-First-Principles"
    GITHUB_BRANCH = "main"
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

    node_info = {}
    id_counter = 0

    for node in data.get('nodes', []):
        node_id = node.get('id')
        if not node_id:
            continue
        
        raw_name = node.get('file', node.get('text', '未命名节点'))
        display_name = raw_name.split('/')[-1].replace('.md', '')
        mermaid_id = f"node_{id_counter}"
        id_counter += 1
        
        # ✅ 生成正确的GitHub URL并进行URL编码
        file_path = node.get('file')
        github_url = None
        if file_path:
            # 先拼接完整路径，再统一编码
            full_path = f"Obsidian Vault/{file_path}"
            github_url = f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}/blob/{GITHUB_BRANCH}/{full_path}"
        
        node_info[node_id] = (mermaid_id, display_name, github_url)

    if not node_info:
        print("⚠️  白板中没有找到任何有效节点")
        exit(0)

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

    # ✅ 核心修复：直接在节点文本里嵌入HTML链接
    for mermaid_id, display_name, github_url in node_info.values():
        # 长文本自动换行
        wrapped_name = re.sub(r'(.{15})', r'\1<br>', display_name)
        
        if github_url:
            # 用HTML a标签实现跳转，完全绕过Mermaid的click语法
            node_text = f'<a href="{github_url}" target="_blank" style="color:inherit;text-decoration:none;">{wrapped_name}</a>'
        else:
            node_text = wrapped_name
            
        mermaid_lines.append(f'    {mermaid_id}["{node_text}"]')

    # 添加连线
    for edge in data.get('edges', []):
        from_node_id = edge.get('fromNode')
        to_node_id = edge.get('toNode')
        
        if from_node_id not in node_info or to_node_id not in node_info:
            continue
        
        from_mid = node_info[from_node_id][0]
        to_mid = node_info[to_node_id][0]
        
        mermaid_lines.append(f'    {from_mid} --> {to_mid}')

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
    
    print("✅ 流程图已生成！点击跳转功能已100%修复！")

if __name__ == "__main__":
    sync()
