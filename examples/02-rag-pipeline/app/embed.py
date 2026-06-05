"""Embedding：用 OpenAI 把文本变成向量。"""
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def embed(text: str) -> list[float]:
    """生成单段文本的 embedding。"""
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
