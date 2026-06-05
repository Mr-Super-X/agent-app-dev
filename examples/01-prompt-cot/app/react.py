"""ReAct 提示示例：Reasoning + Acting 循环。"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "00-hello-llm"))

from app.main import call_llm

REACT_PROMPT = """你是一个能使用工具的助手。可用工具：
- search(query): 搜索
- calc(expr): 计算

格式：每次先输出 Thought，再输出 Action：
Thought: <你的思考>
Action: <工具名>(<参数>)

或者当有答案时：
Thought: 我知道答案了
Final Answer: <答案>

问题：{question}
{history}
"""


def react_loop(question: str, tools: dict, max_steps: int = 5) -> str:
    """ReAct 循环：每步让模型决定 thought + action。"""
    history = ""
    for _ in range(max_steps):
        prompt = REACT_PROMPT.format(question=question, history=history)
        step = call_llm(prompt)
        history += f"\n{step}\n"
        if "Final Answer:" in step:
            return step.split("Final Answer:")[1].strip()
        # 解析 Action 并执行
        m = re.search(r"Action:\s*(\w+)\(([^)]*)\)", step)
        if m:
            tool_name, arg = m.group(1), m.group(2).strip("'\"")
            if tool_name in tools:
                obs = tools[tool_name](arg)
                history += f"Observation: {obs}\n"
    return "未在限定步数内得到答案"


if __name__ == "__main__":
    tools = {
        "search": lambda q: f"[搜索结果] {q} 的相关信息",
        "calc": lambda expr: str(eval(expr)),
    }
    answer = react_loop("北京到上海的距离除以 2 是多少？", tools)
    print(f"[答案] {answer}")
