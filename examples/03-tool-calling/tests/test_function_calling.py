"""冒烟测试：mock OpenAI 让模型发起 tool_call。"""
from unittest.mock import patch, MagicMock

from py.function_calling import chat_with_tools


def test_chat_with_tools_invokes_function():
    """冒烟测试：mock 模型返回 tool_call，验证我们执行工具并喂回结果。"""
    mock_msg = MagicMock()
    mock_msg.tool_calls = [MagicMock(
        id="call_1",
        function=MagicMock(name="get_weather", arguments='{"city": "北京"}')
    )]
    mock_msg.content = None

    # 第一次调用（带 tools）返回 tool_call
    mock_response_with_tools = MagicMock()
    mock_response_with_tools.choices = [MagicMock(message=mock_msg)]

    # 第二次调用（喂回结果）返回文本
    mock_final_msg = MagicMock()
    mock_final_msg.tool_calls = None
    mock_final_msg.content = "北京天气晴，25°C"
    mock_response_final = MagicMock()
    mock_response_final.choices = [MagicMock(message=mock_final_msg)]

    with patch("py.function_calling.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = [
            mock_response_with_tools, mock_response_final
        ]
        mock_openai.return_value = mock_client

        result = chat_with_tools("北京天气")
        assert "北京" in result or "25" in result
        assert mock_client.chat.completions.create.call_count == 2
