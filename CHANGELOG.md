# Changelog

所有教程章节的变更记录在此。格式参考 [Keep a Changelog](https://keepachangelog.com/)。

## [1.0.0] - 2026-06-04

### Added
- 入门教程 9 章：基础认知 → LLM 基础 → 提示工程 → RAG → 工具调用 → Agent 架构 → Agent 框架 → 场景题 → 开放问题
- 生产进阶 4 章：系统设计 → 评估与优化 → 安全与风险 → 工程实战
- 13 个最小可运行 examples（Python 默认 + TS Web 集成）
- VitePress 1.6.4 双侧栏静态站点
- CI/CD：examples 冒烟测试 + docs 构建 + 站内链接检查
- GitHub Pages deploy workflow（待用户推 main 触发）

## [Unreleased]

### Added
- **AI Agent 工程师招聘笔试卷**（[AI-Agent-Engineer-Exam](/exam/AI-Agent-Engineer-Exam)）：对标 P5 / T5 / 2-1 / L5，120 分钟 / 100 分
  - 双向索引表（考点 ↔ 教程 13 章 + 2024-2026 招聘热点）
  - 选择题 10 道（20 分）+ 填空题 5 道（10 分）+ 简答题 4 道（32 分）+ 编程题 2-3 道（24 分）+ 系统设计题 1 道（14 分）
  - 完整参考答案与详解：含干扰项分析、评分要点、复杂度分析、加分项
  - 覆盖：Agent 4 能力 / RAG 4 环节 / 框架选型 / 工具权限分层 / 限流-缓存-降级-成本 / 注入-越狱-隔离 / 异步-流式 + MCP / A2A / Prompt Caching / Structured Outputs / 推理模型 / Long Context / Agent Observability 等招聘热点
- VitePress 导航新增"考试中心"入口（`docs/.vitepress/config.ts`）
- 教程设计 spec（commit dbfab4c）
- 实施 plan（commit bf87530）
- 项目脚手架（package.json、pyproject.toml、tsconfig.json、首页占位）
- Ch1 基础认知（[01-llm-and-agent](/getting-started/01-basics/01-llm-and-agent)）
- Ch2 LLM 基础（[02-llm-fundamentals](/getting-started/01-basics/02-llm-fundamentals)）
- Ch3 提示工程（[03-prompt-engineering](/getting-started/02-core/03-prompt-engineering)）
- Ch4 RAG（[04-rag](/getting-started/02-core/04-rag)）
- Ch5 工具调用（[05-tool-calling](/getting-started/02-core/05-tool-calling)）
- Ch6 Agent 架构（[06-agent-architecture](/getting-started/02-core/06-agent-architecture)）
- Ch7 Agent 框架横评（[07-frameworks](/getting-started/03-advanced/07-frameworks)）
- Ch8 场景题（[08-scenarios](/getting-started/03-advanced/08-scenarios)）
- Ch9 开放问题（[09-open-questions](/getting-started/03-advanced/09-open-questions)）
- 进阶 Ch0 前置（[00-prerequisites](/production/00-prerequisites)）
- 进阶 Ch1 系统设计（[01-system-design](/production/01-system-design)） + 4 个生产组件 demo（限流/缓存/降级/成本监控，[examples/09-system-design](/examples/09-system-design)）
- 进阶 Ch2 评估与优化（[02-evaluation](/production/02-evaluation)） + Benchmark/judge/反馈环 demo（[examples/10-evaluation](/examples/10-evaluation)）
- 进阶 Ch3 安全与风险（[03-security](/production/03-security)） + 注入/越狱/脱敏 demo（[examples/11-security](/examples/11-security)）
- 进阶 Ch4 工程实战（[04-engineering](/production/04-engineering)） + Python 异步 + TS Vercel AI SDK 集成 demo（[examples/12-engineering-async](/examples/12-engineering-async)）
- examples 13 个：00-hello-llm / 01-prompt-cot / 02-rag-pipeline / 03-tool-calling / 04-agent-architecture / 05-frameworks-compare / 06-customer-service / 07-code-generation / 08-multi-agent / 09-system-design / 10-evaluation / 11-security / 12-engineering-async

### Verified (Task 18 全量核验)
- 入门 9 章 + 进阶 4 章 = **13 章全部发布**，每章带"📌 前置阅读"声明（[验证结果见 commit message](#)）
- VitePress 双侧栏导航：`/`、`/getting-started/`、`/production/` 三段 sidebar 配齐（`docs/.vitepress/config.ts`）
- 进阶 Ch3 含 3 张威胁模型 Mermaid 图（注入/越狱/验证）
- 进阶 Ch4 工程实战：Python 异步 pipeline + TS Vercel AI SDK 流式 UI 双 demo（`examples/12-engineering-async/`）
- 进阶 4 章均带"前置阅读"+"下章"互引指针（00→01→02→03→04→00-roadmap 闭环）
