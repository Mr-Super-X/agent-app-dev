"""多 Agent 协作：研究员 / 写作者 / 评审员。

核心设计：
- 3 个 Agent 通过共享 history 列表传递消息（最简版消息总线）
- 评审员说 ok 即退出，否则 max_turns 兜底防止死锁
- 每轮 3 个 Agent 顺序执行：researcher → writer → reviewer
"""
from __future__ import annotations

import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

AGENT_PROMPTS = {
    "researcher": (
        "你是研究员。基于用户提供的主题，给出 3 个关键事实。"
        "只输出事实列表，不要寒暄。"
    ),
    "writer": (
        "你是写作者。基于研究员给出的事实，写一段 200 字左右的短文。"
        "要求结构清晰、语言流畅。"
    ),
    "reviewer": (
        "你是评审员。评审写作者的文章质量。"
        "如果文章合格，回复 'ok' 加简短点评；"
        "如果不合格，列出 1-2 个具体修改点。"
    ),
}

# 评审员认可的终止词
APPROVAL_TOKENS = ("ok", "通过", "approved", "认可")


def _call_agent(role: str, topic: str, history: list[dict]) -> str:
    """调一次 LLM 扮演指定角色。"""
    system = AGENT_PROMPTS[role]
    history_str = "\n".join(
        f"[{m['role']}] {m['content']}" for m in history
    ) or "(空)"
    messages = [
        {"role": "system", "content": system},
        {
            "role": "user",
            "content": f"主题：{topic}\n\n历史对话：\n{history_str}",
        },
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages
    )
    return response.choices[0].message.content or ""


def run_crew(topic: str, max_turns: int = 5) -> str:
    """3 Agent 协作生成文章。

    Args:
        topic: 主题
        max_turns: 最大轮数（防死锁），每轮 3 个 Agent 各跑一次

    Returns:
        最终对话历史（markdown 格式）
    """
    history: list[dict] = []

    for turn in range(max_turns):
        for role in AGENT_PROMPTS:
            content = _call_agent(role, topic, history)
            history.append({"role": role, "content": content})

            # 评审员说 ok 就提前退出
            if role == "reviewer" and _is_approved(content):
                return _format_history(history)

    return f"[max_turns={max_turns} 仍未收敛，共 {len(history)} 条消息]\n" + _format_history(
        history
    )


def _is_approved(review_content: str) -> bool:
    """判断评审员是否认可。"""
    lowered = review_content.lower()
    return any(tok in lowered for tok in APPROVAL_TOKENS)


def _format_history(history: list[dict]) -> str:
    """格式化消息历史为 markdown。"""
    return "\n\n".join(
        f"**[{m['role']}]**\n{m['content']}" for m in history
    )


if __name__ == "__main__":
    topic = input("请输入主题（如：AI 在教育行业的应用）：").strip()
    result = run_crew(topic)
    print("\n" + "=" * 60)
    print(result)
