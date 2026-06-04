"""完整 Agent：规划 → 记忆 → 执行 → 反思 闭环。"""
import sys
from pathlib import Path

# 让 import 能找到同仓其他 examples
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "00-hello-llm"))
sys.path.insert(0, str(ROOT / "03-tool-calling"))
sys.path.insert(0, str(ROOT / "04-agent-architecture"))

from py.executor import execute
from py.memory import Memory
from py.planner import plan
from py.reflector import reflect


def run_agent(goal: str, max_retries: int = 3) -> str:
    """跑 Agent 直到反思通过或达最大重试次数。"""
    memory = Memory()
    memory.add_turn("user", goal)
    steps = plan(goal)
    for attempt in range(max_retries):
        for step in steps:
            result = execute(step.get("tool"), action=step.get("action", ""))
            memory.add_turn("assistant", f"Step {step['step']}: {result}")
        final = "\n".join(t["content"] for t in memory.short_term if t["role"] == "assistant")
        ok, reason = reflect(goal, final)
        if ok:
            return final
        memory.add_turn("system", f"反思失败（{reason}），重试 {attempt + 1}/{max_retries}")
    return f"[重试 {max_retries} 次仍失败] 请人工确认"


if __name__ == "__main__":
    answer = run_agent("查北京天气并告诉用户")
    print(f"[Agent 回复]\n{answer}")
