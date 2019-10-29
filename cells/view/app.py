import sys
import os

from PySide2 import QtWidgets
from PySide2.QtGui import QFontDatabase

from cells.settings import ApplicationInfo

from .main import Main
from cells import events


class App:
    def run(subject):
        app = QtWidgets.QApplication([])
        app.setApplicationName(ApplicationInfo.name)
        app.setApplicationDisplayName(ApplicationInfo.name)

        font_path = os.path.join(App.get_resources_path(),
                                 "fonts", "FiraCode_2", "FiraCode-VF.ttf")
        res = QFontDatabase.addApplicationFont(font_path)

        widget = Main(subject)
        widget.show()
        res = app.exec_()

        subject.on_next(events.app.Quit())

        sys.exit(res)

    def get_resources_path():
        return os.path.join(os.path.dirname(__file__), "resources")
