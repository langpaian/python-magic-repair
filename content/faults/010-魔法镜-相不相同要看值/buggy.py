# 魔法镜：判断两把钥匙是不是配对的（内容相同）
def same_key(a, b):
    return a is b      # is 问的是"是不是同一个"，不是"值相不相同"

key1 = ["魔法"]
key2 = ["魔法"]
print("配对吗？", same_key(key1, key2))
