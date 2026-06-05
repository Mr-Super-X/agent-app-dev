"""执行：包装 Function Calling。"""
import importlib.util
from pathlib import Path
from typing import Callable


def _load_get_weather() -> Callable[[str], str]:
    """延迟加载：从 03-tool-calling 直接加载 get_weather（避免 py 包命名冲突 + openai 依赖）。"""
    fc_path = (
        Path(__file__).resolve().parent.parent.parent
        / "03-tool-calling" / "py" / "function_calling.py"
    )
    spec = importlib.util.spec_from_file_location("function_calling", fc_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load function_calling from {fc_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.get_weather


def execute(tool_name: str | None, **kwargs: str) -> str:
    """根据 plan 里的 tool 字段执行。"""
    if tool_name is None:
        return kwargs.get("action", "")
    if tool_name == "get_weather":
        return _load_get_weather()(kwargs.get("city", ""))
    return f"[未知工具] {tool_name}"
