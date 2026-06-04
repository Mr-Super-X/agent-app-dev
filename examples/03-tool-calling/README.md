# 03 · tool-calling

对应章节：入门 Ch5 工具调用

两个最小可运行示例：Function Calling（OpenAI 原生）+ MCP Server（Anthropic 协议）。

## 运行

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...

# Function Calling
python py/function_calling.py

# MCP server
python py/mcp_server.py
```

## 测试

```bash
pytest tests/ -v
```
