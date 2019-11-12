from PySide2.QtGui import QFont, QTextOption
from PySide2.QtWidgets import QFrame, QPlainTextEdit

from cells import events
from cells.observation import Observation
from cells.settings import FIGLET_NAME, ApplicationInfo


class Console(Observation, QPlainTextEdit):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        QPlainTextEdit.__init__(self)
        self.setReadOnly(True)
        self.setMinimumHeight(150)
        self.setMinimumWidth(250)
        self.setFrameShape(QFrame.NoFrame)
        self.sayHello()
        self.setWordWrapMode(QTextOption.NoWrap)

        font = QFont("Fira Code", 12)
        font.setWeight(QFont.Thin)
        self.setFont(font)
        self.add_responder(events.view.main.ConsoleClear,
                           self.consoleClearResponder)
        self.add_responder(events.backend.Stdout, self.backendStdoutResponder)
        self.add_responder(events.backend.Stderr, self.backendStderrResponder)

    def sayHello(self):
        hello = ApplicationInfo.name + " v" + str(ApplicationInfo.version)

        self.appendPlainText(hello)

    def consoleClearResponder(self, e):
        self.clear()

    def backendStdoutResponder(self, e):
        if e.output:
            self.appendPlainText(e.output)

    def backendStderrResponder(self, e):
        #TODO print in different color
        if e.output:
            self.appendPlainText(e.output)

    def clear(self):
        self.document().clear()

    def closeEvent(self, e):
        self.unregister()

        return super().closeEvent(e)
