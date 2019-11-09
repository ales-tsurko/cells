import asyncio
import os
import sys

from PySide2.QtGui import QFontDatabase
from PySide2.QtWidgets import QApplication

import cells.utility as utility
from asyncqt import QEventLoop
from cells import events
from cells.backend import BackendRouter
from cells.observation import Observation
from cells.settings import ApplicationInfo
from rx.subject import Subject

from .main import Main


class App(Observation):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        self.subject = subject
        self.loop = None
        self.backend = None

        self.app = QApplication(sys.argv)
        self.app.setApplicationName(ApplicationInfo.name)
        self.app.setApplicationDisplayName(ApplicationInfo.name)

        font_path = os.path.join(utility.viewResourcesDir(), "fonts",
                                 "FiraCode_2", "FiraCode-VF.ttf")
        QFontDatabase.addApplicationFont(font_path)
        self.main = Main(subject)

        self._init_responders()

    def document_new_responder(self, e):
        self.subject = Subject()
        self._init_responders()

        self.main.close()
        self.main.deleteLater()
        self.main = Main(self.subject)
        self.backend.delete()
        self.backend = BackendRouter(self.loop, self.subject)

        self.main.show()

    def _init_responders(self):
        self.add_responder(events.view.main.FileNew,
                           self.document_new_responder)

    def run(self):
        self.loop = QEventLoop(self.app)
        self.backend = BackendRouter(self.loop, self.subject)
        asyncio.set_event_loop(self.loop)
        self.main.show()

        self.subject.on_next(events.app.Quit())

        with self.loop:
            sys.exit(self.loop.run_forever())
