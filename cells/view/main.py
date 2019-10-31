from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (QFileDialog, QMainWindow, QMessageBox,
                               QVBoxLayout, QWidget)

from cells import events
from cells.observation import Observation

from .console import Console
from .editor import Editor
from .settings import Settings
from cells.models.document import Document


class Main(QMainWindow, Observation):

    def __init__(self, subject):
        QMainWindow.__init__(self, None)
        Observation.__init__(self, subject)

        self.setWindowTitle("Default")
        self.setMinimumSize(800, 600)
        self._createMenu()
        self._initCentralWidget()

        document = Document(self.subject)
        self.document = document.model
        self.setWindowTitle(self.document.name)
        self.saved = True

        self.add_responder(events.document.Open, self.documentOpenResponder)
        self.add_responder(events.document.Update,
                           self.documentUpdateResponder)
        self.add_responder(events.document.Error, self.documentErrorResponder)

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

        trackSub = editMenu.addMenu("Track")
        self._addMenuAction(trackSub, "Add", self.tr('Ctrl+t'),
                            self.onTrackAdd)
        self._addMenuAction(trackSub, "Remove",
                            self.tr('Ctrl+Backspace'),
                            self.onTrackRemove)
        self._addMenuAction(trackSub, "Select Left",
                            self.tr('h'),
                            self.onTrackSelectLeft)
        self._addMenuAction(trackSub, "Select Right",
                            self.tr('l'),
                            self.onTrackSelectRight)
        self._addMenuAction(trackSub, "Move Left",
                            self.tr('Shift+h'),
                            self.onTrackMoveLeft)
        self._addMenuAction(trackSub, "Move Right",
                            self.tr('Shift+l'),
                            self.onTrackMoveRight)

        rowSub = editMenu.addMenu("Row")
        self._addMenuAction(rowSub, "Add", self.tr('Enter'),
                            self.onRowAdd)
        self._addMenuAction(rowSub, "Evaluate", self.tr('Ctrl+Enter'),
                            self.onRowEvaluate)
        self._addMenuAction(rowSub, "Remove",
                            self.tr('Shift+Backspace'),
                            self.onRowRemove)
        self._addMenuAction(rowSub, "Select Up",
                            self.tr('k'),
                            self.onRowSelectUp)
        self._addMenuAction(rowSub, "Select Down",
                            self.tr('j'),
                            self.onRowSelectDown)
        self._addMenuAction(rowSub, "Move Up", self.tr('Shift+K'),
                            self.onRowMoveUp)
        self._addMenuAction(rowSub, "Move Down", self.tr('Shift+J'),
                            self.onRowMoveDown)
        self._addMenuAction(rowSub, "Copy", self.tr('Ctrl+Shift+C'),
                            self.onRowCopy)
        self._addMenuAction(rowSub, "Cut", self.tr('Ctrl+Shift+X'),
                            self.onRowCut)
        self._addMenuAction(rowSub, "Paste", self.tr('Ctrl+Shift+V'),
                            self.onRowPaste)

        cellSub = editMenu.addMenu("Cell")
        self._addMenuAction(cellSub, "Edit", self.tr('E'),
                            self.onCellEdit)
        self._addMenuAction(cellSub, "Evaluate", self.tr('Shift+Enter'),
                            self.onCellEvaluate)
        self._addMenuAction(cellSub, "Clear", self.tr('Backspace'),
                            self.onCellClear)

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

    def onTrackAdd(self, e):
        self.notify(events.view.main.TrackNew())

    def onTrackRemove(self, e):
        self.notify(events.view.main.TrackRemove())

    def onTrackSelectLeft(self, e):
        self.notify(events.view.main.TrackSelectLeft())
        
    def onTrackSelectRight(self, e):
        self.notify(events.view.main.TrackSelectRight())

    def onTrackMoveLeft(self, e):
        self.notify(events.view.main.TrackMoveLeft())

    def onTrackMoveRight(self, e):
        self.notify(events.view.main.TrackMoveRight())

    def onRowAdd(self, e):
        self.notify(events.view.main.RowAdd())

    def onRowRemove(self, e):
        self.notify(events.view.main.RowRemove())
        
    def onRowSelectUp(self, e):
        self.notify(events.view.main.RowSelectUp())
        
    def onRowSelectDown(self, e):
        self.notify(events.view.main.RowSelectDown())

    def onRowMoveUp(self, e):
        self.notify(events.view.main.RowMoveUp())

    def onRowMoveDown(self, e):
        self.notify(events.view.main.RowMoveDown())

    def onRowEvaluate(self, e):
        self.notify(events.view.main.RowEvaluate())

    def onRowCopy(self, e):
        self.notify(events.view.main.RowCopy())

    def onRowCut(self, e):
        self.notify(events.view.main.RowCut())

    def onRowPaste(self, e):
        self.notify(events.view.main.RowPaste())

    def onCellEvaluate(self, e):
        self.notify(events.view.main.CellEvaluate())

    def onCellClear(self, e):
        self.notify(events.view.main.CellClear())

    def onCellEdit(self, e):
        self.notify(events.view.main.CellEdit())

    def checkSave(self, e):
        if not self.saved:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Closing Document")
            msgBox.setText("Do you want to save changes?")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setDefaultButton(QMessageBox.Yes)
            reply = msgBox.exec()

            if reply == QMessageBox.Yes:
                self.onFileSave(e)

        self.saved = True

    def closeEvent(self, e):
        self.checkSave(e)

        self.notify(events.view.main.Close())
        super().closeEvent(e)
