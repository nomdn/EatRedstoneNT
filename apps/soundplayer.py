from playsound import playsound
import os

def first_sound():
    # 伴奏
    wheredir = os.path.dirname(os.path.abspath(__file__))
    playsound(f"{wheredir}/sounds/1.MP3")

def second_sound():
    # 纯神经
    wheredir = os.path.dirname(os.path.abspath(__file__))
    playsound(f"{wheredir}/sounds/2.MP3")

def third_sound():
    # 原版
    wheredir = os.path.dirname(os.path.abspath(__file__))
    playsound(f"{wheredir}/sounds/3.mp3")
