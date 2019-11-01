from cells.observation import Observation
from cells import events
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QLineEdit, QMessageBox, QVBoxLayout,
                               QWidget, QAction)
from PySide2.QtGui import QIcon


class Track(Observation, QWidget):
    def __init__(self, subject, index, name):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self.index = index
        self.selected = False

        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color:red;")

        self.setFixedWidth(200)

        self.header = Header(subject, index)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.header)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignTop)

        self.setName(name)

        # self.setFocusPolicy(Qt.ClickFocus)

        self.add_responder(events.view.track.Move,
                           self.selfMoveResponder)

    def selfMoveResponder(self, e):
        if self.index == e.index:
            self.setIndex(e.new_index)
        elif self.index == e.new_index:
            self.setIndex(e.index)

    def initConfirmDelete(self):
        name = self.header.nameLabel.text()
        question = f'Do you really want to delete track {name}?'
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Delete Track")
        msgBox.setText(question)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)

        return msgBox

    def setName(self, name):
        self.header.setName(name)

    def name(self):
        return self.header.nameLabel.text()

    def setIndex(self, index):
        self.index = index
        self.header.index = index

    def mousePressEvent(self, event):
        self.notify(events.view.track.Clicked(self.index))
        return super().mousePressEvent(event)

    def setSelected(self, value):
        self.selected = value
        if value:
            self.header.onSelect()
        else:
            self.header.onDeselect()


class Header(Observation, QWidget):
    def __init__(self, subject, index):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self.index = index
        self.selected = False

        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: grey;")

        self.setFixedHeight(100)

        self._initNameLabel()

        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.nameLabel)

        self.add_responder(events.view.main.TrackMoveLeft,
                           self.mainTrackMoveLeftResponder)
        self.add_responder(events.view.main.TrackMoveRight,
                           self.mainTrackMoveRightResponder)

    def _initNameLabel(self):
        self.nameLabel = QLineEdit(self)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setWindowFlags(Qt.FramelessWindowHint)
        self.nameLabel.setStyleSheet("background: transparent; border: none;")
        self.nameLabel.setMaxLength(30)
        self.nameLabel.setContextMenuPolicy(Qt.NoContextMenu)
        self.nameLabel.textChanged.connect(self.onNameChanged)

    def mainTrackMoveLeftResponder(self, e):
        if self.hasFocus() and self.index > 0:
            self.notify(events.view.track.Move(self.index, self.index - 1))

    def mainTrackMoveRightResponder(self, e):
        length = self.totalTracksNum() - 1
        if self.hasFocus() and self.index < length:
            self.notify(events.view.track.Move(self.index, self.index + 1))

    def onNameChanged(self, name):
        self.notify(events.view.track.NameChanged(self.index, name))
        
    def onSelect(self):
        self.selected = True
        self.setStyleSheet("background-color: green;")
        
    def onDeselect(self):
        self.selected = False
        self.setStyleSheet("background-color: grey;")

    def totalTracksNum(self):
        return self.parentWidget().parentWidget().layout().count()

    def setName(self, name):
        self.nameLabel.setText(name)


class Cell(Observation, QWidget):
    def __init__(self, subject, index):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self.index = index

        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: yellow;")

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
        self.nameLabel.setStyleSheet("background: transparent; border: none;")
        self.nameLabel.setMaxLength(30)
        self.nameLabel.setContextMenuPolicy(Qt.NoContextMenu)
        self.nameLabel.textChanged.connect(self.onNameChanged)
