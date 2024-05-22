import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from widgets.chuanganqi_widget import ChuanganqiWidget

class XiaocheWidget(QWidget):
    
    def handle_duan_licheng(self, duan, licheng):
        # self.move_ball_to_position(duan, licheng)
        # self.coord_label.setText(f"new Position: ({duan}, {licheng})")
        # 在这里处理duan和licheng的数据
        self.bili=10
        if duan == '1':
            self.move_ball_to_position((0-float(licheng))*self.bili,0)
            self.rotation_angle = 0
        elif duan == '2':
            self.rotation_angle = 90
            self.move_ball_to_position(-30*self.bili,(0-float(licheng))*self.bili)
        elif duan == '3':
            self.rotation_angle = -90
            self.move_ball_to_position(-30*self.bili,(-5+float(licheng))*self.bili)
        elif duan == '4':
            self.rotation_angle = 180
            self.move_ball_to_position((-30+float(licheng))*self.bili,0)
            
    def __init__(self):
        super().__init__()
        self.angle = 0  # 初始角度为0
        self.rotation_angle = 0  # 初始旋转角度为0
        self.chuanganqi_widget = ChuanganqiWidget()  # 创建 ChuanganqiWidget 实例
        self.chuanganqi_widget.duan_licheng_received.connect(self.handle_duan_licheng)  # 连接信号
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.view = QGraphicsView(self)
        layout.addWidget(self.view)

        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        # 添加x轴和y轴
        self.draw_axes()

        # 添加小车图片
        self.car = self.scene.addPixmap(QPixmap("car.png").scaled(40, 40))  # 添加小车图片
        self.car.setOffset(-self.car.pixmap().width() / 2, -self.car.pixmap().height() / 2)  # 设置小车的中心位置
        self.car.setPos(0, 0)  # 设置小车初始位置

        # 添加一个标签用于显示小车坐标
        self.coord_label = QLabel(self)
        self.coord_label2 = QLabel(self)

        layout.addWidget(self.coord_label)
        layout.addWidget(self.coord_label2)

        self.setFocusPolicy(Qt.StrongFocus)  # 设置窗口部件可以获取焦点

    def draw_axes(self):
        pen = QPen(Qt.black)
        self.bili = 10
        # 绘制x轴和y轴
        self.scene.addLine(-300, 0, 0, 0, pen)  # x轴
        self.scene.addLine(-300, -50, -300, 0, pen)  # y轴

    # 重写键盘按下事件
    def keyPressEvent(self, event):
        step = 5  # 设置每次移动的步长
        rotation_step = 90  # 设置旋转步长
        if event.key() == Qt.Key_W:  # 如果按下了W键
            self.rotation_angle = 90
            self.move_ball(0, -step)  # 将小车向上移动
        elif event.key() == Qt.Key_S:  # 如果按下了S键
            self.rotation_angle = -90
            self.move_ball(0, step)  # 将小车向下移动
        elif event.key() == Qt.Key_A:  # 如果按下了A键
            self.rotation_angle = 0
            self.move_ball(-step, 0)  # 将小车向左移动
        elif event.key() == Qt.Key_D:  # 如果按下了D键
            self.rotation_angle = 180
            self.move_ball(step, 0)  # 将小车向右移动

    # 移动小车的方法
    def move_ball(self, dx, dy):
        current_pos = self.car.pos()  # 获取小车当前的位置
        new_pos = QPointF(current_pos.x() + dx, current_pos.y() + dy)  # 计算新的位置
        self.car.setPos(new_pos)  # 移动小车到新位置

        # 更新坐标标签
        self.coord_label.setText(f"Car Position: ({new_pos.x()}, {new_pos.y()})")

        # 旋转小车
        transform = QTransform().rotate(self.rotation_angle)
        self.car.setTransform(transform)

    # 移动小车到指定位置的方法
    def move_ball_to_position(self, x, y):
        # Convert coordinates to floats
        x_float = float(x)
        y_float = float(y)
        new_pos = QPointF(x_float, y_float)
        self.car.setPos(new_pos)
        self.coord_label.setText(f"Car Position: ({x_float}, {y_float})")
        # 旋转小车
        transform = QTransform().rotate(self.rotation_angle)
        self.car.setTransform(transform)