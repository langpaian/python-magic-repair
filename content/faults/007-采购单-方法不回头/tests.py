from solution import buy, list_now

assert buy("药水") == 3, "买完应该有 3 件"
assert list_now() == "灯笼", "刚加进去的灯笼应该能取到"
print("✓ 机器听懂你的意思了。")
