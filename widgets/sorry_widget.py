# option2_widget.py
import random
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyqtgraph import GraphicsLayoutWidget
import numpy as np

from widgets.plot import Line_plot

class SorryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        welcome_layout = QHBoxLayout(self)
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        center_widget.setObjectName("chuanganqibackground")
        self.welcome_label = QLabel('还未连接至数据库或小车！请前往设置界面。', center_widget)
        self.welcome_label.setObjectName('welcomeLabel')
        center_layout.addWidget(self.welcome_label)
        welcome_layout.addWidget(center_widget)
        self.setLayout(welcome_layout)
        