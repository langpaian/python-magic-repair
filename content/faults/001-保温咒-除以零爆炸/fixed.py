def heat(temp, room_temp):
    if room_temp == 0:
        return "算不了"
    return temp / room_temp

if __name__ == "__main__":
    print("今天气温", 0, "度。")
    print("升温倍率：", heat(60, 0))
