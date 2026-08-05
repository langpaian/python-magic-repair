from solution import new_box

box1 = new_box("娜娜")
box2 = new_box("小奇")
assert box1 == ["娜娜"], "第一个箱子应该只放娜娜"
assert box2 == ["小奇"], "第二个箱子应该是全新的，只放小奇——而不是带着上一个客人的东西"
print("✓ 机器听懂你的意思了。")
