"""流式响应：逐 token 输出。"""
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def stream_chat(prompt: str):
    """流式输出 LLM 回复。"""
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        if content:
            yield content


if __name__ == "__main__":
    for token in stream_chat("用 3 句话介绍 RAG"):
        print(token, end="", flush=True)
    print()
