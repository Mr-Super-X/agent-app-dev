# 11 · security

对应章节：进阶 Ch3 安全与风险

3 个安全组件：注入检测 / 越狱拦截 / 数据脱敏。

## 运行

```bash
pip install -r requirements.txt
python py/injection_detector.py
python py/jailbreak_filter.py
python py/data_sanitizer.py
```

## 测试

```bash
pytest tests/ -v
```
