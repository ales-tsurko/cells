import asyncio
import os
import sys

from asyncqt import QEventLoop
from cells import events
from cells.backend import BackendRouter
from cells.observation import Observation
from cells.settings import ApplicationInfo
from PySide2.QtWidgets import QApplication
from rx.subject import Subject

from .main import Main
from .theme import Fonts


class App(Observation):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        self.subject = subject
        self.loop = None
        self.backend = None

        self.app = QApplication(sys.argv)
        self.app.setApplicationName(ApplicationInfo.name)
        self.app.setApplicationDisplayName(ApplicationInfo.name)

        Fonts.initDb()

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

        with self.loop:
            code = self.loop.run_forever()
            pending = asyncio.Task.all_tasks()
            self.notify(events.app.Quit())
            try:
                self.loop.run_until_complete(
                    asyncio.wait_for(asyncio.gather(*pending), 10))
            except asyncio.futures.TimeoutError as e:
                print(e)
            sys.exit(code)
