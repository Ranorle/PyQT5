# option2_widget.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Option2Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel('This is Option 2 Widget!')
        layout.addWidget(label)
        self.setLayout(layout)
