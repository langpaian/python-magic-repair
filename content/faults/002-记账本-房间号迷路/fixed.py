expenses = [12, 45, 8, 33]

def total():
    s = 0
    for i in range(len(expenses)):
        s += expenses[i]
    return s

print("本月总开销：", total())
