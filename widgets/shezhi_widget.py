import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from widgets.mysql_setting import MySQLConnectionWidget  # Assuming MySQLConnectionWidget is defined in mysql_setting.py
from widgets.car_setting import CarConnectionWidget


class SettingWidget(QWidget):
    database_connection_changed = pyqtSignal(int)
    car_connection_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(10, 30, 10, 10)

        mysql_groupbox = QGroupBox("设置数据库连接")
        mysql_groupbox.setObjectName("Groupboxs")
        mysql_layout = QGridLayout()
        mysql_groupbox.setLayout(mysql_layout)
        mysql_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        mysql_layout.setContentsMargins(10, 10, 10, 10)

        self.mysql_zhuangtai_label = QLabel("数据库连接状态:未连接")
        mysql_layout.addWidget(self.mysql_zhuangtai_label, 0, 0, 1, 2)  

        self.database_button = QPushButton("点击设置数据库连接")
        self.duankai_database_button = QPushButton("断开数据库连接")
        self.database_button.clicked.connect(self.show_mysql_connection_widget)
        self.duankai_database_button.clicked.connect(self.cancel_toggle_database_connection)
        self.duankai_database_button.setEnabled(False)
        mysql_layout.addWidget(self.database_button, 1, 0)  
        mysql_layout.addWidget(self.duankai_database_button, 1, 1)  

        self.mysql_info_label = QLabel()
        self.mysql_info_label.hide()  
        mysql_layout.addWidget(self.mysql_info_label, 2, 0, 1, 2)  

        main_layout.addWidget(mysql_groupbox)

        car_groupbox = QGroupBox("设置小车连接")
        car_groupbox.setObjectName("Groupboxs")
        car_layout = QGridLayout()
        car_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        car_groupbox.setLayout(car_layout)
        self.car_zhuangtai_label = QLabel("小车连接状态:未连接")
        car_layout.addWidget(self.car_zhuangtai_label, 0, 0, 1, 2)

        self.car_button = QPushButton("点击设置小车连接")
        self.car_button.clicked.connect(self.show_car_connection_widget)
        self.duankai_car_button = QPushButton("断开小车连接")
        self.duankai_car_button.setEnabled(False)
        self.duankai_car_button.clicked.connect(self.cancel_toggle_car_connection)
        car_layout.addWidget(self.car_button, 1, 0)
        car_layout.addWidget(self.duankai_car_button, 1, 1)

        self.car_info_label = QLabel()
        self.car_info_label.hide()
        car_layout.addWidget(self.car_info_label, 2, 0, 1, 2)

        main_layout.addWidget(car_groupbox)

    def show_mysql_connection_widget(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("MySQL Connection")
        dialog.resize(500, 400)
        dialog.setLayout(QVBoxLayout())
        self.mysql_widget = MySQLConnectionWidget()
        self.mysql_widget.connection_success.connect(self.handle_mysql_connection_success)
        self.mysql_widget.connection_failure.connect(self.handle_mysql_connection_failure)
        dialog.layout().addWidget(self.mysql_widget)
        dialog.exec_()

    def handle_mysql_connection_success(self):
        ip = self.mysql_widget.ip
        port = self.mysql_widget.port
        database = self.mysql_widget.database
        self.mysql_zhuangtai_label.setText("数据库连接状态:已连接")
        self.mysql_info_label.show()
        self.mysql_info_label.setText(f"mysql数据库IP: {ip}\n端口: {port}\n所连接的数据库: {database}")
        self.database_connection_changed.emit(1)
        self.duankai_database_button.setEnabled(True)
        self.database_button.setEnabled(False)

    def handle_mysql_connection_failure(self, error_message):
        self.mysql_zhuangtai_label.setText("数据库连接状态:未连接")
        self.database_connection_changed.emit(0)
        
    def show_car_connection_widget(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Car Connection")
        dialog.resize(500, 200)
        dialog.setLayout(QVBoxLayout())
        self.car_widget = CarConnectionWidget()
        self.car_widget.connection_success.connect(self.handle_car_connection_success)
        self.car_widget.connection_failure.connect(self.handle_car_connection_failure)
        dialog.layout().addWidget(self.car_widget)
        dialog.exec_()
        
    def handle_car_connection_success(self):
        ip = self.car_widget.ip
        port = self.car_widget.port
        self.car_zhuangtai_label.setText("小车连接状态:已连接")
        self.car_info_label.show()
        self.car_info_label.setText(f"小车IP: {ip}\n端口: {port}")
        self.car_connection_changed.emit(1)
        self.duankai_car_button.setEnabled(True)
        self.car_button.setEnabled(False)

    def handle_car_connection_failure(self, error_message):
        self.car_zhuangtai_label.setText("小车连接状态:未连接")
        self.car_connection_changed.emit(0)
        
    def cancel_toggle_database_connection(self):
        self.database_connection_changed.emit(0)
        self.mysql_zhuangtai_label.setText("数据库连接状态:未连接")
        self.duankai_database_button.setEnabled(False)
        self.database_button.setEnabled(True)
        self.mysql_info_label.clear()
        self.mysql_info_label.hide()
        QMessageBox.information(self, "Connection Status", "成功断开 MySQL 数据库连接")
        
    def cancel_toggle_car_connection(self):
        self.car_connection_changed.emit(0)
        self.car_zhuangtai_label.setText("小车连接状态:未连接")
        self.duankai_car_button.setEnabled(False)
        self.car_button.setEnabled(True)
        car_widget = CarConnectionWidget()
        car_widget.socket.close()
        self.car_info_label.clear()
        self.car_info_label.hide()
        QMessageBox.information(self, "Connection Status", "成功断开小车连接")