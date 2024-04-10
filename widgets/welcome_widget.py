import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class WelcomeWidget(QWidget):
    sensor_system_clicked = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        vertical_layout = QVBoxLayout()

        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignCenter | Qt.AlignBottom)

        center_widget.setObjectName("centerWidget")
        self.welcome_label = QLabel('', center_widget)
        self.welcome_label.setObjectName('welcomeLabel')
        font = QFont("华康少女文字W5(P)")
        self.welcome_label.setFont(font)
        center_layout.addWidget(self.welcome_label)

        self.cursor_label = QLabel('|', center_widget)
        self.cursor_label.setObjectName('cursorLabel')
        center_layout.addWidget(self.cursor_label)

        button_layout = QHBoxLayout()
        self.button1 = QPushButton('进入传感器系统')
        self.button2 = QPushButton('进入小车控制系统')
        self.button3 = QPushButton('进入历史数据查询')
        self.button4 = QPushButton('进入设置')
        self.button1.setObjectName('entrybutton')
        self.button2.setObjectName('entrybutton')
        self.button3.setObjectName('entrybutton')
        self.button4.setObjectName('entrybutton')
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        button_layout.addWidget(self.button3)
        button_layout.addWidget(self.button4)

        vertical_layout.addWidget(center_widget)
        vertical_layout.addLayout(button_layout)

        main_layout.addLayout(vertical_layout)
        self.setLayout(main_layout)

        self.button1.clicked.connect(self.enterSensorSystem)
        self.button2.clicked.connect(self.enterCarControlSystem)
        self.button3.clicked.connect(self.enterDataQuery)
        self.button4.clicked.connect(self.enterSettings)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateLabel)
        self.index = 0
        self.texts = ["你好！", "欢迎来到无敌爆龙战神之上位机系统!", "中国农业大学信电学院电子212究级之第13小组", "荣誉巨献。"]
        self.current_text_index = 0
        self.is_deleting = False
        self.is_showing_cursor = False
        self.is_paused = False
        self.typing_speed = 100
        self.last_text_typing_speed = 200
        self.pause_time1 = 2000
        self.pause_time2 = 800
        self.cursor_time = 500
        self.pause_timer = QTimer(self)
        self.pause_timer.timeout.connect(self.resumeTyping)
        self.timer.start(self.typing_speed)

        self.cursor_blink_timer = QTimer(self)
        self.cursor_blink_timer.timeout.connect(self.blinkCursor)
        self.is_cursor_black = True

    def updateLabel(self):
        current_text = self.texts[self.current_text_index]
        if not self.is_deleting:
            if self.index < len(current_text):
                self.welcome_label.setText(current_text[:self.index+1])
                self.index += 1
                self.is_showing_cursor = not self.is_showing_cursor
                self.cursor_label.setVisible(self.is_showing_cursor)
            else:
                self.is_deleting = True
                self.timer.stop()
                self.pause_timer.start(self.pause_time1 if self.current_text_index != len(self.texts) - 1 else self.pause_time2)
                self.cursor_blink_timer.start(500)
        else:
            if self.index >= 0:
                self.welcome_label.setText(current_text[:self.index])
                self.index -= 1
                self.is_showing_cursor = not self.is_showing_cursor
                self.cursor_label.setVisible(self.is_showing_cursor)
            else:
                self.is_deleting = False
                self.timer.stop()
                self.current_text_index = (self.current_text_index + 1) % len(self.texts)
                self.pause_timer.start(self.pause_time2)
                self.cursor_blink_timer.start(500)
                if self.current_text_index == len(self.texts) - 1:
                    self.timer.start(self.last_text_typing_speed)
                else:
                    self.timer.start(self.typing_speed)

    def resumeTyping(self):
        self.is_paused = False
        self.pause_timer.stop()
        self.timer.start()
        self.cursor_label.setStyleSheet("QLabel#cursorLabel { color: black; }")
        self.cursor_blink_timer.start(500)

    def blinkCursor(self):
        if self.is_cursor_black:
            self.cursor_label.setStyleSheet("QLabel#cursorLabel { color: transparent; }")
            self.is_cursor_black = False
        else:
            self.cursor_label.setStyleSheet("QLabel#cursorLabel { color: black; }")
            self.is_cursor_black = True

    def enterSensorSystem(self):
        self.sensor_system_clicked.emit(1)

    def enterCarControlSystem(self):
        self.sensor_system_clicked.emit(2)

    def enterDataQuery(self):
        self.sensor_system_clicked.emit(3)

    def enterSettings(self):
        self.sensor_system_clicked.emit(4)