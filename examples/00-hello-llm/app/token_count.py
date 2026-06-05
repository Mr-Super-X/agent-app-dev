"""教程 00-hello-llm 扩展 · Token 计数示例。

对应章节：入门 Ch2 LLM 基础 § 3 最小可运行示例。

运行：python py/token_count.py
依赖：pip install tiktoken
"""
import tiktoken


def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """用 tiktoken 统计文本的 token 数。

    Args:
        text: 输入文本
        model: 模型名（不同模型 tokenizer 不同，会取对应编码器）

    Returns:
        token 数（整数）
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


if __name__ == "__main__":
    samples = [
        "Agent 是能调用工具、自主决策的 AI",
        "RAG is retrieval-augmented generation",
        "Hello, world!",
    ]
    for s in samples:
        print(f"[{count_tokens(s):2d} tokens] {s}")
