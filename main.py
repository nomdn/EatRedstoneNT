import sys
import os
import subprocess
import platform
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
import pygame
from mainwindow import Ui_MainWindow

wherepython = sys.executable


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 初始化UI

        # 初始化pygame混音器
        pygame.init()
        pygame.mixer.init()

        # 连接音乐选择信号
        self.music.currentIndexChanged.connect(self.on_music_changed)

        # 打印当前平台信息
        print(f"当前操作系统: {platform.system()}")

    def on_music_changed(self, index):
        """处理音乐选择变化"""
        sound = self.music.currentText()
        self.play_sound(sound)

    def play_sound(self, sound):
        """播放音效"""
        try:
            pygame.mixer.init()
            wheredir = os.path.dirname(os.path.abspath(__file__))

            if sound == "伴奏神经":
                pygame.mixer.music.stop()
                music_file = f'{wheredir}/apps/sounds/1.MP3'
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play()
            elif sound == "完整神经":
                pygame.mixer.music.stop()
                music_file = f'{wheredir}/apps/sounds/3.MP3'
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play()
            elif sound == "纯神经":
                pygame.mixer.music.stop()
                music_file = f'{wheredir}/apps/sounds/2.MP3'
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play()
        except Exception as e:
            print(f"播放音乐失败: {e}")

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

    def _find_binary_file(self, script_path):
        """在脚本所在目录查找同名二进制文件"""
        try:
            script_dir = os.path.dirname(script_path)
            script_name = os.path.splitext(os.path.basename(script_path))[0]

            # 在不同平台下可能的二进制文件扩展名
            binary_extensions = []
            if platform.system() == "Windows":
                binary_extensions = ['.exe', '.bat', '.cmd', '']
            else:
                binary_extensions = ['', '.bin', '.sh', '.out']

            # 只在脚本所在目录检查是否存在同名二进制文件
            for ext in binary_extensions:
                binary_path = os.path.join(script_dir, script_name + ext)
                if os.path.exists(binary_path) and os.path.isfile(binary_path):
                    # 在Unix系统上检查是否有执行权限
                    if platform.system() != "Windows":
                        if os.access(binary_path, os.X_OK):
                            print(f"找到可执行二进制文件: {binary_path}")
                            return binary_path
                    else:
                        print(f"找到二进制文件: {binary_path}")
                        return binary_path

            print(f"在目录 {script_dir} 中未找到 {script_name} 的二进制文件")
            return None

        except Exception as e:
            print(f"查找二进制文件时出错: {e}")
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
    def _run_macos(self, title, script_abs_path):
        """macOS平台终端运行（备用，当前使用Linux逻辑）"""
        try:
            # 使用AppleScript在Terminal中运行
            cmd_str = f'"{wherepython}" "{script_abs_path}"'
            apple_script = f'''
            tell application "Terminal"
                do script "{cmd_str}; echo \\"按任意键退出...\\"; read -n1"
                activate
            end tell
            '''
            process = subprocess.Popen(['osascript', '-e', apple_script])
            print(f"{title} macOS进程ID: {process.pid}")
            return process
        except Exception as e:
            print(f"macOS启动失败: {e}")
            # 如果AppleScript失败，回退到Linux逻辑
            return self._run_linux(title, script_abs_path)

    @pyqtSlot()
    def on_shell_clicked(self):
        """Shell按钮点击事件"""
        self.run_in_terminal("Shell终端", "apps/shell.py")

    @pyqtSlot()
    def on_lh_run_clicked(self):
        """Lemon Helper按钮点击事件"""
        self.run_in_terminal("Lemon Helper", "apps/lemon_helper/helper_main.py")

    @pyqtSlot()
    def on_deer_pipe_clicked(self):
        """Deer Pipe按钮点击事件"""
        self.run_in_terminal("Deer Pipe", "apps/setu.py")

    @pyqtSlot()
    def on_dao_time_clicked(self):
        """倒计时按钮点击事件"""
        self.run_in_terminal("倒计时", "apps/倒计时.py")

    @pyqtSlot()
    def on_start_ffmpeg_clicked(self):
        """FFmpeg按钮点击事件"""
        print("FFmpeg功能尚未实现")
        # 这里可以添加FFmpeg相关的功能


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())