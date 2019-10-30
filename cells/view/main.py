from PySide2.QtCore import Qt
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (QFileDialog, QMainWindow, QMessageBox,
                               QVBoxLayout, QWidget)

from cells import events
from cells.observation import Observation

from .console import Console
from .editor import Editor
from .settings import Settings


class Main(QMainWindow, Observation):

    def __init__(self, subject):
        QMainWindow.__init__(self)
        Observation.__init__(self, subject)

        self.setWindowTitle("Default")
        self.setMinimumSize(800, 600)
        self._createMenu()
        self._initCentralWidget()

        self.document = None
        self.saved = True

        self.add_responder(events.document.New, self.documentNewResponder)
        self.add_responder(events.document.Open, self.documentOpenResponder)
        self.add_responder(events.document.Update,
                           self.documentUpdateResponder)
        self.add_responder(events.document.Error, self.documentErrorResponder)
        self.notify(events.view.main.FileNew())

    def _createMenu(self):
        self._createFileMenu()
        self._createEditMenu()

    def _createFileMenu(self):
        fileMenu = self.menuBar().addMenu("File")
        self._addMenuAction(fileMenu, "New", QKeySequence.New, self.onFileNew)
        self._addMenuAction(fileMenu, "Open", QKeySequence.Open,
                            self.onFileOpen)
        self._addMenuAction(fileMenu, "Save", QKeySequence.Save,
                            self.onFileSave)
        self._addMenuAction(fileMenu,
                            "Duplicate",
                            QKeySequence.SaveAs,
                            self.onFileSaveAs)

    def _createEditMenu(self):
        editMenu = self.menuBar().addMenu("Edit")
        self._addMenuAction(editMenu, "New Track", self.tr('Ctrl+t'),
                            self.onNewTrack)
        editMenu.addSeparator()
        self._addMenuAction(editMenu, "Settings", QKeySequence.Preferences,
                            self.onSettings)

    def _addMenuAction(self, menu, name, shortcut, callback):
        newAct = menu.addAction(name)
        newAct.triggered.connect(callback)
        newAct.setShortcut(shortcut)

    def _initCentralWidget(self):
        centralView = QWidget()
        layout = QVBoxLayout()
        editor = Editor(self.subject)
        console = Console(self.subject)

        layout.setSpacing(0)
        layout.addWidget(editor)
        layout.addWidget(console)

        centralView.setLayout(layout)
        centralView.layout().setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(centralView)

    def documentNewResponder(self, e):
        self.document = e.document
        self.setWindowTitle(self.document.name)

    def documentOpenResponder(self, e):
        self.document = e.document
        self.setWindowTitle(self.document.name)
        self.saved = True

    def documentUpdateResponder(self, e):
        self.saved = False
        self.setWindowTitle("* " + e.document.name)

    def documentErrorResponder(self, e):
        dialog = QMessageBox()
        dialog.setText(e.message)
        dialog.setWindowTitle("Error")
        dialog.exec_()

    def onFileNew(self, e):
        self.checkSave(e)
        self.notify(events.view.main.FileNew())
        self.saved = True

    def onFileOpen(self, e):
        self.checkSave(e)

        fname = QFileDialog.getOpenFileName(self,
                                            "Open Project",
                                            filter="Cells Files (*.cells)")

        if fname[0]:
            self.notify(events.view.main.FileOpen(fname[0]))
            self.saved = True

    def onFileSave(self, e):
        if self.document.path is None:
            self.onFileSaveAs(e)
        else:
            self.notify(events.view.main.FileSave(self.document.path))
            self.setWindowTitle(self.document.name)
            self.saved = True

    def onFileSaveAs(self, e):
        fname = QFileDialog.getSaveFileName(self,
                                            "Save Project",
                                            filter="Cells Files (*.cells)")

        if fname[0]:
            self.notify(events.view.main.FileSaveAs(fname[0]))
            self.setWindowTitle(self.document.name)
            self.saved = True

    def onSettings(self, e):
        settings = Settings(self.subject)
        settings.exec_()

    def onNewTrack(self, e):
        self.notify(events.view.main.TrackNew())

    def keyPressEvent(self, e):
        pass

    def checkSave(self, e):
        if not self.saved:
            reply = QMessageBox.question(self,
                                         'Closing Document',
                                         "Do you want to save changes?",
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                self.onFileSave(e)

        self.saved = True

    def closeEvent(self, e):
        self.checkSave(e)

        self.notify(events.view.main.Close())
