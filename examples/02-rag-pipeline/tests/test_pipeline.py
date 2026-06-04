"""冒烟测试：mock 掉所有 OpenAI 调用，验证 pipeline 能跑通。"""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# 让 import embed / retrieve / rerank 时能找到
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from py.pipeline import rag_answer


def test_rag_pipeline_runs():
    """冒烟测试：mock 掉所有 OpenAI 调用，验证 pipeline 能跑通。"""
    with patch("py.pipeline.embed") as mock_embed, \
         patch("py.pipeline.retrieve") as mock_retrieve, \
         patch("py.pipeline.rerank") as mock_rerank, \
         patch("py.pipeline.OpenAI") as mock_openai:
        mock_embed.return_value = [0.1] * 1536
        mock_retrieve.return_value = [("ctx", 0.9)]
        mock_rerank.return_value = ["ctx"]
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="RAG 答案"))]
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        result = rag_answer("q", "doc")
        assert result == "RAG 答案"
