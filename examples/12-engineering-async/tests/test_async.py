"""冒烟测试：异步组件能跑通（用 mock 不真调 API）。"""
import pytest

from py.async_rag import batch_retrieve
from py.async_agent import run_agents_parallel


@pytest.mark.asyncio
async def test_batch_retrieve_concurrent():
    """测试批量检索并发执行。"""

    async def fake_embed(q: str) -> str:
        return f"fake result for {q}"

    # monkey-patch 替换为 fake
    import py.async_rag
    py.async_rag.embed_and_retrieve = fake_embed

    results = await batch_retrieve(["q1", "q2", "q3"])
    assert len(results) == 3
    assert all("fake" in r for r in results)


@pytest.mark.asyncio
async def test_run_agents_parallel_concurrent():
    """测试并发跑多个 Agent。"""

    async def fake_call(p: str) -> str:
        return f"fake agent reply for {p}"

    import py.async_agent
    py.async_agent.call_llm_async = fake_call

    results = await run_agents_parallel(["p1", "p2"])
    assert len(results) == 2
    assert "p1" in results[0]
    assert "p2" in results[1]


@pytest.mark.asyncio
async def test_empty_input():
    """测试空输入不崩。"""

    async def fake_embed(q: str) -> str:
        return ""

    import py.async_rag
    py.async_rag.embed_and_retrieve = fake_embed

    results = await batch_retrieve([])
    assert results == []
