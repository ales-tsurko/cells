import sys

from PySide2 import QtWidgets

from cells.settings import ApplicationInfo

from .main import Main
from cells import events


class App:
    def run(subject):
        app = QtWidgets.QApplication([])
        app.setApplicationName(ApplicationInfo.name)
        app.setApplicationDisplayName(ApplicationInfo.name)

        widget = Main(subject)
        widget.show()
        res = app.exec_()

        subject.on_next(events.app.Quit())

        sys.exit(res)
