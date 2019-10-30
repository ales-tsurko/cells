import sys
import os

from PySide2 import QtWidgets
from PySide2.QtGui import QFontDatabase

from cells.settings import ApplicationInfo

from .main import Main
from cells import events


class App:
    def __init__(self, subject):
        self.subject = subject

        self.app = QtWidgets.QApplication([])
        self.app.setApplicationName(ApplicationInfo.name)
        self.app.setApplicationDisplayName(ApplicationInfo.name)

        font_path = os.path.join(App.get_resources_path(),
                                 "fonts", "FiraCode_2", "FiraCode-VF.ttf")
        QFontDatabase.addApplicationFont(font_path)
        self.main = Main(subject)

    def run(self):
        self.main.show()
        res = self.app.exec_()

        self.subject.on_next(events.app.Quit())

        sys.exit(res)

    def get_resources_path():
        return os.path.join(os.path.dirname(__file__), "resources")
