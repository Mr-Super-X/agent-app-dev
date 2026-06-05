"""反馈闭环：采集 → 聚合 → 触发升级。"""
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class Feedback:
    """用户反馈。"""
    user_id: str
    rating: int  # 1-5 或 👍/👎 映射
    comment: str = ""
    session_id: str = ""


class FeedbackCollector:
    """反馈采集器。"""

    def __init__(self):
        self.feedbacks: list[Feedback] = []

    def add(self, fb: Feedback) -> None:
        """记录一条反馈。"""
        self.feedbacks.append(fb)

    def satisfaction_rate(self) -> float:
        """满意度（rating >= 4 占比）。"""
        if not self.feedbacks:
            return 0.0
        good = sum(1 for fb in self.feedbacks if fb.rating >= 4)
        return good / len(self.feedbacks)

    def by_user(self) -> dict[str, list[int]]:
        """按用户聚合评分。"""
        result: dict[str, list[int]] = defaultdict(list)
        for fb in self.feedbacks:
            result[fb.user_id].append(fb.rating)
        return dict(result)
