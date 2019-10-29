from PySide2.QtWidgets import QTextEdit
from cells.observation import Observation


class Console(Observation, QTextEdit):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        QTextEdit.__init__(self)
        self.setReadOnly(True)
        self.setFixedHeight(200)
