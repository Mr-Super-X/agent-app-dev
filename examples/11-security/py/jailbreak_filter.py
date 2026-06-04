"""越狱拦截：模式匹配 + 行为标记。"""
import re

JAILBREAK_PATTERNS = [
    r"DAN\s*模式",
    r"无限制模式",
    r"jailbreak",
    r"do anything now",
    r"without (any )?(restrictions|limits)",
    r"bypass (safety|filter)",
    r"扮演.*无道德",
]


def is_jailbreak(text: str) -> bool:
    """检测越狱。"""
    text_lower = text.lower()
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False
