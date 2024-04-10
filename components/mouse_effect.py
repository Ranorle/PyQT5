import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class RlatticeEffect(QWidget):

    def __init__(self, *args, **kwargs):
        super(RlatticeEffect, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.points = []
        self.target = Target(self.width() / 2, self.height() / 2)
        self.initPoints()

    def update(self, *args):
        super(RlatticeEffect, self).update()

    def paintEvent(self, event):
        super(RlatticeEffect, self).paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.black)
        self.animate(painter)
        painter.end()

    def mouseMoveEvent(self, event):
        super(RlatticeEffect, self).mouseMoveEvent(event)
        # 鼠标移动时更新xy坐标
        self.target.x = event.x()
        self.target.y = event.y()
        self.update()

    def initPoints(self):
        t = time()
        self.points.clear()
        # 创建点
        stepX = self.width() / 20
        stepY = self.height() / 20
        for x in range(0, self.width(), int(stepX)):
            for y in range(0, self.height(), int(stepY)):
                ox = x + random() * stepX
                oy = y + random() * stepY
                point = Point(ox, ox, oy, oy)
                point.valueChanged.connect(self.update)
                self.points.append(point)
        print(time() - t)

        t = time()
        # 每个点寻找5个闭合点
        findClose(self.points)
        print(time() - t)

    def animate(self, painter):
        for p in self.points:
            # 检测点的范围
            value = abs(getDistance(self.target, p))
            if value < 4000:
                # 其实就是修改颜色透明度
                p.lineColor.setAlphaF(0.3)
                p.circleColor.setAlphaF(0.6)
            elif value < 20000:
                p.lineColor.setAlphaF(0.1)
                p.circleColor.setAlphaF(0.3)
            elif value < 40000:
                p.lineColor.setAlphaF(0.02)
                p.circleColor.setAlphaF(0.1)
            else:
                p.lineColor.setAlphaF(0)
                p.circleColor.setAlphaF(0)

            # 画线条
            if p.lineColor.alpha():
                for pc in p.closest:
                    if not pc:
                        continue
                    path = QPainterPath()
                    path.moveTo(p.x, p.y)
                    path.lineTo(pc.x, pc.y)
                    painter.save()
                    painter.setPen(p.lineColor)
                    painter.drawPath(path)
                    painter.restore()

            # 画圆
            painter.save()
            painter.setPen(Qt.NoPen)
            painter.setBrush(p.circleColor)
            painter.drawRoundedRect(QRectF(
                p.x - p.radius, p.y - p.radius, 2 * p.radius, 2 * p.radius), p.radius, p.radius)
            painter.restore()

            # 开启动画
            p.initAnimation()