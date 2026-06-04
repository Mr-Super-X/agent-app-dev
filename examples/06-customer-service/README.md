# 06 · customer-service

对应章节：入门 Ch8 场景题-智能客服

多轮对话 + 工具权限分层（高风险操作需用户二次确认）。

## 文件结构

```
06-customer-service/
├── README.md           # 本文件
├── requirements.txt    # 依赖
├── py/
│   ├── __init__.py
│   └── agent.py        # 客服 Agent
└── tests/
    └── test_agent.py   # 冒烟测试
```

## 运行

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python py/agent.py
```

## 测试

```bash
pytest tests/ -v
```

## 核心能力

- **多轮对话**：`history` 参数由调用方维护，模型能记住上文
- **工具权限分层**：`SAFE_TOOLS`（查询类）自动执行；`DANGEROUS_TOOLS`（修改类）需用户二次确认
- **审计日志**：所有工具调用应记录到数据库（生产环境补全）

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `SAFE_TOOLS` | `["get_order", "search_kb"]` | 自动放行的工具 |
| `DANGEROUS_TOOLS` | `["cancel_order", "refund"]` | 需用户确认的工具 |

## 与其他 example 的关系

- 复用 `03-tool-calling` 的 Function Calling 模式
- 复用 `04-agent-architecture` 的 `Memory` 设计（演示版未引入，正式生产应接入）
