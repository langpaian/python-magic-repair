from solution import check

assert check("potions") == "还有 3 件", "有的东西能查到数量"
assert check("swords") == "还有 0 件", "没有的东西也应该给个数，而不是爆炸"
print("✓ 机器听懂你的意思了。")
