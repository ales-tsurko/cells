from PySide2.QtWidgets import QListView

from cells.observation import Observation


class Browser(Observation, QListView):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        QListView.__init__(self)
        
        self.setStyleSheet("border: 0;")
        self.setMaximumWidth(250)
        self.setMinimumWidth(150)