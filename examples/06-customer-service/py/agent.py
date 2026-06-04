"""智能客服 Agent：多轮对话 + 工具权限分层。

核心设计：
- SAFE_TOOLS（查询类）自动执行
- DANGEROUS_TOOLS（修改类）必须用户输入'确认'才执行
- history 由调用方持久化，支持多轮对话
"""
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 工具权限分层：自动放行 vs 需确认
SAFE_TOOLS = ["get_order", "search_kb"]
DANGEROUS_TOOLS = ["cancel_order", "refund"]

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "查询订单信息（自动放行）",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}},
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_kb",
            "description": "搜索知识库常见问题（自动放行）",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "取消订单（需用户输入'确认'才执行）",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}},
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "refund",
            "description": "退款（需用户输入'确认'才执行）",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}},
                "required": ["order_id"],
            },
        },
    },
]


def _execute_tool_safely(tool_name: str, arguments: dict) -> str:
    """演示版：实际生产应查数据库 / 调内部 API。"""
    return f"[{tool_name} 模拟结果] arguments={arguments}"


def chat(user_message: str, history: list[dict] | None = None) -> str:
    """客服多轮对话主函数。

    Args:
        user_message: 用户最新消息
        history: 历史消息列表，格式 [{"role": "user|assistant", "content": "..."}]

    Returns:
        Agent 回复内容
    """
    if history is None:
        history = []
    messages = list(history) + [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS,
    )
    msg = response.choices[0].message

    # 无工具调用：直接返回文本
    if not msg.tool_calls:
        return msg.content or ""

    # 有工具调用：按权限分层处理
    for tc in msg.tool_calls:
        if tc.function.name in DANGEROUS_TOOLS:
            return (
                f"⚠️ 检测到高风险操作 {tc.function.name}，"
                f"请用户输入'确认'后再执行"
            )
        # 安全工具：模拟执行并把结果塞回 messages
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tc.id,
                "content": _execute_tool_safely(tc.function.name, tc.function.arguments),
            }
        )

    # 让模型基于工具结果生成最终回复
    final = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    return final.choices[0].message.content or ""


if __name__ == "__main__":
    print("客服 Agent 演示（输入 q 退出）")
    history: list[dict] = []
    while True:
        user_input = input("\n用户: ").strip()
        if user_input.lower() in ("q", "quit", "exit"):
            break
        reply = chat(user_input, history)
        print(f"客服: {reply}")
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": reply})
