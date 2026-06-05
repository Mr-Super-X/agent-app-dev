"""LLM-as-judge：用 LLM 评 LLM 输出。"""
import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

JUDGE_PROMPT = """你是评估员。给下面问答打分（1-5）+ 简短原因。

问题：{question}
参考答案：{reference}
模型回答：{answer}

只输出 JSON：{{"score": 1-5, "reason": "..."}}"""


def judge(question: str, reference: str, answer: str) -> tuple[int, str]:
    """返回 (分数, 原因)。"""
    raw = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": JUDGE_PROMPT.format(
            question=question, reference=reference, answer=answer
        )}]
    ).choices[0].message.content or ""
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start == -1 or end == 0:
        return 3, "无法解析"
    try:
        obj = json.loads(raw[start:end])
        return int(obj.get("score", 3)), obj.get("reason", "")
    except (ValueError, KeyError):
        return 3, "解析失败"
