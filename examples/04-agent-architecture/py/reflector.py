"""反思：检查执行结果是否合理，不合理就重试。"""
import importlib.util
import json
from pathlib import Path

REFLECTOR_PROMPT = """评估下面执行结果是否合理回答了用户目标。

用户目标：{goal}
执行结果：{result}

回答格式（只输出 JSON）：
{{"ok": true/false, "reason": "..."}}"""


def _get_call_llm() -> object:
    """延迟加载：从 00-hello-llm 直接加载 call_llm。"""
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


def reflect(goal: str, result: str) -> tuple[bool, str]:
    """返回 (是否合理, 原因)。"""
    call_llm = _get_call_llm()
    raw = call_llm(REFLECTOR_PROMPT.format(goal=goal, result=result))
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start == -1 or end == 0:
        return True, "无法解析反思结果，假设通过"
    try:
        obj = json.loads(raw[start:end])
        return bool(obj.get("ok", True)), obj.get("reason", "")
    except (ValueError, KeyError):
        return True, "反思结果解析失败，假设通过"
