# 记账本：学徒小奇这个月买的魔药，要算总账
expenses = [12, 45, 8, 33]

def total():
    s = 0
    for i in range(len(expenses) + 1):   # 咦，这里为什么要 +1？
        s += expenses[i]
    return s

print("本月总开销：", total())
