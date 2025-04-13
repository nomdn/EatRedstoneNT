import os
import sys

from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow,QStackedWidget

import webbrowser
import subprocess

from mainwindow import Ui_MainWindow  # 确保main.py在同一目录下

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 初始化UI
        self.pian_1.clicked.connect(self.on_pian_1_clicked)
        self.shell.clicked.connect(self.on_pian_1_clicked)
        self.start_ffmpeg.clicked.connect(self.on_pian_1_clicked)
        self.dao_time.clicked.connect(self.on_pian_1_clicked)




        # 如果需要，可以在这里连接信号和槽函数
        # 例如，为pushButton连接一个槽函数:
        #self.pushButton.clicked.connect(self.on_pushButton_clicked)

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
        subprocess.Popen(['start', './apps/Python3.8.exe'], shell=True)

    @pyqtSlot()
    def on_pian_1_clicked(self):
        subprocess.Popen(['start', './apps/poem.exe'], shell=True)


    @pyqtSlot()
    def on_start_ffmpeg_clicked(self):
        print("我还没做")
    @pyqtSlot()
    def on_dao_time_clicked(self):
        subprocess.Popen(['start', './apps/countdown.exe'], shell=True)










if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())