"""冒烟测试：验证 MCP server 的工具注册和调用。"""
import asyncio
import pytest

from app.mcp_server import list_tools, call_tool


@pytest.mark.asyncio
async def test_list_tools_returns_add():
    """验证 server 注册了 add 工具。"""
    tools = await list_tools()
    assert len(tools) == 1
    assert tools[0].name == "add"


@pytest.mark.asyncio
async def test_call_tool_add():
    """验证 add 工具正确相加。"""
    result = await call_tool("add", {"a": 2, "b": 3})
    assert result == [{"type": "text", "text": "5"}]


@pytest.mark.asyncio
async def test_call_tool_unknown_raises():
    """验证未知工具抛 ValueError。"""
    with pytest.raises(ValueError, match="Unknown tool"):
        await call_tool("unknown", {})
