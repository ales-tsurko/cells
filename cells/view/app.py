import os
import sys
import asyncio

from asyncqt import QEventLoop

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QFontDatabase

from cells.settings import ApplicationInfo

from .main import Main
from cells import events
from cells.observation import Observation

from rx.subject import Subject
import cells.utility as utility
from cells.backend import Backend


class App(Observation):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        self.subject = subject

        self.app = QApplication(sys.argv)
        self.app.setApplicationName(ApplicationInfo.name)
        self.app.setApplicationDisplayName(ApplicationInfo.name)

        font_path = os.path.join(utility.viewResourcesDir(),
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

    def _init_responders(self):
        self.add_responder(events.view.main.FileNew,
                           self.document_new_responder)

    def run(self):
        backend = Backend(self.subject)
        loop = QEventLoop(self.app)
        asyncio.set_event_loop(loop)
        self.main.show()
        loop.create_task(backend.run())

        self.subject.on_next(events.app.Quit())

        with loop:
            sys.exit(loop.run_forever())
