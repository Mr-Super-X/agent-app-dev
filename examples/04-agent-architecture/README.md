# 04 · agent-architecture

对应章节：入门 Ch6 Agent 架构

完整 Agent 闭环 demo：规划 → 记忆 → 执行 → 反思。

## 文件结构

```
04-agent-architecture/
├── README.md           # 本文件
├── requirements.txt    # 依赖
├── py/
│   ├── planner.py      # 规划（LLM 拆任务）
│   ├── memory.py       # 记忆（短期 deque + 长期 dict）
│   ├── executor.py     # 执行（调工具）
│   ├── reflector.py    # 反思（LLM-as-judge）
│   └── agent.py        # 完整闭环 run_agent()
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

## 4 能力闭环

```
用户目标 → planner 拆任务 → memory 存上下文 → executor 调工具 → reflector 反思 → 终止
                                                                ↺ 反思失败重试
```

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `short_term_size` | 20 | 短期记忆 deque 大小 |
| `max_retries` | 3 | 反思失败最大重试次数 |

## 与其他 example 的关系

- 复用 `00-hello-llm/py/main.py:11` 的 `call_llm` 函数
- 复用 `03-tool-calling/py/function_calling.py:27` 的 `get_weather` 工具
