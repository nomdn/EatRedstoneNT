import turtle as t
import time
import random
import sys

# 我们的turtle必须快
t.delay(0)
t.speed(0)
# 我们的turtle必须看不见
t.hideturtle()
t.penup()
t.goto(0, -150)
t.pendown()
# 我们的turtle必须不受tk颜色的限制
t.colormode(255)
# 我们的tutle必须不需要刷新
t.tracer(False)
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
    # 获取外部参数个数
    value = len(sys.argv)
    # 定义变量
    shi = 0
    fen = int(sys.argv[value - 2])
    miao = int(sys.argv[value - 1])
    # 时间进位
    if miao >= 60:
        # needadd代表的是进位的分
        needadd = miao // 60
        fen += needadd
        # 取余
        miao %= 60
    if fen >= 60:
        # needaddshi代表的是从分进位的时
        needaddshi = fen // 60
        shi += needaddshi
        fen %= 60
    if shi:
        # 如果有小时进位则这样计算循环次数
        steps = 3600 * shi + 60 * fen + miao
    else:
        # 没有时的计算
        steps = 60 * fen + miao

    for i in range(steps):

        # 设置rgb色值
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        bc = random.randint(0, 255)
        t.color(r, g, bc)
        # 时间换算
        if miao == 0:
            fen -= 1
            miao = 60
        miao -= 1
        # w是miao数的字符串化，当秒<10时就朝前面塞个0
        if miao < 10:
            w = f"0{miao}"
        else:
            w = str(miao)

        if fen == 0:
            shi -= 1
            fen = 60
        # fen和miao都是同理
        if fen < 10:
            q = f"0{fen}"
        else:
            q = str(fen)
        # 打印时间
        if shi == 0:
            a = f"{q}:{w}"
        else:
            a = f"{shi}:{q}:{w}"
        time.sleep(1)
        t.write(a, align="center", font=("宋体", 200))

        t.clear()

    t.write("TIME UP", align="center", font=("宋体", 200))



except:
    # 默认操作,看不懂看上面注释
    fen = 2
    miao = 0

    steps = 60 * fen + miao
    for i in range(steps):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        bc = random.randint(0, 255)
        t.color(r, g, bc)

        if miao == 0:
            fen -= 1
            miao += 60
        miao -= 1
        if miao < 10:
            w = f"0{miao}"
        else:
            w = str(miao)
        q = str(fen)

        a = f"{q}:{w}"
        time.sleep(1)

        t.write(a, align="center", font=("宋体", 200))

        t.clear()

    t.write("TIME UP", align="center", font=("宋体", 200))
