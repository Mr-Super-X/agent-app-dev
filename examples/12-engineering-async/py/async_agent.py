"""异步 Agent：并发处理多个工具调用。"""
import asyncio
import os

from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])


async def call_llm_async(prompt: str) -> str:
    """异步 LLM 调用。"""
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""


async def run_agents_parallel(prompts: list[str]) -> list[str]:
    """并发跑多个 Agent。"""
    return await asyncio.gather(*[call_llm_async(p) for p in prompts])


if __name__ == "__main__":
    prompts = ["解释 RAG", "解释 Agent", "解释 MCP"]
    results = asyncio.run(run_agents_parallel(prompts))
    for r in results:
        print(f"[回复] {r[:50]}...")
