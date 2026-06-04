"""稳定输出示例：用 JSON mode 强制结构化输出。"""
import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def extract_person(text: str) -> dict:
    """从文本中抽取人物信息，强制返回 JSON。"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一个信息抽取助手。"},
            {"role": "user", "content": f"从下面文本抽取人物姓名和年龄：\n{text}"},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content or "{}")


if __name__ == "__main__":
    text = "小明今年 25 岁，在北京工作。"
    result = extract_person(text)
    print(f"[抽取结果] {result}")
