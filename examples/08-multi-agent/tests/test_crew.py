"""冒烟测试：mock OpenAI 验证多 Agent 评审员说 ok 后退出。"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# 让 import 能找到 py 包
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "08-multi-agent"))

from app.crew import run_crew  # noqa: E402


def _make_mock_client(per_call_content: list[str]) -> MagicMock:
    """构造按调用顺序返回不同内容的 mock 客户端。"""
    mock_client = MagicMock()
    responses = [
        MagicMock(choices=[MagicMock(message=MagicMock(content=c))])
        for c in per_call_content
    ]
    mock_client.chat.completions.create.side_effect = responses
    return mock_client


def test_crew_exits_when_reviewer_says_ok() -> None:
    """验证评审员说 ok 时，第 1 轮结束后立即退出。"""
    # 顺序：researcher(3 facts) → writer(article) → reviewer(ok)
    per_call = [
        "1. 事实 A\n2. 事实 B\n3. 事实 C",
        "这是一篇关于 AI 的文章……",
        "ok，文章不错，通过",
    ]

    with patch("app.crew.OpenAI") as mock_openai:
        mock_openai.return_value = _make_mock_client(per_call)
        result = run_crew("AI 未来", max_turns=5)

    # 评审员出现且 ok 应在结果中
    assert "[reviewer]" in result
    assert "ok" in result.lower() or "不错" in result
    # 评审员是第 3 个角色，所以总调用 3 次就退出
    assert mock_openai.return_value.chat.completions.create.call_count == 3


def test_crew_exits_when_reviewer_says_approved() -> None:
    """验证评审员说 '通过' / 'approved' 等也能终止。"""
    per_call = [
        "事实列表",
        "文章内容",
        "approved，文章质量合格",
    ]

    with patch("app.crew.OpenAI") as mock_openai:
        mock_openai.return_value = _make_mock_client(per_call)
        result = run_crew("test", max_turns=5)

    assert "approved" in result.lower()


def test_crew_max_turns_fallback() -> None:
    """验证评审员永远不 ok 时，max_turns 兜底退出。"""
    per_call = [
        "事实 A",
        "文章 v1",
        "需要修改：字数太少",  # 第 1 轮 reviewer 不 ok
        "事实 A 补充",
        "文章 v2",
        "需要修改：结构不清",  # 第 2 轮 reviewer 仍不 ok
        "事实 A 再补充",
        "文章 v3",
        "需要修改：举例不足",  # 第 3 轮 reviewer 仍不 ok
        "事实 A 终稿",
        "文章 v4",
        "需要修改：结尾太突兀",  # 第 4 轮 reviewer 仍不 ok
        "事实 A 终极补充",
        "文章 v5",
        "需要修改：标题不够吸引人",  # 第 5 轮（max_turns=5）reviewer 仍不 ok
    ]

    with patch("app.crew.OpenAI") as mock_openai:
        mock_openai.return_value = _make_mock_client(per_call)
        result = run_crew("test", max_turns=5)

    # max_turns=5 时共 5 轮 × 3 角色 = 15 次调用
    assert mock_openai.return_value.chat.completions.create.call_count == 15
    # 结果应包含"未收敛"提示
    assert "未收敛" in result or "max_turns" in result
