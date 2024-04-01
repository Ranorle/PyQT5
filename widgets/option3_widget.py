# option3_widget.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Option3Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel('This is Option 3 Widget!')
        layout.addWidget(label)
        self.setLayout(layout)
