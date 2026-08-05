inventory = {"potions": 3, "scrolls": 2}

def check(item):
    return "还有 " + str(inventory.get(item, 0)) + " 件"
