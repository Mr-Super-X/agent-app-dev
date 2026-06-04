"""OpenAI Function Calling 示例：让模型决定调用哪个工具。"""
import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询某地天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名"}
                },
                "required": ["city"]
            }
        }
    }
]


def get_weather(city: str) -> str:
    """模拟天气查询。"""
    return f"{city} 天气：晴，25°C"


def chat_with_tools(user_message: str) -> str:
    """对话流程：模型决定是否调用工具。"""
    messages = [{"role": "user", "content": user_message}]
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, tools=TOOLS
    )
    msg = response.choices[0].message
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            result = get_weather(**args)
            messages.append(msg)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages
        )
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    answer = chat_with_tools("北京今天天气怎么样？")
    print(f"[回复] {answer}")
