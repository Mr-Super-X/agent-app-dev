"""Chain of Thought 提示示例：让模型分步推理。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "00-hello-llm"))

from app.main import call_llm

COT_PROMPT = """一步步思考下面问题：
{question}

要求：
1. 先列出已知条件
2. 再列出推理步骤
3. 最后给出答案
"""


def solve_with_cot(question: str) -> str:
    """用 CoT 提示让模型分步回答。"""
    return call_llm(COT_PROMPT.format(question=question))


if __name__ == "__main__":
    q = "小明有 5 个苹果，吃了 2 个，又买了 3 倍的数量，现在有几个？"
    print(solve_with_cot(q))
