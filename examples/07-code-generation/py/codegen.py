"""代码生成 Agent：生成 → 沙箱执行 → 失败重试。

核心设计：
- 沙箱用 subprocess + timeout，防止模型写死循环
- 失败重试最多 max_retries 次（默认 3）
- 从 LLM 输出中精确提取 ```python ... ``` 块
"""
from __future__ import annotations

import os
import re
import subprocess

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

CODEGEN_PROMPT = """你是代码生成助手。根据用户需求生成可运行的 Python 代码。

需求：{requirement}

要求：
1. 只输出 Python 代码（用 ```python 包裹）
2. 不要解释、不要加示例
3. 代码必须能直接运行，不要 placeholder
"""

# 匹配 ```python\n...code...\n``` 块（非贪婪，DOTALL 让 . 匹配换行）
PY_BLOCK_RE = re.compile(r"```python\s*\n(.*?)```", re.DOTALL)


def generate_code(requirement: str) -> str:
    """让 LLM 生成代码，提取 ```python``` 块。

    若未找到 python 标记，回退返回原始文本（容错）。
    """
    raw = (
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": CODEGEN_PROMPT.format(requirement=requirement),
                }
            ],
        )
        .choices[0]
        .message.content
        or ""
    )
    match = PY_BLOCK_RE.search(raw)
    return match.group(1).strip() if match else raw.strip()


def run_in_sandbox(code: str, timeout: int = 5) -> tuple[bool, str]:
    """在子进程沙箱跑代码。

    Returns:
        (成功, 输出) 元组
    """
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode == 0, (result.stdout + result.stderr).strip()
    except subprocess.TimeoutExpired:
        return False, f"[沙箱超时] 代码执行超过 {timeout}s"
    except Exception as e:
        return False, f"[沙箱错误] {type(e).__name__}: {e}"


def codegen_with_retry(requirement: str, max_retries: int = 3) -> str:
    """生成 + 执行 + 失败重试。

    返回 markdown 格式的最终结果（成功 / 失败 + 代码 + 输出）。
    """
    last_code = ""
    last_output = ""
    for attempt in range(max_retries):
        # 首次直接生成；后续把上一次错误反馈给模型
        if attempt == 0:
            code = generate_code(requirement)
        else:
            code = _regenerate_with_error(requirement, last_code, last_output)

        last_code = code
        ok, output = run_in_sandbox(code)
        last_output = output

        if ok:
            return (
                f"✅ 代码运行成功（第 {attempt + 1} 次）：\n"
                f"```python\n{code}\n```\n"
                f"输出：\n{output or '(空)'}"
            )

    return (
        f"❌ {max_retries} 次重试仍失败：\n"
        f"```python\n{last_code}\n```\n"
        f"最后错误：\n{last_output}"
    )


def _regenerate_with_error(requirement: str, last_code: str, last_error: str) -> str:
    """把上一次的错误反馈给 LLM，让它重写。"""
    prompt = (
        f"你的上一次代码有错误，请修正：\n\n"
        f"需求：{requirement}\n\n"
        f"你的上一次代码：\n```python\n{last_code}\n```\n\n"
        f"错误：\n{last_error}\n\n"
        f"请重新输出修正后的 Python 代码（用 ```python 包裹）。"
    )
    raw = (
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        .choices[0]
        .message.content
        or ""
    )
    match = PY_BLOCK_RE.search(raw)
    return match.group(1).strip() if match else raw.strip()


if __name__ == "__main__":
    requirement = input("请输入你的需求（如：写个脚本打印 1 到 10）：").strip()
    result = codegen_with_retry(requirement)
    print("\n" + result)
