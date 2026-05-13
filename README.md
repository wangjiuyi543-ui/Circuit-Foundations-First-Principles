这是一个专注于从第一性原理出发，通过严谨的数学（如线性代数、麦克斯韦方程组）推导电路原理核心命题的开源笔记仓库。

📖 项目初衷
在电子信息专业的学习中，工程近似固然重要，但对于追求本质的开发者来说，只有严谨的推导才能带来安全感。本项目旨在打破“背公式”的传统模式，复现每一个定理的底层逻辑。

🛠️ 推荐阅读方式（重点）
为了获得最佳的阅读体验（包括查看数学公式渲染和 Obsidian Canvas 画布思维导图），强烈建议采用以下方案：

本地使用 Obsidian 查看：

克隆本仓库到本地。

在 Obsidian 中将其作为“库（Vault）”打开。

安装并配置 Obsidian Git 插件以同步更新。

为什么不建议直接在网页端查看？：

GitHub 网页端目前无法直接渲染 Obsidian 的 .canvas 画布文件，会导致思维导图显示为 JSON 代码。

部分复杂的 LaTeX 公式在浏览器自动翻译下可能会出现显示异常。

🧠 核心内容
一阶线性动态系统响应：电容电压连续性的广义函数证明（冲激配平法），持续更新当中。

电路分析基本定理：KCL、KVL 与替代定理的严格证明。



🤝 贡献与交流
如果你也对严谨电路理论感兴趣，欢迎提交 Pull Request 或 Issue 进行探讨。
这也是我第一次用github上传知识，还有许多地方没有优化好，后续也会不断又换并且更新

作者：王久一
<!-- START_CANVAS -->
```mermaid
%%{init: {'theme':'neutral', 'flowchart': {'nodeSpacing': 50, 'rankSpacing': 70, 'curve': 'basis', 'htmlLabels': true}}}%%
graph TD
    classDef default fill:#e8e0ff,stroke:#9370db,stroke-width:2px,rx:8px,ry:8px;
    node_0["<a href="https://github.com/wangjiuyi543-ui/Circuit-Foundations-First-Principles/blob/main/Obsidian Vault/电路原理相关证明/00电路分析证明.md" target="_blank" style="color:inherit;text-decoration:none;">00电路分析证明</a>"]
    node_1["<a href="https://github.com/wangjiuyi543-ui/Circuit-Foundations-First-Principles/blob/main/Obsidian Vault/电路原理相关证明/06.0.0_第六章 一阶电路.md" target="_blank" style="color:inherit;text-decoration:none;">06.0.0_第六章 一阶电路<br></a>"]
    node_2["<a href="https://github.com/wangjiuyi543-ui/Circuit-Foundations-First-Principles/blob/main/Obsidian Vault/电路原理相关证明/06.1.0_一阶线性动态系统（电路）响应的底层数学与物理逻辑.md" target="_blank" style="color:inherit;text-decoration:none;">06.1.0_一阶线性动态系统<br>（电路）响应的底层数学与物理逻<br>辑</a>"]
    node_3["<a href="https://github.com/wangjiuyi543-ui/Circuit-Foundations-First-Principles/blob/main/Obsidian Vault/电路原理相关证明/06.2.0_动态电路叠加定理.md" target="_blank" style="color:inherit;text-decoration:none;">06.2.0_动态电路叠加定理<br></a>"]
    node_4["<a href="https://github.com/wangjiuyi543-ui/Circuit-Foundations-First-Principles/blob/main/Obsidian Vault/电路原理相关证明/06.3.0_引入阶跃函数与冲击函数的一些问题证明.md" target="_blank" style="color:inherit;text-decoration:none;">06.3.0_引入阶跃函数与冲<br>击函数的一些问题证明</a>"]
    node_5["<a href="https://github.com/wangjiuyi543-ui/Circuit-Foundations-First-Principles/blob/main/Obsidian Vault/电路原理相关证明/06.3.4_算子与仿射.md" target="_blank" style="color:inherit;text-decoration:none;">06.3.4_算子与仿射</a>"]
    node_6["<a href="https://github.com/wangjiuyi543-ui/Circuit-Foundations-First-Principles/blob/main/Obsidian Vault/电路原理相关证明/06.3.1阶跃函数下电容电压连续性.md" target="_blank" style="color:inherit;text-decoration:none;">06.3.1阶跃函数下电容电压<br>连续性</a>"]
    node_7["<a href="https://github.com/wangjiuyi543-ui/Circuit-Foundations-First-Principles/blob/main/Obsidian Vault/电路原理相关证明/06.3.2_线性时不变(LTI)系统中冲激响应与阶跃响应的微积分关系.md" target="_blank" style="color:inherit;text-decoration:none;">06.3.2_线性时不变(LT<br>I)系统中冲激响应与阶跃响应的<br>微积分关系</a>"]
    node_8["<a href="https://github.com/wangjiuyi543-ui/Circuit-Foundations-First-Principles/blob/main/Obsidian Vault/电路原理相关证明/06.3.3冲激与阶跃响应的微积分关系及工程定义域闭环.md" target="_blank" style="color:inherit;text-decoration:none;">06.3.3冲激与阶跃响应的微<br>积分关系及工程定义域闭环</a>"]
    node_9["<a href="https://github.com/wangjiuyi543-ui/Circuit-Foundations-First-Principles/blob/main/Obsidian Vault/电路原理相关证明/06.3.2.1_补充.md" target="_blank" style="color:inherit;text-decoration:none;">06.3.2.1_补充</a>"]
    node_0 --> node_1
    node_1 --> node_2
    node_1 --> node_3
    node_1 --> node_4
    node_4 --> node_6
    node_4 --> node_7
    node_4 --> node_8
    node_7 --> node_9
    node_1 --> node_5
```
<!-- END_CANVAS -->
