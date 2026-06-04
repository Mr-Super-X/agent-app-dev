"""冒烟测试：mock LLM 与 subprocess，验证代码生成 Agent 重试逻辑。"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# 让 import 能找到 py 包
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "07-code-generation"))

from py.codegen import (  # noqa: E402
    codegen_with_retry,
    generate_code,
    run_in_sandbox,
)


def test_generate_code_extracts_python_block() -> None:
    """验证从 LLM 输出中精确提取 ```python``` 块，过滤解释文字。"""
    fake_response = MagicMock()
    fake_response.choices = [
        MagicMock(
            message=MagicMock(
                content="看这个：\n```python\nprint(1)\n```\n搞定"
            )
        )
    ]

    with patch("py.codegen.OpenAI") as mock_openai:
        mock_openai.return_value.chat.completions.create.return_value = fake_response
        result = generate_code("test")

    assert "print(1)" in result
    assert "看这个" not in result
    assert "搞定" not in result


def test_generate_code_fallback_when_no_block() -> None:
    """未找到 python 标记时，容错返回原始文本。"""
    fake_response = MagicMock()
    fake_response.choices = [
        MagicMock(message=MagicMock(content="print(2)  # 无代码块标记"))
    ]

    with patch("py.codegen.OpenAI") as mock_openai:
        mock_openai.return_value.chat.completions.create.return_value = fake_response
        result = generate_code("test")

    assert "print(2)" in result


def test_codegen_succeeds_first_try() -> None:
    """验证首次沙箱执行成功时直接返回。"""
    with patch("py.codegen.generate_code") as mock_gen, patch(
        "py.codegen.run_in_sandbox"
    ) as mock_run:
        mock_gen.return_value = "print(1)"
        mock_run.return_value = (True, "1")

        result = codegen_with_retry("test", max_retries=3)

    assert "✅" in result
    assert "第 1 次" in result
    assert "print(1)" in result
    # 成功时不应再调 sandbox
    assert mock_run.call_count == 1


def test_codegen_retries_then_fails() -> None:
    """验证多次沙箱执行失败时返回错误信息。"""
    with patch("py.codegen.generate_code") as mock_gen, patch(
        "py.codegen._regenerate_with_error",
        return_value="print(broken)",
    ), patch("py.codegen.run_in_sandbox") as mock_run:
        mock_gen.return_value = "print(broken)"
        mock_run.return_value = (False, "NameError: name 'broken' is not defined")

        result = codegen_with_retry("test", max_retries=3)

    assert "❌" in result
    assert "3 次重试" in result
    # 验证重试 3 次
    assert mock_run.call_count == 3


def test_run_in_sandbox_timeout() -> None:
    """验证沙箱超时被正确捕获。"""
    import subprocess

    with patch("py.codegen.subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="python", timeout=5)
        ok, output = run_in_sandbox("while True: pass", timeout=5)

    assert ok is False
    assert "超时" in output
