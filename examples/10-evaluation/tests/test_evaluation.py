"""冒烟测试：3 个评估组件能跑通。"""
from app.benchmark import Benchmark, BenchmarkTask
from app.feedback_loop import FeedbackCollector, Feedback


def test_benchmark_scores_keyword_hits():
    """测试 benchmark 关键词命中评分。"""
    task = BenchmarkTask(
        id="1", question="什么是 RAG？",
        expected_keywords=["检索", "生成"]
    )
    benchmark = Benchmark([task])
    result = benchmark.score(task, "RAG 是检索增强生成")
    assert result.score == 1.0  # 2/2 命中


def test_benchmark_average_aggregation():
    """测试 benchmark 平均分聚合。"""
    tasks = [BenchmarkTask(id=str(i), question=f"q{i}") for i in range(3)]
    benchmark = Benchmark(tasks)
    results = [benchmark.score(t, "a") for t in tasks]
    assert benchmark.average_score(results) == 1.0


def test_feedback_satisfaction_rate():
    """测试反馈满意度计算。"""
    collector = FeedbackCollector()
    collector.add(Feedback("u1", 5))
    collector.add(Feedback("u1", 4))
    collector.add(Feedback("u2", 2))
    assert collector.satisfaction_rate() == 2 / 3


def test_feedback_by_user():
    """测试按用户聚合。"""
    collector = FeedbackCollector()
    collector.add(Feedback("u1", 5))
    collector.add(Feedback("u1", 3))
    collector.add(Feedback("u2", 4))
    by_user = collector.by_user()
    assert by_user["u1"] == [5, 3]
    assert by_user["u2"] == [4]
