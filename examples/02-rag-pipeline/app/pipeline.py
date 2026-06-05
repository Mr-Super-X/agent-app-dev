"""完整 RAG pipeline：切片 → embedding → 召回 → rerank → 生成。"""
import os
from pathlib import Path

from chunk import chunk_by_paragraph
from embed import embed
from rerank import rerank
from retrieve import retrieve

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def rag_answer(question: str, document: str) -> str:
    """基于文档回答问题。"""
    chunks = chunk_by_paragraph(document)
    top = retrieve(question, chunks, k=5)
    reranked = rerank(question, [c for c, _ in top])
    context = "\n\n".join(reranked[:3])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"参考资料：\n{context}\n\n问题：{question}\n\n基于参考资料回答，不要编造。"
        }],
    )
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parent.parent / "data" / "sample.txt"
    document = data_path.read_text(encoding="utf-8")
    answer = rag_answer("什么是 RAG？", document)
    print(f"[RAG 答案]\n{answer}")
