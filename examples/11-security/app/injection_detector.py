"""Prompt 注入检测：关键词 + 模式匹配。"""
import re

INJECTION_PATTERNS = [
    r"忽略之前(的|所有)指令",
    r"ignore (previous|all) instructions",
    r"你现在是",
    r"you are now",
    r"system\s*prompt",
    r"打印.*prompt",
    r"DAN\s*模式",
    r"developer\s*mode",
]


def is_injection(text: str) -> bool:
    """检测文本是否含注入攻击。"""
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False
