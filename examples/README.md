# 教程配套 Examples

13 个最小可运行项目，每个对应一个章节。

## 列表

| 编号 | 名称 | 对应章节 | 状态 |
|---|---|---|---|
| 00 | hello-llm | Ch1 基础认知 | ✅ |
| 01 | prompt-cot | Ch3 提示工程 | ⬜ |
| 02 | rag-pipeline | Ch4 RAG | ⬜ |
| 03 | tool-calling | Ch5 工具调用 | ⬜ |
| 04 | agent-architecture | Ch6 Agent 架构 | ⬜ |
| 05 | frameworks-compare | Ch7 Agent 框架 | ⬜ |
| 06 | customer-service | Ch8 场景题-客服 | ⬜ |
| 07 | code-generation | Ch8 场景题-代码生成 | ⬜ |
| 08 | multi-agent | Ch8 场景题-多 Agent | ⬜ |
| 09 | system-design | 进阶 Ch1 系统设计 | ⬜ |
| 10 | evaluation | 进阶 Ch2 评估 | ⬜ |
| 11 | security | 进阶 Ch3 安全 | ⬜ |
| 12 | engineering-async | 进阶 Ch4 工程实战 | ⬜ |

## 运行

```bash
cd examples/00-hello-llm
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python py/main.py
```

## 测试

```bash
cd examples/00-hello-llm
pytest tests/ -v
```

## 冒烟测试（CI 跑）

```bash
pnpm examples:test
```
