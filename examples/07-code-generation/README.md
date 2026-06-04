# 07 · code-generation

对应章节：入门 Ch8 场景题-代码生成

代码生成 Agent：用户提需求 → 生成代码 → 沙箱执行 → 失败重试。

## 文件结构

```
07-code-generation/
├── README.md           # 本文件
├── requirements.txt    # 依赖
├── py/
│   ├── __init__.py
│   └── codegen.py      # 代码生成 Agent
└── tests/
    └── test_codegen.py # 冒烟测试
```

## 运行

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python py/codegen.py
```

## 测试

```bash
pytest tests/ -v
```

## 核心能力

- **代码生成**：从 LLM 输出中提取 ```python``` 代码块
- **沙箱执行**：`subprocess.run(timeout=5)` 隔离执行，超时强杀
- **失败重试**：最多 3 次重试，避免模型写死循环
- **静态分析（建议）**：生产环境应加 `bandit` 扫危险 API（`os.system`、`eval`）

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `timeout` | 5 | 沙箱执行超时秒数 |
| `max_retries` | 3 | 失败重试上限 |

## 风险提示

演示版用 `subprocess` 沙箱，仅防死循环。生产环境必须用 Docker / Firecracker 强隔离，否则模型生成的 `os.system(user_input)` 是高危操作。

## 与其他 example 的关系

- 复用 `01-prompt-cot` 的"少样本 prompt"思路
- 沙箱执行是 Ch4 RAG-as-tool 的扩展：把"工具"换成"代码解释器"
