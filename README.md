# 大模型 Agent 应用开发学习教程

> 体系化教程，从初级开发者到能搭建生产级 Agent。
> 入门 9 章 + 生产进阶 4 章 + 13 个最小可运行 examples。

**🎉 v1.0.0 已发布**

## 📘 入门教程（9 章）

适合初级开发者（含前端），9 章带你从零到能搭出 RAG + 工具调用 Agent。

1. **基础认知** — 大模型应用、Agent、AI 应用三者关系
2. **LLM 基础** — Token、Attention、采样
3. **提示工程** — CoT、ReAct、稳定输出
4. **RAG 检索增强** — Embedding、Chunk、召回、Rerank
5. **工具调用** — Function Calling、MCP、权限与结果反馈
6. **Agent 架构** — 规划-记忆-执行-反思闭环
7. **Agent 框架** — LangChain / LlamaIndex / Agno / Vercel AI SDK 横评
8. **场景题** — 客服 / 代码生成 / 多 Agent 真实业务
9. **开放问题** — Agent 未来、瓶颈、框架评价

## 📗 生产进阶（4 章）

适合中级开发者，4 章深入系统设计、评估优化、安全风险与工程实战。

1. **系统设计** — 高并发、缓存、降级、成本控制
2. **评估与优化** — Benchmark、LLM-as-judge、反馈闭环
3. **安全与风险** — Prompt 注入、越狱、数据隔离
4. **工程实战** — Python 异步、TS Web 集成、流式响应

## 🚀 在线阅读

访问 **https://mr-super-x.github.io/agent-app-dev/**

## 📦 仓库内容

```
agent-app-dev/
├── docs/                # VitePress 教程源（13 章节 + 索引 + 部署文档）
│   ├── getting-started/ # 入门教程 9 章
│   ├── production/      # 生产进阶 4 章
│   ├── examples.md      # 13 examples 索引页
│   └── operations/      # DEPLOY.md / E2E-RUN.md 运维文档
├── examples/            # 13 个最小可运行 Python 项目
│   ├── 00-hello-llm/    # 基础 LLM 调用（DeepSeek 验证跑通）
│   ├── 01-prompt-cot/  # CoT 推理
│   └── ...              # 11 个更多 examples
├── docs/superpowers/    # 设计 spec + 实施 plan（开发过程文档）
├── .github/workflows/   # CI + GitHub Pages deploy
├── package.json
├── pyproject.toml
└── README.md            # 本文件
```

## 🏃 5 分钟跑通

```bash
# 1. 克隆仓
git clone https://github.com/Mr-Super-X/agent-app-dev.git
cd agent-app-dev

# 2. 装 examples 依赖
cd examples/00-hello-llm
pip install -r requirements.txt

# 3. 设 API Key（任选 OpenAI / DeepSeek / 智谱 / 通义）
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.deepseek.com"  # 国产模型
export OPENAI_MODEL="deepseek-chat"

# 4. 跑
python app/main.py
```

跨模型兼容性：OpenAI 兼容 API 都能用（DeepSeek / 智谱 / 通义 / Claude 等）。

## 🎯 适合谁

- 🎓 前端 / 后端想转 Agent 方向的初中级开发者
- 🛠️ 正在用 LangChain / LlamaIndex 想深入原理
- 🚀 准备把 demo Agent 改造为生产 Agent
- 🤔 想系统理解 Agent 未来与瓶颈

## 📐 教程设计原则

| 原则 | 说明 |
|---|---|
| 给"初中生"也能懂 | 每个抽象概念配生活类比 + Mermaid 图 |
| 章节关联性强 | 每章开头"前置阅读"+ 末尾"下章预告 + 关键术语桥接" |
| 螺旋式上升 | 入门三阶段（打地基→核心能力→实战视野） |
| 13 examples | 每章配 1 个最小可运行项目，可独立调试 |
| 跨模型兼容 | OpenAI / 国产模型 0 改动切换 |

## 🤝 贡献

- **发现错别字 / 代码 bug** → 直接 PR
- **想加 1 章新内容** → 先开 issue 讨论
- **跑通 13 example 的真实验证** → 提 PR 更新 `docs/operations/E2E-RUN.md`

## 📜 License

MIT
