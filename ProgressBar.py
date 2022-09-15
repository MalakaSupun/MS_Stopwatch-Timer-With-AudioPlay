from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class CrlProgressBar(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # Parameters fro the project...
        self.value = 0
        self.width = 502
        self.height = 502
        self.progress_width = 12
        self.progress_rounded_cap = True
        self.enable_BackGround = True
        
        # Setting colours to the progress bar ...............
        self.BackGround_color = QColor(68, 71, 90, 110)
        self.progress_color = QColor(0, 237, 255, 200)
        
        # Max value is set to 60 because, to a minute there are 60 seconds...... 
        self.max_value = 60

        # Set default sizes........
        self.resize(self.width, self.height)

    def set_value(self,value):
        self.value = value
        self.repaint()

    def Set_Shadow(self, enable):
        if enable:
           self.shadow = QGraphicsDropShadowEffect(self)
           self.shadow.setBlurRadius(8)
           self.shadow.setXOffset(0)
           self.shadow.setYOffset(0)
           self.shadow.setColor(QColor(0, 0, 0, 130))
           self.setGraphicsEffect(self.shadow)

    def paintEvent(self, e):

        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = self.progress_width / 2
        value = self.value * 360 / self.max_value

        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)
        #paint.setFont(QFont(self.font_family, self.font_size))

        rect = QRect(0, 0, self.width, self.height)
        paint.setPen(Qt.NoPen)
        paint.drawRect(rect)

        pen = QPen()
        pen.setColor(QColor(self.progress_color))
        pen.setWidth(self.progress_width)

        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)

        if self.enable_BackGround:
            pen.setColor(QColor(self.BackGround_color))
            paint.setPen(pen)
            paint.drawArc(margin, margin, width, height, 0, 360 * 16)

        pen.setColor(QColor(self.progress_color))
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, 90 * 16, -value * 16)

        paint.end()
