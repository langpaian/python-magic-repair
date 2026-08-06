# 7 块魔石分给 2 个学徒
stones = 7
people = 2
each = stones % people     # 应该是 //
left = stones // people    # 应该是 %
print("每人", each, "块，剩", left, "块")
