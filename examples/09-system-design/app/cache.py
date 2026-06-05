"""缓存：内存 LRU + 过期时间。"""
import time
from collections import OrderedDict


class TTLCache:
    """带过期时间的 LRU 缓存。"""

    def __init__(self, max_size: int = 1000, ttl: int = 300):
        self.max_size = max_size
        self.ttl = ttl
        self.cache: OrderedDict = OrderedDict()

    def get(self, key: str):
        """获取缓存值，过期返回 None。"""
        if key not in self.cache:
            return None
        value, expires_at = self.cache[key]
        if time.time() > expires_at:
            del self.cache[key]
            return None
        self.cache.move_to_end(key)
        return value

    def set(self, key: str, value):
        """设置缓存。"""
        self.cache[key] = (value, time.time() + self.ttl)
        self.cache.move_to_end(key)
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
