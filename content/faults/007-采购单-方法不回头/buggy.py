# 学徒的采购单
shopping = ["面包", "蜡烛"]

def buy(item):
    shopping.append(item)
    return len(shopping)

def list_now():
    bag = shopping.append("灯笼")   # append 返回 None，不是新列表！
    return bag[-1]                  # 从 None 上取位置 → 爆炸

print(list_now())
