# import PyQt5 libraries .....................
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class CrlProgressBar(QWidget):
    def __init__(self):
        QWidget.__init__(self)
               
        self.value = 0            # value of the progress bar
        self.width = 502          # Width of progress bar 
        self.height = 502         # Height of progress bar
        self.progress_width = 12  # Width of progress bar 
        
        # Making end of bar round............
        self.progress_rounded_cap = True
        
        # Making background circle...........
        self.enable_BackGround = True
        
        # Setting colours to the progress bar ...............
        self.BackGround_color = QColor(68, 71, 90, 110) # Background color for progress bar
        self.progress_color = QColor(0, 237, 255, 200)  # Background color for progress bar
        
        # Max value is set to 60 because, to a minute there are 60 seconds...... 
        self.max_value = 60

        # Set default sizes........
        self.resize(self.width, self.height)

    def set_value(self,value):
        # Make the round progress bar draws again and again ...................
        self.value = value
        self.repaint()

    def Set_Shadow(self, enable):
        # Setting  a shadow to the progress Bar ..............................
        if enable:
           self.shadow = QGraphicsDropShadowEffect(self)
           self.shadow.setBlurRadius(8)
           self.shadow.setXOffset(0)
           self.shadow.setYOffset(0)
           self.shadow.setColor(QColor(0, 0, 0, 130))
           self.setGraphicsEffect(self.shadow)
            
    # Main painting method.......................
    def paintEvent(self, e):
       
        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = self.progress_width / 2
        value = self.value * 360 / self.max_value

        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)
       
        rect = QRect(0, 0, self.width, self.height)
        paint.setPen(Qt.NoPen)
        paint.drawRect(rect)

        pen = QPen()
        pen.setColor(QColor(self.progress_color))
        pen.setWidth(self.progress_width)

        # Painting Round Progress........................ 
        if self.progress_rounded_cap:
            # Set up rounded cap for drawing pen ........
            pen.setCapStyle(Qt.RoundCap)
        
        # Enable background circle........................
        if self.enable_BackGround:
            pen.setColor(QColor(self.BackGround_color))
            paint.setPen(pen)
            paint.drawArc(margin, margin, width, height, 0, 360 * 16)

        pen.setColor(QColor(self.progress_color))
        paint.setPen(pen)
        
        # Drawing progress bar............... 
        paint.drawArc(margin, margin, width, height, 90 * 16, -value * 16)

        # Finishing the round progress bar ............
        paint.end()
