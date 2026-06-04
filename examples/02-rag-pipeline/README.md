# 02 · rag-pipeline

对应章节：入门 Ch4 RAG

完整 RAG pipeline：切片 → embedding → 召回 → rerank → 生成。

## 运行

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python py/pipeline.py
```

## 数据

`data/sample.txt` 是一段测试文档（Agent / RAG / Embedding / MCP 概念解释）。

## 测试

```bash
pytest tests/ -v
```
