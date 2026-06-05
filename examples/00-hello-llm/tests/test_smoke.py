"""冒烟测试：验证 LLM 调用可成功发起（mock 网络层）。"""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# 把 py/ 父目录加到 sys.path，使 `from app.main import call_llm` 可解析
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import call_llm


def test_call_llm_returns_text():
    """冒烟测试：mock OpenAI client，验证函数能解析回复。"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="你好"))]

    with patch("app.main.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        result = call_llm("hi")
        assert result == "你好"
