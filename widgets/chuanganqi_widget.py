import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebSockets import QWebSocket
from PyQt5.QtNetwork import QAbstractSocket
from pyqtgraph import GraphicsLayoutWidget
from widgets.mysql_setting import MySQLConnectionWidget
from widgets.car_setting import CarConnectionWidget
from widgets.plot import Line_plot
from widgets.shezhi_widget import SettingWidget
import json
import random
import pymysql
import datetime


class ChuanganqiWidget(QWidget):
    duan_licheng_received = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.Duan = ""
        self.Licheng = ""
        self.initUI()
        self.initWebSocket()
        self.load_mysql_info_from_json("mysql_data")
    def initUI(self):
        
        welcome_layout = QHBoxLayout(self)
        center_widget1 = QWidget()
        center_widget = GraphicsLayoutWidget(center_widget1)
        self.line_plot = Line_plot(center_widget)
        self.line_plot.first_on = True
        self.line_plot.start()
        
        
        welcome_layout.setSpacing(10)  
        welcome_layout.setContentsMargins(0, 0, 0, 0)  # 设置vlayout布局边距为0

        center_layout = QHBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        center_widget.setObjectName("chuanganqibackground")
        welcome_layout.addWidget(center_widget)
        center_layout.setContentsMargins(10, 10, 10, 10)  # 设置内边距

        self.temparray = []
        self.humiarray = []
        self.lightarray = []
        self.setting_widget = SettingWidget()  # 创建 SettingWidget 的实例

        button_layout = QVBoxLayout()
        self.clear_button = QPushButton("清空画面")
        self.clear_button.setObjectName("entrybutton")
        self.clear_button.clicked.connect(self.clear_plot)
        button_layout.addWidget(self.clear_button)

        self.stop_button = QPushButton("停止获取与存储数据")
        self.stop_button.setObjectName("entrybutton")
        self.stop_button.clicked.connect(self.stop_data_acquisition)
        button_layout.addWidget(self.stop_button)

        self.start_button = QPushButton("开始获取与存储数据")
        self.start_button.setObjectName("entrybutton")
        self.start_button.clicked.connect(self.start_data_acquisition)
        button_layout.addWidget(self.start_button)
        welcome_layout.addLayout(button_layout)

        # 创建一个 QTimer   
        self.timer = QTimer(self)
        # 连接 QTimer 的 timeout 信号到更新数据的槽函数
        self.timer.timeout.connect(self.update_data_delayed)
        self.timer.start(1000)  # 启动 QTimer，每1000毫秒触发一次
        
        self.mysql_widget = MySQLConnectionWidget()

    def clear_plot(self):
        self.temparray.clear()
        self.humiarray.clear()
        self.lightarray.clear()
        self.line_plot.cur_x = 0
        self.line_plot.data_dict = {"温度(℃)": [], "湿度(%)": [], "光照(Lex)": []}
        self.line_plot.new_data = True
    def initWebSocket(self):
            self.socket = CarConnectionWidget.socket
            self.socket.textMessageReceived.connect(self.process_message)
            
    def load_mysql_info_from_json(self, filename):
        with open(filename, 'r') as f:
            mysql_info = json.load(f)
        self.ip = mysql_info.get("ip")
        self.port = int(mysql_info.get("port"))
        self.username = mysql_info.get("username")
        self.password = mysql_info.get("password")
        self.database = mysql_info.get("database")
        
    def update_data_delayed(self):
        self.load_mysql_info_from_json("mysql_data")
        if self.socket.state() == QAbstractSocket.ConnectedState:
            self.socket.sendTextMessage("1")
        else:
            print("WebSocket is not connected.")
            
    def store_data_to_mysql(self, temperature, humidity, light, timestamp):
        try:
            # 连接到 MySQL 数据库
            conn = pymysql.connect(host=self.ip, port=self.port, user=self.username, password=self.password, database=self.database)
            cursor = conn.cursor()
            print(timestamp)
            # 根据日期动态创建数据表
            table_name = "_" + timestamp.strftime("%Y%m%d%H")
            create_table_query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    temperature FLOAT,
                                    humidity FLOAT,
                                    light FLOAT,
                                    timestamp DATETIME
                                    )"""
            cursor.execute(create_table_query)

            # 插入数据到相应的数据表中
            insert_query = f"INSERT INTO {table_name} (temperature, humidity, light, timestamp) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (temperature, humidity, light, timestamp))

            # 提交事务并关闭连接
            conn.commit()
            cursor.close()
            conn.close()
        except pymysql.Error as e:
            print("Error while storing data to MySQL:", e)
    def stop_data_acquisition(self):
        self.timer.stop()
        self.socket.disconnect()

    def start_data_acquisition(self):
        self.timer.start()
        self.initWebSocket()           
    def process_message(self, message):
        try:
            data = json.loads(message)
            temperature = data.get("temperature")
            humidity = data.get("relative humidity")
            light = data.get("light intensity")
            duan = data.get("duan")
            licheng = data.get("licheng")
            timestamp = datetime.datetime.now()
            if(duan is not None and licheng is not None):
                self.Duan = duan
                self.Licheng = licheng
                self.duan_licheng_received.emit(duan, licheng)
            if temperature is not None and humidity is not None and light is not None :
                self.temparray.append(temperature)
                self.humiarray.append(humidity)
                self.lightarray.append(light)
                
                self.store_data_to_mysql(temperature, humidity, light, timestamp)  # 存储到 MySQL 数据库
                self.line_plot.cur_x = len(self.temparray)
                self.line_plot.data_dict = {"温度(℃)": self.temparray, "湿度(%)": self.humiarray, "光照(Lex)": self.lightarray}
                self.line_plot.new_data = True
        except json.JSONDecodeError:
            print("Failed to parse JSON message:", message)
    def closeEvent(self, event):
        self.line_plot.stop()