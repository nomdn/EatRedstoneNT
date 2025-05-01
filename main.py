import os
import sys


from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow,QStackedWidget

import pygame
import os




import subprocess

from mainwindow import Ui_MainWindow  # 确保main.py在同一目录下

from apps import soundplayer
wherepython = sys.executable



class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):

        super().__init__()
        self.setupUi(self)  # 初始化UI
        running = True


        def play(sound):

            pygame.mixer.init()
            if sound =="伴奏神经":
                pygame.mixer.stop()
                wheredir = os.path.dirname(os.path.abspath(__file__))
                music1 = pygame.mixer.Sound(f'{wheredir}/apps/sounds/1.MP3')
                music1.play()
            elif sound =="完整神经":
                pygame.mixer.stop()
                wheredir = os.path.dirname(os.path.abspath(__file__))
                music3 = pygame.mixer.Sound(f'{wheredir}/apps/sounds/3.MP3')
                music3.play()


            elif sound =="纯神经":
                pygame.mixer.stop()
                wheredir = os.path.dirname(os.path.abspath(__file__))
                music2 = pygame.mixer.Sound(f'{wheredir}/apps/sounds/2.MP3')
                music2.play()




        self.pian_1.clicked.connect(self.on_pian_1_clicked)
        self.shell.clicked.connect(self.on_pian_1_clicked)
        self.start_ffmpeg.clicked.connect(self.on_pian_1_clicked)
        self.dao_time.clicked.connect(self.on_pian_1_clicked)
        self.music.currentIndexChanged.connect(lambda index: play(self.music.currentText()))







        # 如果需要，可以在这里连接信号和槽函数
        # 例如，为pushButton连接一个槽函数:
        # self.pushButton.clicked.connect(self.on_pushButton_clicked)

    # 示例槽函数
        self.shell.clicked.disconnect()
    # 然后重新连接
        self.shell.clicked.connect(self.on_shell_clicked)
        self.pian_1.clicked.disconnect()
        # 然后重新连接
        self.pian_1.clicked.connect(self.on_pian_1_clicked)
        self.start_ffmpeg.clicked.disconnect()
        # 然后重新连接
        self.start_ffmpeg.clicked.connect(self.on_start_ffmpeg_clicked)

        self.dao_time.clicked.disconnect()
        # 然后重新连接
        self.dao_time.clicked.connect(self.on_dao_time_clicked)



    @pyqtSlot()
    def on_shell_clicked(self):
        whereshell = os.path.abspath("apps/shell.py")

        subprocess.Popen([wherepython, whereshell], shell=True)
        pass

    @pyqtSlot()
    def on_pian_1_clicked(self):
        wherepoem = os.path.abspath("apps/gushici.py")
        subprocess.Popen([wherepython, wherepoem], shell=True)


    @pyqtSlot()
    def on_start_ffmpeg_clicked(self):
        print("我还没做")
    @pyqtSlot()
    def on_dao_time_clicked(self):
        wheretime = os.path.abspath("apps/倒计时.py")
        subprocess.Popen([wherepython, wheretime], shell=True)












if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())

