from solution import same_key

assert same_key(["魔法"], ["魔法"]) is True, "内容一样的钥匙应该配对"
assert same_key(["火"], ["水"]) is False, "内容不同的钥匙不该配对"
print("✓ 机器听懂你的意思了。")
