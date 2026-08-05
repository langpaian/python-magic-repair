# 保温咒：给冬天怕冷的客人计算暖宝宝的温度
# 客人说："我要知道，在什么温度下暖宝宝会热过头。"

def heat(temp, room_temp):
    return temp / room_temp

if __name__ == "__main__":
    print("今天气温", 0, "度。")
    print("升温倍率：", heat(60, 0))
