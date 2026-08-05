from solution import heat

# 机器认定的"正确"：正常能算，室温为零时不再爆炸、给出提示
assert heat(60, 20) == 3.0, "正常温度：60 / 20 应该等于 3.0"

result = heat(60, 0)   # 这一行若抛出 ZeroDivisionError，就是还没修好
assert result in ("算不了", None, 0) or "算不了" in str(result), "室温为 0 时不应崩溃，应给出'算不了'的提示"

print("✓ 机器听懂你的意思了。")
