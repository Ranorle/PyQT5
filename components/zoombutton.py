import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setGeometry(0, 0, 100, 30)  # 设置按钮的初始位置和大小
        self._animation = QPropertyAnimation(self, b'pos')  # 创建属性动画
        self._animation.setDuration(1000)  # 设置动画持续时间为1秒
        self._animation.setStartValue(self.pos())  # 设置动画的起始位置
        self._animation.setEndValue(self.rect().bottomRight())  # 设置动画的结束位置为父窗口的右下角减去按钮的右下角
        self._animation.setEasingCurve(QEasingCurve.OutBounce)  # 设置动画的缓动曲线为反弹效果