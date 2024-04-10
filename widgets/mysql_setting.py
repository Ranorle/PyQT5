import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pymysql

class MySQLConnectionWidget(QWidget):
    connection_success = pyqtSignal()
    connection_failure = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MySQL Connection")
        layout = QVBoxLayout()

        # IP Address
        self.ip_label = QLabel("数据库 IP 地址:")
        self.ip_edit = QLineEdit()
        self.ip_edit.setPlaceholderText("默认为127.0.0.1")
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_edit)

        # Port
        self.port_label = QLabel("端口:")
        self.port_edit = QLineEdit()
        self.port_edit.setPlaceholderText("默认为3306")
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_edit)

        # Username
        self.username_label = QLabel("用户名:")
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("默认为root")
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)

        # Password
        self.password_label = QLabel("密码:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)

        # Database
        self.database_label = QLabel("数据库:")
        self.database_edit = QLineEdit()
        layout.addWidget(self.database_label)
        layout.addWidget(self.database_edit)

        # Connect Button
        self.connect_button = QPushButton("连接")
        self.connect_button.clicked.connect(self.connect_to_mysql)
        layout.addWidget(self.connect_button)
        print(self.connection_success)
        self.setLayout(layout)

    def connect_to_mysql(self):
        self.ip = self.ip_edit.text() or "127.0.0.1"
        self.port = self.port_edit.text() or "3306"
        self.username = self.username_edit.text() or "root"
        self.password = self.password_edit.text()
        self.database = self.database_edit.text()

        # Check if any field is empty
        if not self.database:
            QMessageBox.warning(self, "连接失败", "请填写完整的连接信息")
            return

        try:
            # Connect to MySQL database
            connection = pymysql.connect(host=self.ip, port=int(self.port), user=self.username, password=self.password, database=self.database)
            connection.close()  # Close connection
            self.connection_success.emit()  # Emit signal for successful connection
            QMessageBox.information(self, "Connection Status", "成功连接到 MySQL 数据库")
            parent_window = self.window()
            parent_window.close()  # Close the parent window upon successful connection
        except pymysql.Error as e:
            error_message = f"连接失败: {e.args[1]}"
            self.connection_failure.emit(error_message)  # Emit signal for connection failure
            QMessageBox.warning(self, "Connection Status", error_message)
