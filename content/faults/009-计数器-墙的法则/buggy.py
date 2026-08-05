# 占卜屋的到访计数器
visits = 0

def count_visit():
    visits = visits + 1     # 它以为自己在动墙外的变量
    return visits

print(count_visit())
