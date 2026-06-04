# 12 · engineering-async

对应章节：进阶 Ch4 工程实战

Python 异步 + TS Web 集成 + 流式响应。

## 文件清单

- `py/async_rag.py` — Python 异步 RAG pipeline（asyncio.gather 并发）
- `py/async_agent.py` — 异步 Agent（AsyncOpenAI + gather）
- `py/streaming.py` — 流式响应（stream=True 逐 token 输出）
- `ts/web_integration.ts` — TS Vercel AI SDK 集成 demo
- `tests/test_async.py` — 冒烟测试（用 mock 不真调 API）

## 运行（Python）

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python py/async_rag.py
python py/async_agent.py
python py/streaming.py
```

## 运行（TS）

```bash
npm install ai @ai-sdk/openai
npx tsx ts/web_integration.ts
```

## 测试

```bash
pytest tests/ -v
```

## 核心能力

1. **Python 异步 pipeline** —— 单进程 QPS 提升 5-10 倍
2. **TS Web 集成** —— Vercel AI SDK + Next.js 一行接上
3. **流式响应** —— 首 token 延迟从 5s 降到 <500ms

## 关键陷阱

- async 协程里调同步 I/O（`requests` / 同步 `OpenAI`）→ 阻塞事件循环
- Vercel AI SDK 用 `generateText` 而非 `streamText` → 丢流式
- 流式 SSE 没设 `max_duration` → 连接挂死
- pytest 不识别 `async def` → 装 `pytest-asyncio`
