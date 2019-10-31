from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLineEdit, QMessageBox, QVBoxLayout, QWidget

from cells import events
from cells.observation import Observation


class Track(Observation, QWidget):
    def __init__(self, subject, index, name):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color:red;")

        self.setFixedWidth(200)

        self.header = Header(subject, index)
        self.index = index

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.header)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignTop)

        self.setName(name)

        self.setFocusPolicy(Qt.ClickFocus)

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

    def focusInEvent(self, e):
        self.header.setFocus()


class Header(Observation, QWidget):
    def __init__(self, subject, index):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self.index = index

        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: grey;")

        self.setFixedHeight(100)

        self._initNameLabel()

        self.setLayout(QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.nameLabel)

        self.add_responder(events.view.main.TrackRemove,
                           self.mainTrackRemoveResponder)
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

    def mainTrackRemoveResponder(self, e):
        # I don't know why, but it doesn't work inside of Track itself:
        # - self.hasFocus() always returns False
        # - if I introduce self.selected, it changes correctly inside
        #   focusEvents but it somehow remains always True after just one
        #   select inside the responder (even given the fact, that it's
        #   changing inside of delegates %-| )

        if self.hasFocus():
            self.notify(events.view.track.Remove(self.index))

    def mainTrackMoveLeftResponder(self, e):
        if self.hasFocus() and self.index > 0:
            self.notify(events.view.track.Move(self.index, self.index - 1))

    def mainTrackMoveRightResponder(self, e):
        length = self.parentWidget().parentWidget().layout().count() - 1
        if self.hasFocus() and self.index < length:
            self.notify(events.view.track.Move(self.index, self.index + 1))

    def onNameChanged(self, name):
        self.notify(events.view.track.NameChanged(self.index, name))

    def focusInEvent(self, e):
        self.setStyleSheet("background-color: green;")

    def focusOutEvent(self, e):
        self.setStyleSheet("background-color: grey;")

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