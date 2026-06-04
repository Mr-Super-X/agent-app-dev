# 08 · multi-agent

对应章节：入门 Ch8 场景题-多 Agent 协作

3 个 Agent 协作：研究员 / 写作者 / 评审员，共享消息历史，最多 max_turns 轮。

## 文件结构

```
08-multi-agent/
├── README.md           # 本文件
├── requirements.txt    # 依赖
├── py/
│   ├── __init__.py
│   └── crew.py         # 多 Agent 协作主逻辑
└── tests/
    └── test_crew.py    # 冒烟测试
```

## 运行

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python py/crew.py
```

## 测试

```bash
pytest tests/ -v
```

## 核心能力

- **角色分工**：3 个独立 system prompt（研究员 / 写作者 / 评审员）
- **消息总线**：共享 `history` 列表传递消息
- **终止条件**：评审员说 "ok" 即退出，否则 max_turns 兜底
- **死锁防护**：`max_turns=5` 防止 Agent 互相等对方回复导致死锁

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `max_turns` | 5 | 协作最大轮数（防死锁） |
| `AGENT_PROMPTS` | 3 个角色 | researcher / writer / reviewer |

## 与其他 example 的关系

- 是 `04-agent-architecture` 单 Agent 闭环的"多角色扩展"
- 共享消息历史 = 最简版"消息总线"，生产可用 Redis Streams / Kafka
