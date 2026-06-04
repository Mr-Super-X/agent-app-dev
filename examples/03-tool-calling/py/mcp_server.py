"""MCP server 示例：用官方 SDK 实现一个简单的 MCP server。

运行：python py/mcp_server.py
依赖：pip install mcp
"""
from mcp.server import Server
from mcp.types import Tool

server = Server("demo-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """声明 server 提供的工具列表。"""
    return [
        Tool(
            name="add",
            description="两数相加",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"},
                },
                "required": ["a", "b"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """实际执行工具调用。"""
    if name == "add":
        return [{"type": "text", "text": str(arguments["a"] + arguments["b"])}]
    raise ValueError(f"Unknown tool: {name}")
