"""冒烟测试：验证 ReAct 循环能 mock 通。"""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "00-hello-llm"))

from app.react import react_loop


def test_react_loop_returns_final_answer():
    """冒烟测试：mock 让模型直接给 Final Answer。"""
    with patch("app.react.call_llm") as mock_call:
        mock_call.return_value = "Thought: 知道了\nFinal Answer: 42"
        result = react_loop("test", {"search": lambda q: "x"}, max_steps=3)
        assert result == "42"
