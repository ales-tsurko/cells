from PySide2.QtCore import Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QLineEdit, QVBoxLayout, QWidget

from cells import events
from cells.observation import Observation


class Track(Observation, QWidget):
    def __init__(self, subject, index, name):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("red"))
        self.setPalette(palette)

        self.setFixedWidth(200)

        self.header = Header(subject, index)
        self.index = index

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.header)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignTop)

        self.setName(name)

    def setName(self, name):
        self.header.setName(name)


class Header(Observation, QWidget):
    def __init__(self, subject, index):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self.index = index

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("blue"))
        self.setPalette(palette)

        self.setFixedHeight(100)

        self._initNameLabel()

        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.nameLabel)

    def _initNameLabel(self):
        self.nameLabel = QLineEdit(self)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setWindowFlags(Qt.FramelessWindowHint)
        self.nameLabel.setStyleSheet("background:transparent; border: none;")
        self.nameLabel.setMaxLength(30)
        self.nameLabel.setContextMenuPolicy(Qt.NoContextMenu)
        self.nameLabel.textChanged.connect(self.onNameChanged)

    def setName(self, name):
        self.nameLabel.setText(name)

    def onNameChanged(self, name):
        self.notify(events.view.track.NameChanged(self.index, name))
