"""异步 RAG pipeline：并发检索多个 query。"""
import asyncio
import os

from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])


async def embed_and_retrieve(query: str) -> str:
    """单 query 异步检索（模拟）。"""
    # 实际应调 async embed + 向量库
    response = await client.embeddings.create(
        model="text-embedding-3-small", input=query
    )
    return f"[{query}] → {len(response.data[0].embedding)} 维向量"


async def batch_retrieve(queries: list[str]) -> list[str]:
    """并发检索多个 query。"""
    tasks = [embed_and_retrieve(q) for q in queries]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    queries = ["什么是 RAG？", "什么是 Agent？", "什么是 MCP？"]
    results = asyncio.run(batch_retrieve(queries))
    for r in results:
        print(r)
