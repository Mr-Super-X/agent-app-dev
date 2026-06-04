# 09 · system-design

对应章节：进阶 Ch1 系统设计

4 个生产级组件：限流 / 缓存 / 降级 / 成本监控。

## 运行
```bash
pip install -r requirements.txt
python py/rate_limit.py
python py/cache.py
python py/fallback.py
python py/cost_monitor.py
```

## 测试
```bash
pytest tests/ -v
```
