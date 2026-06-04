"""召回：基于余弦相似度找 top-k。"""
import numpy as np

from embed import embed


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算两个向量的余弦相似度。"""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def retrieve(query: str, chunks: list[str], k: int = 3) -> list[tuple[str, float]]:
    """返回与 query 最相关的 top-k 个 chunk 及相似度。"""
    query_vec = embed(query)
    scored = [(c, cosine_similarity(query_vec, embed(c))) for c in chunks]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
