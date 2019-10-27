import sys

from PySide2 import QtWidgets

from .main import Main


class App:
    def run(subject):
        app = QtWidgets.QApplication([])

        widget = Main(subject)
        widget.show()

        sys.exit(app.exec_())
