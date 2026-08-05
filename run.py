"""魔法维修铺 —— 本地启动入口。

   一条命令开铺：  python run.py
   然后浏览器访问 http://127.0.0.1:8000
"""
import uvicorn

if __name__ == "__main__":
    print("✨  魔法维修铺正在开门……")
    print("    修好后，机器会为你点亮一盏灯。")
    print("    →  http://127.0.0.1:8000\n")
    uvicorn.run("web.app:app", host="127.0.0.1", port=8000, reload=False)
