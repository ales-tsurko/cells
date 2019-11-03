import sys
import os

from PySide2 import QtWidgets
from PySide2.QtGui import QFontDatabase

from cells.settings import ApplicationInfo

from .main import Main
from .code import Code
from cells import events
from cells.observation import Observation

from rx.subject import Subject


class App(Observation):
    def __init__(self, subject):
        super().__init__(subject)
        self.subject = subject

        self.app = QtWidgets.QApplication([])
        self.app.setApplicationName(ApplicationInfo.name)
        self.app.setApplicationDisplayName(ApplicationInfo.name)

        font_path = os.path.join(get_resources_path(),
                                 "fonts", "FiraCode_2", "FiraCode-VF.ttf")
        QFontDatabase.addApplicationFont(font_path)
        self.main = Main(subject)

        self._init_responders()

    def document_new_responder(self, e):
        self.subject = Subject()
        self._init_responders()

        self.main.close()
        self.main.deleteLater()
        self.main = Main(self.subject)
        self.main.show()
        Code(self.subject).exec_()

    def _init_responders(self):
        self.add_responder(events.view.main.FileNew,
                           self.document_new_responder)

    def run(self):
        self.main.show()
        res = self.app.exec_()

        self.subject.on_next(events.app.Quit())

        sys.exit(res)


def get_resources_path():
    return os.path.join(os.path.dirname(__file__), "resources")
