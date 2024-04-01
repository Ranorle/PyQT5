import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from widgets.welcome_widget import WelcomeWidget
from widgets.option2_widget import Option2Widget
from widgets.option3_widget import Option3Widget

class wholeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('无敌爆龙战神小车之上位机系统')
        self.setGeometry(0, 0, 1200, 720)

        layout = QHBoxLayout()

        self.list_widget = QListWidget()
        home_item = QListWidgetItem('首页')
        home_item.setIcon(QIcon('./icons/home.svg'))
        home_item.setFont(QFont('System'))
        self.list_widget.addItem(home_item)

        option2_item = QListWidgetItem('传感器系统')
        option2_item.setIcon(QIcon('./icons/home.svg'))
        option2_item.setFont(QFont('System'))
        self.list_widget.addItem(option2_item)

        option3_item = QListWidgetItem('小车控制系统')
        option3_item.setIcon(QIcon('./icons/home.svg'))
        option3_item.setFont(QFont('System'))
        self.list_widget.addItem(option3_item)
        
        option4_item = QListWidgetItem('历史数据查询')
        option4_item.setIcon(QIcon('./icons/database.svg'))
        option4_item.setFont(QFont('System'))
        self.list_widget.addItem(option4_item)
        
        option5_item = QListWidgetItem('设置')
        option5_item.setIcon(QIcon('./icons/home.svg'))
        option5_item.setFont(QFont('System'))
        self.list_widget.addItem(option5_item)       
        # 设置默认选中“首页”
        self.list_widget.setCurrentItem(home_item)

        self.list_widget.itemSelectionChanged.connect(self.onItemSelected)

        self.list_widget.setFixedWidth(200)
        self.list_widget.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.list_widget)

        # 在主窗口中添加新的欢迎部分
        self.welcome_widget = WelcomeWidget()
        layout.addWidget(self.welcome_widget)

        self.setLayout(layout)

        styleFile = QFile("./styles/style.qss")
        styleFile.open(QFile.ReadOnly)

        styleSheet = str(styleFile.readAll(), encoding='utf-8')
        self.setStyleSheet(styleSheet)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("#eee"))
        self.setPalette(palette)

    def onItemSelected(self):
        selected_item = self.list_widget.currentItem()
        if selected_item.text() == '首页':
            welcome_widget = WelcomeWidget()
            self.layout().itemAt(1).widget().deleteLater()
            self.layout().replaceWidget(self.layout().itemAt(1).widget(), welcome_widget)
        elif selected_item.text() == '传感器系统':
            option2_widget = Option2Widget()
            self.layout().itemAt(1).widget().deleteLater()
            self.layout().replaceWidget(self.layout().itemAt(1).widget(), option2_widget)
        elif selected_item.text() == '小车控制系统':
            option3_widget = Option3Widget()
            self.layout().itemAt(1).widget().deleteLater()
            self.layout().replaceWidget(self.layout().itemAt(1).widget(), option3_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome_screen = wholeScreen()
    welcome_screen.show()
    sys.exit(app.exec_())
