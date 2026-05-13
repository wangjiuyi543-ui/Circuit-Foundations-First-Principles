import json
import re
import os

def sync():
    # ✅ 完全匹配你现在的文件路径
    CANVAS_FILE = "Obsidian Vault/未命名.canvas"
    README_FILE = "README.md"

    # 1. 检查文件是否存在
    if not os.path.exists(CANVAS_FILE):
        print(f"❌ 错误：未找到 {CANVAS_FILE}")
        exit(1)
    print(f"✅ 找到白板文件：{CANVAS_FILE}")

    # 2. 解析Canvas JSON
    try:
        with open(CANVAS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("❌ 错误：Canvas文件格式损坏")
        exit(1)
    except Exception as e:
        print(f"❌ 读取失败：{str(e)}")
        exit(1)

    # 3. 提取节点
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

    # 4. 生成Mermaid（解决ID重复问题）
    mermaid_lines = ["graph LR"]
    used_keys = set()

    def clean_key(name):
        return re.sub(r'[^\w\u4e00-\u9fa5]', '', name) or "Node"

    for edge in data.get('edges', []):
        from_id = edge.get('fromNode')
        to_id = edge.get('toNode')
        from_name = nodes.get(from_id, "未知节点")
        to_name = nodes.get(to_id, "未知节点")

        # 自动处理同名节点
        f_key = clean_key(from_name)
        t_key = clean_key(to_name)
        while f_key in used_keys:
            f_key += "_1"
        while t_key in used_keys:
            t_key += "_1"
        used_keys.add(f_key)
        used_keys.add(t_key)

        mermaid_lines.append(f'    {f_key}["{from_name}"] --> {t_key}["{to_name}"]')

    mermaid_block = "\n```mermaid\n" + "\n".join(mermaid_lines) + "\n```\n"

    # 5. 更新README
    try:
        with open(README_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ 错误：未找到 {README_FILE}")
        exit(1)

    START_MARKER = "<!-- START_CANVAS -->"
    END_MARKER = "<!-- END_CANVAS -->"

    if START_MARKER not in content or END_MARKER not in content:
        print(f"❌ 错误：README中缺少标记 {START_MARKER} 或 {END_MARKER}")
        exit(1)

    # 替换标记间内容
    pattern = re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER)
    new_content = re.sub(pattern, START_MARKER + mermaid_block + END_MARKER, content, flags=re.DOTALL)

    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ README流程图已生成！")

if __name__ == "__main__":
    sync()
