"""冒烟测试：验证 CoT 调用能 mock 通。"""
import sys
from pathlib import Path
from unittest.mock import patch

# 把 00-hello-llm 加入路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "00-hello-llm"))

from py.cot import solve_with_cot


def test_solve_with_cot_returns_text():
    """冒烟测试：mock call_llm，验证 solve_with_cot 能传递 prompt。"""
    with patch("py.cot.call_llm") as mock_call:
        mock_call.return_value = "[CoT] 已知... 推理... 答案: 13"
        result = solve_with_cot("1+1=?")
        assert "13" in result
        mock_call.assert_called_once()
        call_args = mock_call.call_args[0][0]
        assert "一步步思考" in call_args
