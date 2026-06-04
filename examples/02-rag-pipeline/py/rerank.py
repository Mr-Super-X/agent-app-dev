"""Rerank：用 LLM 对候选 chunks 重排。"""
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def rerank(query: str, candidates: list[str]) -> list[str]:
    """用 LLM 对候选 chunks 重排。返回按相关度从高到低排序的列表。"""
    numbered = "\n".join(f"[{i}] {c[:200]}" for i, c in enumerate(candidates))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"问题：{query}\n\n候选段落：\n{numbered}\n\n按相关度从高到低输出编号，如：3,1,2"
        }],
    )
    order = [int(x) for x in (response.choices[0].message.content or "").split(",")]
    return [candidates[i] for i in order]
