# 01 · prompt-cot

对应章节：入门 Ch3 提示工程

三个最小可运行示例：CoT（分步思考）/ ReAct（思考+行动循环）/ 稳定输出（JSON mode）。

## 运行

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...

# CoT
python py/cot.py

# ReAct
python py/react.py

# 稳定输出
python py/stable_output.py
```

## 测试

```bash
pytest tests/ -v
```
