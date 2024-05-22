from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pymysql
import json
import numpy as np
import matplotlib.pyplot as plt

class HistoryWidget(QMainWindow):
    mysql_conn = None
    ip = None
    port = None
    username = None
    password = None
    database = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table Viewer")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.initUI()
        self.load_mysql_info_from_json("mysql_data")
        self.connect_to_mysql()
        self.populate_table_list()
        self.table_widget.setColumnWidth(0, 180)  # 设置第一列宽度为 200 像素
        self.table_list_view.setCurrentRow(0)
        self.display_table_data()  # 默认显示第一个项目的数据

    def initUI(self):
        self.table_list_view = QListWidget()
        self.table_list_view.setFont(QFont("Arial", 12))
        self.table_list_view.clicked.connect(self.display_table_data)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["时间", "温度(℃)", "湿度(%)", "光照(Lex)"])
        self.table_list_view.setFixedWidth(200)  # 固定宽度为 200

        self.plot_button = QPushButton("显示图形")
        self.plot_button.setObjectName("entrybutton")
        self.plot_button.clicked.connect(self.plot_data)

        self.refresh_button = QPushButton("刷新")
        self.refresh_button.setObjectName("entrybutton")
        self.refresh_button.clicked.connect(self.refresh_page)

        left_layout = QVBoxLayout()  # 创建左侧垂直布局
        left_layout.addWidget(self.table_list_view)
        left_layout.addWidget(self.plot_button)
        left_layout.addWidget(self.refresh_button)

        right_layout = QVBoxLayout()  # 创建右侧垂直布局
        right_layout.addWidget(self.table_widget)

        layout = QHBoxLayout()
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.central_widget.setLayout(layout)

    def load_mysql_info_from_json(self, filename):
        with open(filename, 'r') as f:
            mysql_info = json.load(f)
        self.ip = mysql_info.get("ip")
        self.port = int(mysql_info.get("port"))
        self.username = mysql_info.get("username")
        self.password = mysql_info.get("password")
        self.database = mysql_info.get("database")

    def connect_to_mysql(self):
        try:
            self.mysql_conn = pymysql.connect(host=self.ip, port=self.port, user=self.username, password=self.password, database=self.database)
        except pymysql.Error as e:
            print("Error connecting to MySQL:", e)

    def disconnect_from_mysql(self):
        if self.mysql_conn:
            self.mysql_conn.close()

    def fetch_table_names(self):
        table_names = []
        try:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                result = cursor.fetchall()
                for row in result:
                    table_names.append(row[0])
        except pymysql.Error as e:
            print("Error fetching table names:", e)
        return table_names

    def populate_table_list(self):
        self.table_list_view.clear()
        table_names = self.fetch_table_names()
        self.table_list_view.addItems(table_names)

    def fetch_table_data(self, table_name):
        data = []
        try:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(f"SELECT timestamp, humidity, light, temperature FROM {table_name}")
                data = cursor.fetchall()
        except pymysql.Error as e:
            print(f"Error fetching data from table {table_name}:", e)
        return data

    def display_table_data(self):
        table_name = self.table_list_view.currentItem().text()
        data = self.fetch_table_data(table_name)
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)
        if data:
            self.table_widget.setRowCount(len(data))
            for i, row in enumerate(data):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.table_widget.setItem(i, j, item)

    def plot_data(self):
        table_name = self.table_list_view.currentItem().text()
        data = self.fetch_table_data(table_name)
        if data:
            timestamp, temperature, humidity, light = zip(*data)
            plt.plot(timestamp, temperature, label='Temperature')
            plt.plot(timestamp, humidity, label='Humidity')
            plt.plot(timestamp, light, label='Light')
            plt.xlabel('Time')
            plt.ylabel('Value')
            plt.title('Table Data Visualization')
            plt.legend()
            plt.show()

    def refresh_page(self):
        self.disconnect_from_mysql()
        self.connect_to_mysql()
        self.populate_table_list()
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)
        self.table_list_view.setCurrentRow(0)
        self.display_table_data()

    def closeEvent(self, event):
        self.disconnect_from_mysql()
        event.accept()
