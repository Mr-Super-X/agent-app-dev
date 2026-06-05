"""教程 00-hello-llm · 最小 LLM 调用示例。

运行：python py/main.py
环境：
  - OPENAI_API_KEY: 必需
  - OPENAI_BASE_URL: 可选，默认 OpenAI 官方。设成 https://api.deepseek.com 跑国产模型
  - OPENAI_MODEL: 可选，默认 gpt-4o-mini。设成 deepseek-chat 跑 DeepSeek
"""
import os

from openai import OpenAI


def call_llm(prompt: str) -> str:
    """调用 LLM 并返回回复文本。"""
    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ.get("OPENAI_BASE_URL"),  # None = OpenAI 官方
    )
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    reply = call_llm("用一句话介绍你自己")
    print(f"[LLM 回复] {reply}")
