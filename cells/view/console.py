from PySide2.QtWidgets import QFrame, QTextEdit
from PySide2.QtGui import QFont

from cells.observation import Observation
from cells.settings import ApplicationInfo
from cells import events


class Console(Observation, QTextEdit):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        QTextEdit.__init__(self)
        self.setReadOnly(True)
        self.setFixedHeight(200)
        self.setFrameShape(QFrame.NoFrame)
        self.sayHello()

        font = QFont("Fira Code", 12)
        font.setWeight(QFont.Thin)
        self.setFont(font)
        self.add_responder(events.view.main.ConsoleClear,
                           self.consoleClearResponder)

    def sayHello(self):
        hello = ApplicationInfo.name + " v" + str(ApplicationInfo.version)
        self.append(hello)

    def consoleClearResponder(self, e):
        self.clear()

    def clear(self):
        self.setText("")

    def closeEvent(self, e):
        self.unregister()
        return super().closeEvent(e)
