import random

from cells import events
from cells.observation import Observation
from cells.settings import FIGLET_NAME, ApplicationInfo
from PySide2.QtCore import Qt
from PySide2.QtGui import QTextOption
from PySide2.QtWidgets import QFrame, QTextEdit

from .theme import ScrollBar, Theme


class Console(Observation, QTextEdit):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        QTextEdit.__init__(self)
        self.whoami = self._initWhoami()
        self.setReadOnly(True)
        self.setMinimumHeight(162)
        self.setMinimumWidth(252)
        self.setFrameShape(QFrame.NoFrame)
        self.sayHello()
        self.setWordWrapMode(QTextOption.NoWrap)

        self.setHorizontalScrollBar(ScrollBar())
        self.setVerticalScrollBar(ScrollBar())
        self.setFont(Theme.console.font)
        self.setStyleSheet(Theme.console.style)

        self.add_responder(events.view.main.ConsoleClear,
                           self.consoleClearResponder)
        self.add_responder(events.backend.Stdout, self.backendStdoutResponder)
        self.add_responder(events.backend.Stderr, self.backendStderrResponder)

    def _initWhoami(self):
        first = random.choice(
            ["Live", "Generative", "Algorithmic", "Creative"])
        second = random.choice(
            ["Coding", "Prototyping", "Audio", "Visuals", "Thing"])
        third = random.choice(
            ["Environment", "Workstation", "Sequencer", "Editor"])

        return f"{first} {second} {third}"

    def sayHello(self):
        self.appendOutput(FIGLET_NAME)
        version = f"{self.whoami} v{ApplicationInfo.version}"
        longestLine = max(FIGLET_NAME.splitlines(), key=lambda line: len(line))
        numOfSpaces = (len(longestLine) - len(version)) // 2
        self.appendOutput(" " * numOfSpaces + version)

    def consoleClearResponder(self, e):
        self.clear()

    def backendStdoutResponder(self, e):
        self.appendOutput(e.output)

    def backendStderrResponder(self, e):
        self.appendOutput(e.output, True)

    def appendOutput(self, text, err=False):
        if text:
            color = Theme.console.stderrFontColor if err else Theme.console.stdoutFontColor
            self.setTextColor(color)
            self.append(text)

    def clear(self):
        self.document().clear()

    def closeEvent(self, e):
        self.unregister()

        super().closeEvent(e)
