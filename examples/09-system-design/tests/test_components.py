"""冒烟测试：验证 4 个组件能跑通。"""
import time
import pytest

from py.rate_limit import TokenBucket
from py.cache import TTLCache
from py.fallback import FallbackChain
from py.cost_monitor import CostTracker


def test_token_bucket_allows_within_capacity():
    """测试令牌桶：不超过容量时全部通过。"""
    bucket = TokenBucket(capacity=5, refill_rate=1.0)
    for _ in range(5):
        assert bucket.allow() is True
    assert bucket.allow() is False


def test_cache_set_get_with_ttl():
    """测试缓存：set 后能 get，TTL 过期后 get 返回 None。"""
    cache = TTLCache(max_size=10, ttl=1)
    cache.set("key", "value")
    assert cache.get("key") == "value"
    time.sleep(1.1)
    assert cache.get("key") is None


def test_fallback_chain_uses_final():
    """测试降级链：主路径和所有降级都失败时用 final 兜底。"""
    chain = FallbackChain(
        primary=lambda: (_ for _ in ()).throw(RuntimeError("primary")),
        fallbacks=[lambda: (_ for _ in ()).throw(RuntimeError("fb1"))],
        final=lambda: "兜底文案"
    )
    assert chain.execute() == "兜底文案"


def test_cost_tracker_aggregates_by_user():
    """测试成本：按 user_id 聚合正确。"""
    tracker = CostTracker()
    tracker.record("user1", "gpt-4o-mini", 1000, 500)
    tracker.record("user1", "gpt-4o-mini", 2000, 1000)
    tracker.record("user2", "gpt-4o", 500, 250)
    by_user = tracker.by_user()
    assert by_user["user1"] > 0
    assert by_user["user2"] > 0
    assert by_user["user1"] != by_user["user2"]
