import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebSockets import QWebSocket, QWebSocketProtocol

class CarConnectionWidget(QWidget):
    socket = QWebSocket()
    connection_success = pyqtSignal()
    connection_failure = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("WebSocket 连接")
        layout = QVBoxLayout()

        # IP 地址
        self.ip_label = QLabel("小车 IP 地址:")
        self.ip_edit = QLineEdit()
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_edit)

        # 端口
        self.port_label = QLabel("端口:")
        self.port_edit = QLineEdit()
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_edit)

        # 连接按钮
        self.connect_button = QPushButton("连接")
        self.connect_button.clicked.connect(self.connect_to_websocket)
        layout.addWidget(self.connect_button)

        self.setLayout(layout)

    def display_message(self, status, ip, port):
        if status:
            QMessageBox.information(self, "连接状态", f"成功连接到小车:\nIP: {ip}\n端口: {port}")
            self.connection_success.emit()  # 发射成功连接的信号
            parent_window = self.window()
            parent_window.close()  # 在成功连接时关闭父窗口

    def connect_to_websocket(self):
        self.ip = self.ip_edit.text()
        self.port = self.port_edit.text()

        self.socket.error.connect(self.on_error)
        self.socket.connected.connect(self.on_connected)
        self.socket.disconnected.connect(self.on_disconnected)

        uri = QUrl(f"ws://{self.ip}:{self.port}")
        self.socket.open(uri)

    def on_connected(self):
        ip = self.ip_edit.text()
        port = self.port_edit.text()
        self.display_message(True, ip, port)

    def on_disconnected(self):
        ip = self.ip_edit.text()
        port = self.port_edit.text()
        self.display_message(False, ip, port)

    def on_error(self, error_code):
        QMessageBox.warning(self, "连接错误", f"错误: {error_code}")
