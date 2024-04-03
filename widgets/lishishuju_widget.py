# option2_widget.py
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class HistoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        welcome_layout = QHBoxLayout(self)
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        center_widget.setObjectName("chuanganqibackground")
        self.welcome_label = QLabel('lishishuju', center_widget)
        self.welcome_label.setObjectName('welcomeLabel')
        center_layout.addWidget(self.welcome_label)
        welcome_layout.addWidget(center_widget)
        self.setLayout(welcome_layout)
