"""记忆：短期（deque）+ 长期（dict）。"""
from collections import deque
from typing import Any


class Memory:
    """Agent 记忆：短期对话 + 长期偏好。"""

    def __init__(self, short_term_size: int = 20) -> None:
        self.short_term: deque = deque(maxlen=short_term_size)
        self.long_term: dict[str, Any] = {}

    def add_turn(self, role: str, content: str) -> None:
        """记录一轮对话到短期记忆。"""
        self.short_term.append({"role": role, "content": content})

    def set_preference(self, key: str, value: Any) -> None:
        """设置长期偏好。"""
        self.long_term[key] = value

    def get_context(self) -> str:
        """生成给 LLM 的上下文（含短期 + 长期）。"""
        turns = "\n".join(f"[{t['role']}] {t['content']}" for t in self.short_term)
        prefs = "\n".join(f"- {k}: {v}" for k, v in self.long_term.items())
        return f"## 对话历史\n{turns}\n\n## 用户偏好\n{prefs}"
