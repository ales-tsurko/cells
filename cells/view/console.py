from PySide2.QtWidgets import QFrame, QPlainTextEdit
from PySide2.QtGui import QFont

from cells.observation import Observation
from cells.settings import ApplicationInfo
from cells import events


class Console(Observation, QPlainTextEdit):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        QPlainTextEdit.__init__(self)
        self.setReadOnly(True)
        self.setMinimumHeight(150)
        self.setMinimumWidth(250)
        self.setFrameShape(QFrame.NoFrame)
        self.sayHello()

        font = QFont("Fira Code", 12)
        font.setWeight(QFont.Thin)
        self.setFont(font)
        self.add_responder(events.view.main.ConsoleClear,
                           self.consoleClearResponder)
        self.add_responder(events.backend.Stdout,
                           self.backendStdoutResponder)

    def sayHello(self):
        hello = ApplicationInfo.name + " v" + str(ApplicationInfo.version)
        self.appendPlainText(hello)

    def consoleClearResponder(self, e):
        self.clear()
        
    def backendStdoutResponder(self, e):
        self.appendPlainText(e.output)
        
    def clear(self):
        self.document().clear()

    def closeEvent(self, e):
        self.unregister()
        return super().closeEvent(e)