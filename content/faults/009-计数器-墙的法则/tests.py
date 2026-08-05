import solution

assert solution.count_visit() == 1, "第一次来应该记 1"
assert solution.count_visit() == 2, "第二次来应该记 2"
assert solution.visits == 2, "墙外的计数器应该真的变大了"
print("✓ 机器听懂你的意思了。")
