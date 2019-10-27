from PySide2.QtWidgets import QLabel, QMainWindow
from cells.observer import Observer
from cells.events import file


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

    def _createMenu(self):
        self._createFileMenu()

    def _createFileMenu(self):
        fileMenu = self.menuBar().addMenu('File')
        fileMenu.addAction("New")
        fileMenu.addAction("Open")
        fileMenu.addAction("Save")
        fileMenu.addAction("Duplicate")
