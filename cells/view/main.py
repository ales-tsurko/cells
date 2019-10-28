from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (QFileDialog, QLabel, QMainWindow, QMessageBox,
                               QScrollArea)

from cells import events
from cells.observation import Observation


class Main(QMainWindow, Observation):
    """Main Window."""
    def __init__(self, subject):
        """Initializer."""
        QMainWindow.__init__(self)
        Observation.__init__(self, subject)

        self.setWindowTitle('Default')
        self.setMinimumSize(800, 600)
        self._createMenu()
        self._init_central_widget()

        self.document = None

        self.add_responder(events.document.Load, self.documentLoadResponder)

    def _createMenu(self):
        self.menuBar().addAction("Set")
        self._createFileMenu()

    def _createFileMenu(self):
        fileMenu = self.menuBar().addMenu("File")
        self._addAction(fileMenu, "New", QKeySequence.New, self.onFileNew)
        self._addAction(fileMenu, "Open", QKeySequence.Open, self.onFileOpen)
        self._addAction(fileMenu, "Save", QKeySequence.Save, self.onFileSave)
        self._addAction(fileMenu,
                        "Duplicate",
                        QKeySequence.SaveAs,
                        self.onFileSaveAs)

    def _addAction(self, menu, name, shortcut, callback):
        newAct = menu.addAction(name)
        newAct.triggered.connect(callback)
        newAct.setShortcuts(shortcut)

    def _init_central_widget(self):
        scrollArea = QScrollArea()
        label = QLabel("Hi there")
        scrollArea.setWidget(label)
        self.setCentralWidget(scrollArea)

    def onFileNew(self, e):
        self.notify(events.document.New())

    def onFileOpen(self, e):
        fname = QFileDialog.getOpenFileName(self,
                                            "Open Project",
                                            filter="Cells Files (*.cells)")

        if fname[0]:
            self.notify(events.document.Open(fname[0]))

    def onFileSave(self, e):
        if not self.document:
            self.onFileSaveAs(e)
        else:
            self.notify(events.document.Save())

    def onFileSaveAs(self, e):
        fname = QFileDialog.getSaveFileName(self,
                                            "Save Project",
                                            filter="Cells Files (*.cells)")

        if fname[0]:
            self.notify(events.document.SaveAs(fname[0]))

    def documentLoadResponder(self, e):
        print(e)
        self.document = e.document

    def keyPressEvent(self, e):
        pass

    def closeEvent(self, e):
        if not self.document or not self.document.saved:
            reply = QMessageBox.question(self, 
                                         'Closing Document',
                                         "Do you save changes?", 
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                self.onFileSave(e)

        self.notify(events.document.Close(self.document))
