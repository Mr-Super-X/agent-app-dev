# 10 · evaluation

对应章节：进阶 Ch2 评估与优化

3 个评估组件：Benchmark / LLM-as-judge / 反馈闭环。

## 运行

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python py/benchmark.py
python py/llm_judge.py
python py/feedback_loop.py
```

## 测试

```bash
pytest tests/ -v
```

## 模块说明

| 文件 | 作用 |
|------|------|
| `py/benchmark.py` | 任务集定义 + 关键词命中率评分 + 平均分聚合 |
| `py/llm_judge.py` | GPT-4o-mini 当 judge，给输出打 1-5 分 + 原因 |
| `py/feedback_loop.py` | 反馈采集 + 满意度计算 + 按用户聚合 |
| `tests/test_evaluation.py` | 冒烟测试（不依赖网络） |
