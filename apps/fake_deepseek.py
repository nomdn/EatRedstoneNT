import colorama
import platform
import os
import requests
import json
import random

# === 安全建议：实际使用请用环境变量 ===
# import os
# API_KEY = os.getenv("SUANLI_API_KEY")
# if not API_KEY:
#     print("❌ 请设置环境变量 SUANLI_API_KEY")
#     exit(1)

API_KEY = "sk-WBKcgxq63396eXMFYQYdyraLnAtzcOLEAxBmJb6FABsn5wcF"  # 仅演示用！
url = "https://api.suanli.cn/v1/chat/completions"
HISTORY_FILE="history.json"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 初始化 colorama（支持 Windows/Linux）
colorama.init(autoreset=True)

# 欢迎界面
print(colorama.Fore.LIGHTBLUE_EX + """
╭───────────────────────────────────────────────────────────╮
│  Welcome to DeepSeek/QwQ Assistant                        │
╰───────────────────────────────────────────────────────────╯
""" + colorama.Style.RESET_ALL)

print(colorama.Fore.LIGHTBLUE_EX + """
             █████     ██                                                                                             
    █████████████     █████    ███                                                                                    
  ██████████████████   ███████████                                                                                    
 █████████████████████  ████████           ███                                                               ██       
████████████████████████ ████          ███ ███   █████     █████    ███████     ██████    ██████     █████   ██    ██ 
███       █████████  ███████         █████ ███ ██     ██ ██    ██   ██    ██  ████      ███    ██  ███   ██  ██   ███ 
███          ███████  ██████        ██     ███ ██  █████ ██  █████  ██     ██  ███████  ██  █████  ██ ██████ ██ ███   
████           ████████████          ██    ███ ███   ██  ███   ███  ██    ██        ███ ███   ███  ██    ██  ██  ███  
 ████           ██████████            ████████  ███████   ███████  ███ ████   ████████    ██████    ███████  ██    ███
  █████    ████   ███████                                          ███                                                
    ███████████████████████                                                                                           
       █████████████                                                                                                  
""" + colorama.Style.RESET_ALL)

print("\n📢 Connected to Fake DeepSeek-V3.1(QwQ-32B). Press Enter to start...", end="")
input()

def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")
def history():
    print("全部对话历史:")
    print(messages)
def help_cmd():
    print("\n📌 可用命令:")
    print("  /help    - 显示此帮助")
    print("  /clear   - 清空屏幕")
    print("  /quit    - 退出程序\n")


# 命令映射
command_list = {
    "/help": help_cmd,
    "/clear": clear,
    "/history":history
}

# 对话历史（包含 system prompt）
messages = [
    {"role": "system", "content": "虽然不是DeepSeek，但是你要假装自己是DeepSeek V3.1回答用户问题，并用纯文本输出"}
]

# 主循环
while True:
    try:
        run = random.randint(1,5)


        print(" >", end="", flush=True)
        user_input = input().strip()

        # 忽略空输入
        if not user_input:
            continue

        # 处理内置命令
        if user_input in command_list:
            command_list[user_input]()
            continue
        elif user_input.lower() in ["/quit", "quit", "exit"]:
            print("👋 Goodbye!")
            with open("history.txt", "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            break

        # 添加用户消息
        if run == 1 or run == 5:
            data = {
                "model": "Qwen/QwQ-32B",
                "messages": messages
            }

            # 发送请求
            response = requests.post(url, headers=headers, json=data, timeout=60)

            # 错误处理
            if response.status_code != 200:
                # 移除刚添加的用户消息（避免污染上下文）
                messages.pop()
                continue

            result = response.json()

            # 提取回复内容
            if "choices" in result and len(result["choices"]) > 0:
                reply = result["choices"][0]["message"]["content"]
                print(colorama.Fore.GREEN + "\n🤖 " + reply.strip() + "\n")

                # 保存助手回复到上下文
                messages.append({"role": "assistant", "content": reply})
            else:
                print(colorama.Fore.YELLOW + "服务器繁忙，请稍后再试:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                messages.pop()  # 回滚
        else:
            print("服务器繁忙，请稍后再试。")

    except KeyboardInterrupt:
        print("\n\n👋 Bye!")
        with open("history.txt", "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        break
    except Exception as e:
        print(colorama.Fore.RED + f"服务器繁忙，请稍后再试。: {e}")
        break