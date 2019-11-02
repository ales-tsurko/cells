from PySide2.QtWidgets import QFrame, QTextEdit
from PySide2.QtGui import QFont

from cells.observation import Observation


class Console(Observation, QTextEdit):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        QTextEdit.__init__(self)
        self.setReadOnly(True)
        self.setFixedHeight(200)
        self.setFrameShape(QFrame.NoFrame)
        self.append("console messages go here")

        font = QFont("Fira Code", 12)
        font.setWeight(QFont.Thin)
        self.setFont(font)

    def closeEvent(self, e):
        self.unregister()
        return super().closeEvent(e)
