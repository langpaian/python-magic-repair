shopping = ["面包", "蜡烛"]

def buy(item):
    shopping.append(item)
    return len(shopping)

def list_now():
    shopping.append("灯笼")
    return shopping[-1]
