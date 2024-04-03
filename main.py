import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from widgets.welcome_widget import WelcomeWidget
from widgets.chuanganqi_widget import ChuanganqiWidget
from widgets.xiaoche_widget import XiaocheWidget
from widgets.lishishuju_widget import HistoryWidget
from widgets.shezhi_widget import SettingWidget

class wholeScreen(QMainWindow):
    database_connection=0
    car_connection=0

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('无敌爆龙战神小车之上位机系统')
        self.setGeometry(0, 0, 1200, 720)
        
        # 创建一个水平布局
        main_layout = QVBoxLayout()
        
        # 在顶部插入一个区域
        top_area = QWidget()
        top_layout = QHBoxLayout()
        top_area.setLayout(top_layout)
        top_area.setObjectName("topArea")
        # 添加一些空白占位符，以便使区域看起来像是在窗口的顶部
        top_area.setFixedHeight(50)
        top_layout.setSpacing(0)
        top_layout.setContentsMargins(0, 0, 0, 0)
        # 左侧区域
        right_layout = QHBoxLayout()
        left_layout = QHBoxLayout()

        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setFixedWidth(200)  # 固定宽度为 200
        
        # 左侧标签
        left_label = QLabel('第13组｜Version:1.0')
        left_layout.addWidget(left_label)
        left_layout.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        left_label.setObjectName("topLeftWidget")
        top_layout.addWidget(left_widget)
        # 右侧区域
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        right_widget.setObjectName("topRightWidget")
        right_layout.setContentsMargins(0, 0, 0, 0)  # 设置vlayout布局边距为0
        left_layout.setContentsMargins(0, 0, 0, 0)  # 设置vlayout布局边距为0
        right_layout.setSpacing(0)  
        left_layout.setSpacing(0)  
        # 标题
        database_connection_icon_path ="./icon_connect/data1.svg"
        if(self.database_connection==1) :
            database_connection_icon_path="./icon_connect/data1.svg"
        else:
            database_connection_icon_path="./icon_disconnect/data1.svg"
        wifi_connection_icon_path ="./icon_connect/wifi.svg"
        if(self.database_connection==1) :
            wifi_connection_icon_path="./icon_connect/wifi.svg"
        else:
            wifi_connection_icon_path="./icon_disconnect/wifi.svg"
        lianjie_label = QLabel('数据库连接状态:')
        lianjie_label.setAlignment(Qt.AlignCenter)
        lianjie_label.setObjectName("lianjieLabel")
        
        lianjie_label1 = QLabel('小车连接状态:')
        lianjie_label1.setAlignment(Qt.AlignCenter)
        lianjie_label1.setObjectName("lianjieLabel")
        right_layout.addStretch(1)
        right_layout.addWidget(lianjie_label)
        
        database_connection_icon = QLabel()
        pixmap = QPixmap(database_connection_icon_path)
        scaled_pixmap = pixmap.scaled(QSize(20, 20))  # 调整图标大小为 20x20
        database_connection_icon.setPixmap(scaled_pixmap)
        right_layout.addWidget(database_connection_icon)
        
        right_layout.addWidget(lianjie_label1)
        
        wifi_connection_icon = QLabel()
        pixmap = QPixmap(wifi_connection_icon_path)
        scaled_pixmap = pixmap.scaled(QSize(24, 24))  # 调整图标大小为 20x20
        wifi_connection_icon.setPixmap(scaled_pixmap)
        right_layout.addWidget(wifi_connection_icon)
        
        top_layout.addWidget(right_widget)

        # 将顶部区域添加到主布局中
        main_layout.addWidget(top_area)
        main_layout.setSpacing(0)  # 调整hlayout1中按钮间距为0
        main_layout.setContentsMargins(0, 0, 0, 0)  # 设置vlayout布局边距为0

        # 创建左右布局
        layout = QHBoxLayout()
        layout.setSpacing(0)  # 调整hlayout1中按钮间距为0
        layout.setContentsMargins(0, 0, 0, 0)  # 设置vlayout布局边距为0
        
        self.list_widget = QListWidget()
        home_item = QListWidgetItem('首页')
        home_item.setIcon(QIcon('./icons/home.svg'))
        home_item.setFont(QFont('System'))
        self.list_widget.addItem(home_item)

        option2_item = QListWidgetItem('传感器系统')
        option2_item.setIcon(QIcon('./icons/link.svg'))
        option2_item.setFont(QFont('System'))
        self.list_widget.addItem(option2_item)

        option3_item = QListWidgetItem('小车控制系统')
        option3_item.setIcon(QIcon('./icons/database.svg'))
        option3_item.setFont(QFont('System'))
        self.list_widget.addItem(option3_item)
        
        option4_item = QListWidgetItem('历史数据查询')
        option4_item.setIcon(QIcon('./icons/chart-bar.svg'))
        option4_item.setFont(QFont('System'))
        self.list_widget.addItem(option4_item)
        
        option4_item = QListWidgetItem('设置')
        option4_item.setIcon(QIcon('./icons/cog.svg'))
        option4_item.setFont(QFont('System'))
        self.list_widget.addItem(option4_item)
        # 设置默认选中“首页”
        self.list_widget.setCurrentItem(home_item)

        layout.addWidget(self.list_widget)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(WelcomeWidget())  # 添加首页
        self.stacked_widget.addWidget(ChuanganqiWidget())  # 添加传感器系统页面
        self.stacked_widget.addWidget(XiaocheWidget())  # 添加小车控制系统页面
        self.stacked_widget.addWidget(HistoryWidget())  # 添加小车控制系统页面
        self.stacked_widget.addWidget(SettingWidget())  # 添加小车控制系统页面

        layout.addWidget(self.stacked_widget)

        # 将左右布局添加到主布局中
        main_layout.addLayout(layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.list_widget.setFixedWidth(200)
        self.list_widget.setViewportMargins(0, 10, 0, 0)

        self.list_widget.itemClicked.connect(self.onItemSelected)

        # 连接WelcomeWidget的信号
        welcome_widget = self.stacked_widget.widget(0)  # 获取WelcomeWidget实例
        welcome_widget.sensor_system_clicked.connect(self.selectSensorSystemItem)

        styleFile = QFile("./styles/style.qss")
        styleFile.open(QFile.ReadOnly)

        styleSheet = str(styleFile.readAll(), encoding='utf-8')
        self.setStyleSheet(styleSheet)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white"))
        self.setPalette(palette)

    def onItemSelected(self, item):
        index = self.list_widget.row(item)
        self.stacked_widget.setCurrentIndex(index)

    def selectSensorSystemItem(self,value):
        self.list_widget.setCurrentRow(value)  # 选择传感器系统项
        self.stacked_widget.setCurrentIndex(value)  # 切换到传感器系统页面


if __name__ == '__main__':
    app = QApplication(sys.argv)
    welcome_screen = wholeScreen()
    welcome_screen.show()
    sys.exit(app.exec_())
