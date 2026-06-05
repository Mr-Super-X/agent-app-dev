"""教程 00-hello-llm · 最小 LLM 调用示例。

运行：python py/main.py
环境：需要 OPENAI_API_KEY。
"""
import os

from openai import OpenAI


def call_llm(prompt: str) -> str:
    """调用 LLM 并返回回复文本。"""
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    reply = call_llm("用一句话介绍你自己")
    print(f"[LLM 回复] {reply}")
