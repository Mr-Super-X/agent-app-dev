"""冒烟测试：mock OpenAI 验证客服 Agent 危险工具拦截。"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# 让 import 能找到 py 包
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "06-customer-service"))

from app.agent import chat  # noqa: E402


def _make_mock_openai(msg: MagicMock) -> MagicMock:
    """构造 patch 后的 OpenAI 客户端。"""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=msg)]
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


def test_dangerous_tool_requires_confirmation() -> None:
    """模型调用 cancel_order 时，应返回确认提示，不执行。"""
    mock_msg = MagicMock()
    mock_msg.content = None
    mock_msg.tool_calls = [
        MagicMock(
            id="call_1",
            function=MagicMock(
                name="cancel_order",
                arguments='{"order_id": "123"}',
            ),
        )
    ]

    with patch("app.agent.OpenAI") as mock_openai:
        mock_openai.return_value = _make_mock_openai(mock_msg)
        result = chat("取消订单 123", [])

    assert "确认" in result or "⚠️" in result
    assert "取消订单 123" in result or "cancel_order" in result


def test_safe_tool_executes_and_returns_text() -> None:
    """模型调用 get_order 时，应执行工具并返回文本回复。"""
    # 第一次调用：模型请求工具
    first_msg = MagicMock()
    first_msg.content = None
    first_msg.tool_calls = [
        MagicMock(
            id="call_1",
            function=MagicMock(
                name="get_order",
                arguments='{"order_id": "123"}',
            ),
        )
    ]
    # 第二次调用：模型基于工具结果生成回复
    second_msg = MagicMock()
    second_msg.content = "您的订单 123 正在运输中"
    second_msg.tool_calls = None

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = [
        MagicMock(choices=[MagicMock(message=first_msg)]),
        MagicMock(choices=[MagicMock(message=second_msg)]),
    ]

    with patch("app.agent.OpenAI") as mock_openai:
        mock_openai.return_value = mock_client
        result = chat("我的订单 123 呢", [])

    assert "运输中" in result
    # 验证调用了 2 次（一次工具选择，一次基于工具结果生成）
    assert mock_client.chat.completions.create.call_count == 2


def test_no_tool_call_returns_direct_text() -> None:
    """模型直接文本回复时（如问候），应原样返回。"""
    mock_msg = MagicMock()
    mock_msg.content = "您好，我是智能客服"
    mock_msg.tool_calls = None

    with patch("app.agent.OpenAI") as mock_openai:
        mock_openai.return_value = _make_mock_openai(mock_msg)
        result = chat("你好", [])

    assert "客服" in result or "您好" in result
