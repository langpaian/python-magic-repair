# 订金箱：给每位客人开一个存钱箱
def new_box(owner, coins=[]):     # 经典陷阱：默认值只被创建一次，被所有人共用
    coins.append(owner)
    return coins

print("娜娜的箱子：", new_box("娜娜"))
print("小奇的箱子：", new_box("小奇"))
