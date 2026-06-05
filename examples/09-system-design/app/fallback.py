"""降级：主路径失败时降级到规则 / 缓存 / 兜底文案。"""
from typing import Callable


class FallbackChain:
    """多级降级链。"""

    def __init__(self, primary: Callable, fallbacks: list[Callable], final: Callable):
        self.primary = primary
        self.fallbacks = fallbacks
        self.final = final

    def execute(self, *args, **kwargs):
        """按主路径 → 降级 → 兜底 顺序执行。"""
        try:
            return self.primary(*args, **kwargs)
        except Exception:
            for fb in self.fallbacks:
                try:
                    return fb(*args, **kwargs)
                except Exception:
                    continue
            return self.final(*args, **kwargs)
