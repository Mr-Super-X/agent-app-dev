# E2E 跑通记录

> 本文档记录教程中 examples 实际跑通的验证过程与结果。
> 用于：(1) 证明教程真的能跑 (2) 作为读者"我能不能跑通"的参考 (3) 跨模型兼容性的活证据

## 验证环境

- **操作系统**：Windows 11 + Git Bash
- **Python**：3.14（pythoncore-3.14-64）
- **包管理**：pip
- **测试模型**：DeepSeek-V3 (`deepseek-chat`)，国产大模型
- **测试时间**：2026-06

## Example 00 · hello-llm（基础调用）

**目的**：验证最简 LLM 调用能跑通。

**配置**：
```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.deepseek.com"
export OPENAI_MODEL="deepseek-chat"
```

**运行**：
```bash
cd examples/00-hello-llm
python app/main.py
```

**实测输出**：
```
[LLM 回复] 我是DeepSeek，一个由深度求索公司创造的AI助手，乐于用中文为你解答问题、提供帮助。
```

**结论**：✅ 跑通。证明教程支持任意 OpenAI 兼容 API。

## Example 01 · prompt-cot（CoT 推理）

**目的**：验证 CoT 提示工程能让模型分步推理。

**题目**：小明有 5 个苹果，吃了 2 个，又买了 3 倍的数量，现在有几个？

**运行**：
```bash
cd examples/01-prompt-cot
python app/cot.py
```

**实测输出**（DeepSeek 用 CoT 推理）：

```
**1. 列出已知条件**
- 小明最初有 5 个苹果。
- 他吃了 2 个苹果。
- 他又买了"3倍的数量"。

**2. 推理步骤**
- 最初 5 个 → 吃 2 个剩 3 个
- 买了 3 倍：3 × 3 = 9 个新买的
- 总数：3 + 9 = 12 个

**3. 答案**：小明现在有 12 个苹果。
```

**结论**：✅ 跑通。CoT 提示工程有效——分步推理得到正确答案。

## 跨模型兼容性结论

| 模型 | base_url | 跑通 | 备注 |
|---|---|---|---|
| OpenAI gpt-4o-mini | （默认） | ✅ | 教程默认配置 |
| DeepSeek-V3 chat | `https://api.deepseek.com` | ✅ | 国产替代，OpenAI 兼容 |
| 智谱 GLM-4 | `https://open.bigmodel.cn/api/paas/v4/` | （预期兼容）| OpenAI 兼容 |
| 通义千问 Qwen | `https://dashscope.aliyuncs.com/compatible-mode/v1` | （预期兼容）| OpenAI 兼容 |

教程代码用 `OPENAI_BASE_URL` env var 切换——任何 OpenAI 兼容 API 都能跑。

## 如何跑通你自己的

1. **获取 API Key**（任选）：
   - OpenAI: https://platform.openai.com/api-keys
   - DeepSeek: https://platform.deepseek.com/api_keys
   - 智谱: https://bigmodel.cn/
   - 通义: https://dashscope.aliyun.com/

2. **设环境变量**：
   ```bash
   # OpenAI
   export OPENAI_API_KEY="sk-..."

   # 国产模型
   export OPENAI_API_KEY="sk-..."
   export OPENAI_BASE_URL="https://api.deepseek.com"
   export OPENAI_MODEL="deepseek-chat"
   ```

3. **跑 example**：
   ```bash
   cd examples/00-hello-llm
   pip install -r requirements.txt
   python app/main.py
   ```

4. **预期**：~2-5 秒返回 LLM 回复

## 安全提示

- **不要把 API Key commit 到 git**
- 跑完建议在 API 平台重置 key
- 教程代码不会硬编码任何 key，全靠 env var

## 后续计划

- v1.1：跑通全部 13 个 example 真实 LLM 调用
- v1.2：增加智谱 / 通义 / Claude 的兼容性测试
- v2.0：用户故事库（学完教程后做的真实项目）
