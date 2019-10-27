from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QFileDialog, QLabel, QMainWindow

from cells import events
from cells.observer import Observer


class Main(QMainWindow, Observer):
    """Main Window."""
    def __init__(self, subject):
        """Initializer."""
        QMainWindow.__init__(self)
        Observer.__init__(self, subject)

        self.setWindowTitle('Default')
        self.setMinimumSize(800, 600)
        self.setCentralWidget(QLabel("I'm the Central Widget"))
        self._createMenu()

        self.document = None

        self.add_responder(events.document.Load, self.documentLoadResponder)

    def _createMenu(self):
        self._createFileMenu()

    def _createFileMenu(self):
        fileMenu = self.menuBar().addMenu('File')
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

    def onFileNew(self, e):
        self.notify(events.file.New())

    def onFileOpen(self, e):
        fname = QFileDialog.getOpenFileName(self,
                                            "Open Project",
                                            filter="Cells Files (*.cells)")

        if fname[0]:
            self.notify(events.file.Open(fname[0]))

    def onFileSave(self, e):
        if not self.document:
            self.onFileSaveAs(e)
        else:
            self.notify(events.file.Save())

    def onFileSaveAs(self, e):
        fname = QFileDialog.getSaveFileName(self,
                                            "Save Project",
                                            filter="Cells Files (*.cells)")

        if fname[0]:
            self.notify(events.file.SaveAs(fname[0]))

    def documentLoadResponder(self, e):
        print(e)
        self.document = e.document
