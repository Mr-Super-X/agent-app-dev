"""数据脱敏：手机号 / 邮箱 / 身份证。"""
import re

PII_PATTERNS = {
    "phone": re.compile(r"1[3-9]\d{9}"),
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "id_card": re.compile(r"\d{17}[\dXx]"),
}


def sanitize(text: str) -> str:
    """脱敏文本中的 PII。"""
    result = text
    for pii_type, pattern in PII_PATTERNS.items():
        result = pattern.sub(f"[{pii_type}_REDACTED]", result)
    return result
