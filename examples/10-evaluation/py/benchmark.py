"""Benchmark：任务集 + 评分函数。"""
from dataclasses import dataclass, field


@dataclass
class BenchmarkTask:
    """单个 benchmark 任务。"""
    id: str
    question: str
    expected_keywords: list[str] = field(default_factory=list)
    expected_answer: str = ""


@dataclass
class BenchmarkResult:
    """单次评估结果。"""
    task_id: str
    actual: str
    score: float  # 0-1


class Benchmark:
    """Benchmark 评估器。"""

    def __init__(self, tasks: list[BenchmarkTask]):
        self.tasks = tasks

    def score(self, task: BenchmarkTask, actual: str) -> BenchmarkResult:
        """评分：关键词命中率。"""
        if not task.expected_keywords:
            return BenchmarkResult(task.id, actual, 1.0)
        hits = sum(1 for kw in task.expected_keywords if kw in actual)
        return BenchmarkResult(task.id, actual, hits / len(task.expected_keywords))

    def average_score(self, results: list[BenchmarkResult]) -> float:
        """聚合平均分。"""
        if not results:
            return 0.0
        return sum(r.score for r in results) / len(results)
