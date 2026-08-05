# 宝库清单：查库存
inventory = {"potions": 3, "scrolls": 2}

def check(item):
    return "还有 " + str(inventory[item]) + " 件"

print(check("swords"))
