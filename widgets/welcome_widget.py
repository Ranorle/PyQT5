from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer

class WelcomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        welcome_layout = QHBoxLayout(self)
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignCenter)
        center_widget.setObjectName("centerWidget")
        self.welcome_label = QLabel('', center_widget)
        self.welcome_label.setObjectName('welcomeLabel')
        center_layout.addWidget(self.welcome_label)

        # 添加光标label
        self.cursor_label = QLabel('|', center_widget)
        self.cursor_label.setObjectName('cursorLabel')
        center_layout.addWidget(self.cursor_label)

        welcome_layout.addWidget(center_widget)
        self.setLayout(welcome_layout)

        # 设置打字机效果的定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateLabel)
        self.index = 0
        self.texts = ["你好！", "欢迎来到无敌爆龙战神之上位机系统!", "中国农业大学信电学院电子212究级之第n小组", "荣誉巨献。"]
        self.current_text_index = 0
        self.is_deleting = False
        self.is_showing_cursor = False  # 控制光标显示
        self.is_paused = False  # 控制暂停
        self.typing_speed = 100  # 打字速度（单位：毫秒）
        self.last_text_typing_speed = 200  # 最后一个字符串打字速度（单位：毫秒）
        self.pause_time1 = 2000  # 暂停时间（单位：毫秒）
        self.pause_time2 = 800  # 暂停时间（单位：毫秒）
        self.cursor_time = 500
        self.pause_timer = QTimer(self)
        self.pause_timer.timeout.connect(self.resumeTyping)
        self.timer.start(self.typing_speed)  # 设置定时器间隔为100毫秒

        # 光标闪烁定时器
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
                self.timer.stop()  # 停止打字效果定时器
                self.pause_timer.start(self.pause_time1 if self.current_text_index != len(self.texts) - 1 else self.pause_time2)  # 开始暂停定时器
                self.cursor_blink_timer.start(500)  # 停止光标闪烁定时器
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
                self.pause_timer.start(self.pause_time2)  # 开始暂停定时器
                self.cursor_blink_timer.start(500)  # 停止光标闪烁定时器
                if self.current_text_index == len(self.texts) - 1:  # 如果是最后一个字符串，改变打字速度
                    self.timer.start(self.last_text_typing_speed)
                else:
                    self.timer.start(self.typing_speed)

    def resumeTyping(self):
        self.is_paused = False
        self.pause_timer.stop()
        self.timer.start()  # 重新启动打字效果定时器
        self.cursor_label.setStyleSheet("QLabel#cursorLabel { color: black; }")  # 设置光标颜色为黑色
        self.cursor_blink_timer.start(500)  # 开始光标闪烁定时器

    def blinkCursor(self):
        if self.is_cursor_black:
            self.cursor_label.setStyleSheet("QLabel#cursorLabel { color: transparent; }")  # 设置光标颜色为透明
            self.is_cursor_black = False
        else:
            self.cursor_label.setStyleSheet("QLabel#cursorLabel { color: black; }")  # 设置光标颜色为黑色
            self.is_cursor_black = True
