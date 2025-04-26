import webbrowser
import time
import random
import traceback



timefor = random.randint(1, 10)
print('''
Python 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:37:02) [MSC v.1924 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.''')
for i in range(timefor):

    a = str(input(">>>"))

    try:
        exec(a)
        time2 = random.randint(1, 3)

        time.sleep(time2)

    except:

        traceback.print_exc()

time.sleep(1)
webbrowser.open("https://www.bilibili.com/video/BV11JsfehEHn/?spm_id_from=333.999.0.0")
