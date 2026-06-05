# 13 个最小可运行 Examples

> 本教程的 13 个章节各配 1 个 example 项目。
> 完整代码在仓内 [`examples/`](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples) 目录，本页是导航索引。

## 运行方式

```bash
# 克隆仓
git clone https://github.com/Mr-Super-X/agent-app-dev.git
cd agent-app-dev

# 进入任一 example
cd examples/00-hello-llm
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python py/main.py
```

## 入门教程 examples

| # | 名称 | 章节 | 跑通 | 仓内路径 |
|---|---|---|---|---|
| 00 | hello-llm | [Ch1 基础认知](./getting-started/01-basics/01-llm-and-agent) | ✅ | [examples/00-hello-llm](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/00-hello-llm) |
| 01 | prompt-cot | [Ch3 提示工程](./getting-started/02-core/03-prompt-engineering) | ✅ | [examples/01-prompt-cot](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/01-prompt-cot) |
| 02 | rag-pipeline | [Ch4 RAG](./getting-started/02-core/04-rag) | ✅ | [examples/02-rag-pipeline](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/02-rag-pipeline) |
| 03 | tool-calling | [Ch5 工具调用](./getting-started/02-core/05-tool-calling) | ✅ | [examples/03-tool-calling](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/03-tool-calling) |
| 04 | agent-architecture | [Ch6 Agent 架构](./getting-started/02-core/06-agent-architecture) | ✅ | [examples/04-agent-architecture](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/04-agent-architecture) |
| 05 | frameworks-compare | [Ch7 框架横评](./getting-started/03-advanced/07-frameworks) | 🚧 草稿 | [examples/05-frameworks-compare](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/05-frameworks-compare) |
| 06 | customer-service | [Ch8 场景题-客服](./getting-started/03-advanced/08-scenarios) | ✅ | [examples/06-customer-service](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/06-customer-service) |
| 07 | code-generation | [Ch8 场景题-代码生成](./getting-started/03-advanced/08-scenarios) | ✅ | [examples/07-code-generation](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/07-code-generation) |
| 08 | multi-agent | [Ch8 场景题-多 Agent](./getting-started/03-advanced/08-scenarios) | ✅ | [examples/08-multi-agent](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/08-multi-agent) |

## 生产进阶 examples

| # | 名称 | 章节 | 跑通 | 仓内路径 |
|---|---|---|---|---|
| 09 | system-design | [进阶 Ch1 系统设计](./production/01-system-design) | ✅ | [examples/09-system-design](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/09-system-design) |
| 10 | evaluation | [进阶 Ch2 评估优化](./production/02-evaluation) | ✅ | [examples/10-evaluation](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/10-evaluation) |
| 11 | security | [进阶 Ch3 安全风险](./production/03-security) | ✅ | [examples/11-security](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/11-security) |
| 12 | engineering-async | [进阶 Ch4 工程实战](./production/04-engineering) | ✅ | [examples/12-engineering-async](https://github.com/Mr-Super-X/agent-app-dev/tree/main/examples/12-engineering-async) |

## CI 冒烟测试

```bash
# 跑全部 examples 的 pytest 冒烟测试
pnpm examples:test
```

## 下一步

- 跑通 1-2 个 example 拿到实际体感
- 按章节顺序阅读，遇到 example 链接时**实际跑一次**而非只读代码
- 把 13 个 demo 当作"实验"，每个都加点自己的改动
