import requests
import os
import sys
import json
import base64

username = input("输入你这次的用户名")
print(f"你好！{username}")

def base64_encode(score):
    # 分数格式先改成字符串再改成utf8编码
    score_bytes = str(score).encode('utf-8')
    encoded_score = base64.b64encode(score_bytes)
    return encoded_score.decode('utf-8')

def base64_decode(encoded_score):
    score_bytes = encoded_score.encode('utf-8')
    decoded_score = base64.b64decode(score_bytes)  # 解密同理
    return int(decoded_score.decode('utf-8'))

def update_user_score(user, score):
    # 尝试打开文件，如果文件不存在则创建
    try:
        # 这个文件里的内容谁改谁小狗👇
        with open('user_score.json', 'r') as file:
            # 读取现有的分数数据
            user_score = json.load(file)
    except FileNotFoundError:
        # 文件不存在，创建一个空的分数字典
        user_score = {}

    # 更新或添加用户的分数
    encoded_score = base64_encode(score)
    user_score[user] = encoded_score

    # 将更新后的分数数据写回文件
    with open('user_score.json', 'w') as file:
        json.dump(user_score, file, indent=4)

try:
    with open('user_score.json', 'r') as file:
        # 读取现有的分数数据
        user_scores = json.load(file)
    if username in user_scores:
        last_user_scores = base64_decode(user_scores[username])
        print(f"{username}上次的分数为{last_user_scores}")
    else:
        print(f"{username}没有之前的分数记录,第一次运行？")
except FileNotFoundError:
    # 文件不存在，创建一个空的分数字典
    user_scores = {}

# 下面的内容应该是个人就能看懂
a = (requests.get(f"https://xiaoapi.cn/API/game_gs.php?msg=开始游戏&id={username}")).text
print(a)
right = 0
cuo = 0
for i in range(1, 50):

    answer = input()

    while True:
        try:
            answer = int(answer)
            if answer == 1:
                b = (requests.get(f"https://xiaoapi.cn/API/game_gs.php?msg=答1&id={username}")).text
                right += 1
            elif answer == 2:
                b = (requests.get(f"https://xiaoapi.cn/API/game_gs.php?msg=答2&id={username}")).text
                right += 1
            elif answer == 3:
                b = (requests.get(f"https://xiaoapi.cn/API/game_gs.php?msg=答3&id={username}")).text
                right += 1
            elif answer == 4:
                b = (requests.get(f"https://xiaoapi.cn/API/game_gs.php?msg=答4&id={username}")).text
                right += 1

            if b == "抱歉，答案不对哦！":
                print("抱歉，答案不对哦！")
                cuo += 1
                b = (requests.get(f"https://xiaoapi.cn/API/game_gs.php?msg=开始游戏&id={username}")).text
            break
        except:
            print("好好看看你输入的对吗")
            break
    print(b)

# 示例使用
update_user_score(username, right)

print("来让我看看！")
print("在50道古诗题里")
print("你错了这么多", cuo)
print("你对了这么多", right)
print((requests.get("https://xiaoapi.cn/API/yiyan.php")).text)
print("片就不给你看了( つ•̀ω•́)つ")
os.system("pause")
sys.exit()
