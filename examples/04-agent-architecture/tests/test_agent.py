"""冒烟测试：mock 所有 OpenAI 调用，验证 Agent 闭环能跑通。"""
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "00-hello-llm"))
sys.path.insert(0, str(ROOT / "03-tool-calling"))
sys.path.insert(0, str(ROOT / "04-agent-architecture"))

from app.agent import run_agent


def test_run_agent_succeeds_on_first_try() -> None:
    """冒烟测试：mock 让 planner + reflector 都成功，Agent 一次跑通。"""
    with patch("app.planner._get_call_llm") as mock_plan_factory, \
         patch("app.reflector._get_call_llm") as mock_reflect_factory, \
         patch("app.agent.execute") as mock_exec:
        mock_plan_factory.return_value = lambda _prompt: (
            '[{"step": 1, "action": "查天气", "tool": "get_weather"}]'
        )
        mock_reflect_factory.return_value = lambda _prompt: (
            '{"ok": true, "reason": "ok"}'
        )
        mock_exec.return_value = "北京 天气：晴"

        result = run_agent("北京天气")
        assert "北京" in result


def test_run_agent_retries_on_reflection_failure() -> None:
    """冒烟测试：第 1 次反思失败，第 2 次成功，验证重试逻辑。"""
    with patch("app.planner._get_call_llm") as mock_plan_factory, \
         patch("app.reflector._get_call_llm") as mock_reflect_factory, \
         patch("app.agent.execute") as mock_exec:
        mock_plan_factory.return_value = lambda _prompt: (
            '[{"step": 1, "action": "查天气", "tool": "get_weather"}]'
        )
        # 第一次失败、第二次成功
        responses = iter([
            '{"ok": false, "reason": "信息不全"}',
            '{"ok": true, "reason": "ok"}',
        ])
        mock_reflect_factory.return_value = lambda _prompt: next(responses)
        mock_exec.return_value = "北京 天气：晴"

        result = run_agent("北京天气", max_retries=3)
        assert "北京" in result
        # 验证 _get_call_llm 被调了 2 次
        assert mock_reflect_factory.call_count == 2
