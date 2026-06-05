"""成本监控：每请求记录 tokens / 成本。"""
from collections import defaultdict

# 模型单价（每 1K tokens，美元）
MODEL_PRICING = {
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-4o": {"input": 0.0025, "output": 0.01},
}


class CostTracker:
    """成本追踪器：按 user_id / 模型 / 时间维度聚合。"""

    def __init__(self):
        self.records: list[dict] = []

    def record(self, user_id: str, model: str, input_tokens: int, output_tokens: int):
        """记录一次调用。"""
        price = MODEL_PRICING.get(model, {"input": 0, "output": 0})
        cost = (input_tokens / 1000) * price["input"] + (output_tokens / 1000) * price["output"]
        self.records.append({
            "user_id": user_id, "model": model,
            "input_tokens": input_tokens, "output_tokens": output_tokens,
            "cost": cost
        })

    def by_user(self) -> dict[str, float]:
        """按用户聚合成本。"""
        result: dict[str, float] = defaultdict(float)
        for r in self.records:
            result[r["user_id"]] += r["cost"]
        return dict(result)
