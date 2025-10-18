
import platform
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow,QStackedWidget
import webbrowser
import pygame
import os


pygame.init()  # 初始化所有pygame模块，包括mixer
pygame.mixer.init()  # 专门初始化混音器系统:cite[5]





import subprocess

from lemonhelper import Ui_MainWindow  # 确保main.py在同一目录下


wherepython = sys.executable



def play(filename):
    pygame.mixer.init()

    helper_dir = os.path.dirname(os.path.abspath(__file__))
    # 基于 helper_dir 构建到 unimatrix 的路径
    wheresounds = os.path.join(helper_dir, "..", "sounds", f"{filename}")
    wheresounds = os.path.abspath(wheresounds)  # 转换为绝对路径

    print(wheresounds)

    pygame.mixer.music.load(wheresounds)
    pygame.mixer.music.play(loops=-1)  # 音乐将无限循环播放

class MainWindow(QMainWindow, Ui_MainWindow):


    def __init__(self):


        super().__init__()
        self.setupUi(self)  # 初始化UI
        running = True


        self.Color.currentIndexChanged.connect(lambda index: print(self.Color.currentText()))
        self.Font_dict.currentIndexChanged.connect(lambda index: print(self.Font_dict.currentText()))
        # 设置提示文本
        self.Font_dict.setPlaceholderText("选择一个预设文本")

        # 取消选中
        self.Font_dict.setCurrentIndex(-1)

    def run_in_terminal(self, title, script_path, args=None, python_executable=None):
        """跨平台的终端运行方法"""
        try:
            script_abs_path = os.path.abspath(script_path)

            # 检查是否存在同名二进制文件

                # 如果没有指定Python解释器，使用默认的
            if python_executable is None:
                python_executable = wherepython
            script_to_run = script_abs_path

            print(f"启动 {title}...")
            print(f"操作系统: {platform.system()}")
            if python_executable:
                print(f"Python: {python_executable}")
            print(f"运行目标: {script_to_run}")
            print(f"文件存在: {os.path.exists(script_to_run)}")
            if args:
                print(f"命令行参数: {args}")

            if platform.system() == "Windows":
                return self._run_windows(title, script_to_run, args, python_executable)
            else:
                # Linux, macOS, 和其他类Unix系统都使用Linux逻辑
                return self._run_linux(title, script_to_run, args, python_executable)

        except Exception as e:
            print(f"启动 {title} 失败: {e}")
            return None

    def _run_windows(self, title, target_path, args=None, python_executable=None):
        """Windows平台终端运行"""
        try:
            # 构建命令
            if python_executable:
                # 使用Python运行脚本
                command = [python_executable, target_path]
            else:
                # 直接运行二进制文件
                command = [target_path]

            if args:
                if isinstance(args, list):
                    command.extend(args)
                else:
                    command.append(str(args))

            # 方法1: 使用CREATE_NEW_CONSOLE
            process = subprocess.Popen(
                command,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            print(f"{title} Windows进程ID: {process.pid}")
            return process
        except Exception as e:
            print(f"Windows方法1失败: {e}")
            # 备用方法
            try:
                # 构建命令行字符串
                if python_executable:
                    cmd_parts = [f'"{python_executable}"', f'"{target_path}"']
                else:
                    cmd_parts = [f'"{target_path}"']

                if args:
                    if isinstance(args, list):
                        cmd_parts.extend([f'"{arg}"' if ' ' in str(arg) else str(arg) for arg in args])
                    else:
                        cmd_parts.append(f'"{args}"' if ' ' in str(args) else str(args))

                cmd_str = ' '.join(cmd_parts)
                cmd = f'start "{title}" cmd /K {cmd_str}'
                process = subprocess.Popen(cmd, shell=True)
                print(f"{title} Windows备用方法进程ID: {process.pid}")
                return process
            except Exception as e2:
                print(f"Windows备用方法也失败: {e2}")
                return None

    def _run_linux(self, title, target_path, args=None, python_executable=None):
        """Linux及其他平台终端运行"""
        try:
            # 构建命令
            if python_executable:
                cmd_parts = [f'"{python_executable}"', f'"{target_path}"']
            else:
                cmd_parts = [f'"{target_path}"']

            if args:
                if isinstance(args, list):
                    cmd_parts.extend([f'"{arg}"' if ' ' in str(arg) else str(arg) for arg in args])
                else:
                    cmd_parts.append(f'"{args}"' if ' ' in str(args) else str(args))

            cmd_str = ' '.join(cmd_parts)

            # 尝试多种终端模拟器

            # 尝试多种终端模拟器
            terminals = [
                ['gnome-terminal', '--'],
                ['konsole', '-e'],
                ['xterm', '-e'],
                ['terminator', '-e'],
                ['xfce4-terminal', '-x'],
                ['mate-terminal', '-e'],
                ['lxterminal', '-e'],
                ['tilix', '-e'],
                ['deepin-terminal', '-e']

            ]

            # 获取默认终端
            default_terminal = os.environ.get('TERMINAL', 'x-terminal-emulator')
            if default_terminal:
                terminals.insert(0, [default_terminal, '-e'])

            for terminal in terminals:
                try:
                    # 对于gnome-terminal需要使用不同的参数
                    if terminal[0] == 'gnome-terminal':
                        cmd = [
                            'gnome-terminal',
                            '--title', title,
                            '--',
                            'bash', '-c',
                            f'{cmd_str}; echo "按任意键退出..."; read -n1'
                        ]
                    else:
                        cmd = [
                            terminal[0],
                            terminal[1],
                            'bash', '-c',
                            f'{cmd_str}; echo "按任意键退出..."; read -n1'
                        ]

                    print(f"尝试使用终端: {terminal[0]}")
                    process = subprocess.Popen(cmd)
                    print(f"{title} {terminal[0]}进程ID: {process.pid}")
                    return process

                except FileNotFoundError:
                    print(f"终端 {terminal[0]} 未找到，尝试下一个...")
                    continue
                except Exception as e:
                    print(f"终端 {terminal[0]} 启动失败: {e}")
                    continue

            # 如果所有终端都失败，尝试使用os.system
            print("所有终端模拟器都失败，尝试使用os.system...")
            try:
                os.system(f'xterm -title "{title}" -e bash -c "{cmd_str}; echo \\"按任意键退出...\\"; read -n1" &')
                print("使用os.system启动成功")
                return True
            except Exception as e:
                print(f"最终方法也失败: {e}")
                return None

        except Exception as e:
            print(f"Linux平台启动失败: {e}")
            return None
    @pyqtSlot()
    def on_Run_clicked(self):
        # 获取 lemon_helper 脚本所在的目录
        helper_dir = os.path.dirname(os.path.abspath(__file__))
        # 基于 helper_dir 构建到 unimatrix 的路径
        wherematrix = os.path.join(helper_dir, "..", "unimatrix", "unimatrix.py")
        wherematrix = os.path.abspath(wherematrix)  # 转换为绝对路径

        print(f"Matrix路径: {wherematrix}")
        print(f"路径是否存在: {os.path.exists(wherematrix)}")

        enable_music_check = self.Enable_music.isChecked()
        text = self.Fonts.text()
        color = self.Color.currentText()
        font = self.Font_dict.currentText()
        music = self.music.text()
        # 替换为：
        wherematrix = os.path.abspath("../unimatrix/unimatrix.py")
        args = []

        if color:
            args.extend(["-c", color])

        if text:
            if font:
                args.extend(["-l", font])
            else:
                # 移除单引号，直接传递文本
                args.extend(["-u", text])  # 去掉 f"'{text}'"
        elif font:
            args.extend(["-l", font])

        self.run_in_terminal("矩阵终端", wherematrix, args)

        if enable_music_check:
            if music == "佳豪小曲":
                play("jiahao.mp3")
            if music == "Faded":
                play("faded.mp3")

        print(text)
        print(color)
        print(font)

        print(enable_music_check)
        # 创建新控制台窗口，避免重定向问题

    @pyqtSlot()
    def on_Github_clicked(self):
        webbrowser.open("https://github.com/will8211/unimatrix")
















if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())

