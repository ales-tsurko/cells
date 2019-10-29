from PySide2.QtGui import QColor
from PySide2.QtWidgets import QWidget

from cells.observation import Observation


class Track(Observation, QWidget):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("red"))
        self.setPalette(palette)

        self.setFixedWidth(200)
