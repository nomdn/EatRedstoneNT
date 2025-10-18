import turtle as t
import time
import random
import sys

# 设置turtle
t.delay(0)
t.speed(0)
t.hideturtle()
t.penup()
t.goto(0, -150)
t.pendown()
t.colormode(255)
t.tracer(True)  # 改为True，让turtle自动更新

print('''
使用文档:
在命令行输入该脚本的运行命令，并在后面加入分秒参数，用空格隔开
例子：
python path_the_script_name.py 9 30
./path_the_script_name.exe 9 30
tip:管理员模式下的powershell或者cmd可以去掉./

如果不使用参数，默认倒计时2分钟
''')

try:
    value = len(sys.argv)
    shi = 0
    fen = int(sys.argv[value - 2])
    miao = int(sys.argv[value - 1])

    if miao >= 60:
        needadd = miao // 60
        fen += needadd
        miao %= 60
    if fen >= 60:
        needaddshi = fen // 60
        shi += needaddshi
        fen %= 60

    steps = 3600 * shi + 60 * fen + miao if shi else 60 * fen + miao

    for i in range(steps):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        bc = random.randint(0, 255)
        t.color(r, g, bc)

        # 计算当前时间
        total_seconds = steps - i
        current_shi = total_seconds // 3600
        current_fen = (total_seconds % 3600) // 60
        current_miao = total_seconds % 60

        # 格式化
        miao_str = f"0{current_miao}" if current_miao < 10 else str(current_miao)
        fen_str = f"0{current_fen}" if current_fen < 10 else str(current_fen)

        if current_shi == 0:
            a = f"{fen_str}:{miao_str}"
        else:
            a = f"{current_shi}:{fen_str}:{miao_str}"

        t.clear()
        t.write(a, align="center", font=("宋体", 200))
        t.update()  # 手动更新显示

        time.sleep(1)

    t.write("TIME UP", align="center", font=("宋体", 200))
    t.update()

except:
    # 默认2分钟
    steps = 120
    for i in range(steps):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        bc = random.randint(0, 255)
        t.color(r, g, bc)

        total_seconds = steps - i
        fen = total_seconds // 60
        miao = total_seconds % 60

        miao_str = f"0{miao}" if miao < 10 else str(miao)
        a = f"{fen}:{miao_str}"

        t.clear()
        t.write(a, align="center", font=("宋体", 200))
        t.update()

        time.sleep(1)

    t.clear()
    t.write("TIME UP", align="center", font=("宋体", 200))
    t.update()

# 保持窗口打开
t.mainloop()