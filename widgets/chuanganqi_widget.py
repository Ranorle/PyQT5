# option2_widget.py
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebSockets import QWebSocket
from PyQt5.QtNetwork import QAbstractSocket
from widgets.car_setting import CarConnectionWidget

class ChuanganqiWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initWebSocket()

    def initUI(self):
        welcome_layout = QHBoxLayout(self)
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        center_widget.setObjectName("chuanganqibackground")
        self.welcome_label = QLabel('chuanganqiwidget', center_widget)
        self.welcome_label.setObjectName('welcomeLabel')
        center_layout.addWidget(self.welcome_label)
        welcome_layout.addWidget(center_widget)

        # 添加按钮
        self.send_button = QPushButton("发送消息", self)
        self.send_button.clicked.connect(self.send_message)
        center_layout.addWidget(self.send_button)

        self.setLayout(welcome_layout)

    def initWebSocket(self):
        self.socket = CarConnectionWidget.socket

    def send_message(self):
        if self.socket.state() == QAbstractSocket.ConnectedState:
            message = "Your message here"  # 替换为您要发送的实际消息
            self.socket.sendTextMessage(message)
        else:
            print("WebSocket is not connected.")