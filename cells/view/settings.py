from PySide2.QtWidgets import QDialog
from cells.observation import Observation


class Settings(Observation, QDialog):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        QDialog.__init__(self)

        self.setWindowTitle("Settings")
        self.setFixedSize(600, 400)
