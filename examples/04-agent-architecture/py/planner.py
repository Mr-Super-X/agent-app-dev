"""规划：用 LLM 把目标拆成步骤。"""
import importlib.util
import json
from pathlib import Path

PLANNER_PROMPT = """把下面目标拆成 3-5 个可执行步骤。每步用 JSON 格式：
{{"step": 1, "action": "...", "tool": "工具名或 null"}}

目标：{goal}

只输出 JSON 列表。"""


def _get_call_llm() -> object:
    """延迟加载：从 00-hello-llm 直接加载 call_llm（避免 py 包命名冲突 + openai 依赖）。"""
    main_path = (
        Path(__file__).resolve().parent.parent.parent
        / "00-hello-llm" / "py" / "main.py"
    )
    spec = importlib.util.spec_from_file_location("main", main_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load main from {main_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.call_llm


def plan(goal: str) -> list[dict]:
    """把目标拆成步骤列表。"""
    call_llm = _get_call_llm()
    raw = call_llm(PLANNER_PROMPT.format(goal=goal))
    start = raw.find("[")
    end = raw.rfind("]") + 1
    if start == -1 or end == 0:
        return [{"step": 1, "action": goal, "tool": None}]
    return json.loads(raw[start:end])
