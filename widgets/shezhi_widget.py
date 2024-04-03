# option2_widget.py
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# SettingWidget 类中的修改
class SettingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        welcome_layout = QHBoxLayout(self)
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        center_widget.setObjectName("chuanganqibackground")
        self.welcome_label = QLabel('shezhi', center_widget)
        self.welcome_label.setObjectName('welcomeLabel')
        center_layout.addWidget(self.welcome_label)
        welcome_layout.addWidget(center_widget)
        self.setLayout(welcome_layout)

        # 连接信号与槽
        #parent_screen = self.parent()
        #parent_screen.database_connection_changed.connect(self.onDatabaseConnectionChanged)
        #parent_screen.car_connection_changed.connect(self.onCarConnectionChanged)

    #def onDatabaseConnectionChanged(self, value):
        # 处理数据库连接状态变化
        #print("Database Connection Changed:", value)

    #def onCarConnectionChanged(self, value):
        # 处理小车连接状态变化
        #print("Car Connection Changed:", value)