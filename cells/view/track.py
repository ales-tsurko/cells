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
        self.cells = [Cell(self, subject, 0)]

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.header)
        self.layout().addWidget(self.cells[0])
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignTop)

        self.setName(name)
        
        self.add_responder(events.view.main.RowAdd, self.rowAddResponder)
        
    def rowAddResponder(self, e):
        index = len(self.cells)
        cell = Cell(self, self.subject, index)
        self.cells.append(cell)
        self.layout().addWidget(cell)

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
        self.header.setSelected(value)


class CellBase(Observation, QWidget):
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
        
        self.updateStyle()

    def _initNameLabel(self):
        self.nameLabel = QLineEdit(self)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setWindowFlags(Qt.FramelessWindowHint)
        self.nameLabel.setStyleSheet("background: transparent; border: none;")
        self.nameLabel.setMaxLength(30)
        self.nameLabel.setContextMenuPolicy(Qt.NoContextMenu)
        self.nameLabel.textChanged.connect(self.onNameChanged)
        self.nameLabel.editingFinished.connect(self.onEditingNameFinished)

    def editNameResponder(self, e):
        if self.selected:
            self.nameLabel.setFocus()

    def onNameChanged(self, name):
        pass

    def onEditingNameFinished(self):
        self.nameLabel.clearFocus()

    def setSelected(self, value):
        self.selected = value
        self.updateStyle()
        
    def updateStyle(self):
        pass

    def setName(self, name):
        self.nameLabel.setText(name)


class Header(CellBase):
    def __init__(self, subject, index):
        super().__init__(subject, index)

        self.add_responder(events.view.main.TrackEditName,
                           self.editNameResponder)

    def onNameChanged(self, name):
        super().onNameChanged(name)
        self.notify(events.view.track.NameChanged(self.index, name))
        
    def updateStyle(self):
        if self.selected:
            self.setSelectedStyle()
        else:
            self.setNormalStyle()
            
    def setSelectedStyle(self):
        self.setStyleSheet("background-color: green;")
        
    def setNormalStyle(self):
        self.setStyleSheet("background-color: grey;")


class Cell(CellBase):
    def __init__(self, track, subject, index):
        self.track = track
        
        super().__init__(subject, index)

        self.add_responder(events.view.main.CellEditName,
                           self.editNameResponder)
        self.add_responder(events.view.track.Select,
                           self.trackSelectResponder)

    def _initNameLabel(self):
        super()._initNameLabel()
        self.nameLabel.setStyleSheet("background-color:rgba(255, 255, 255, 0.2); border: none;")
        self.nameLabel.setAlignment(Qt.AlignCenter | Qt.AlignTop)
    
    def editNameResponder(self, e):
        if self.selected and self.track.selected:
            self.nameLabel.setFocus()
        
    def trackSelectResponder(self, e):
        self.updateStyle()

    def updateStyle(self):
        if self.track.selected and self.selected:
            self.setSelectedStyle()
        elif self.track.selected:
            self.setInactiveStyle()
        else:
            self.setNormalStyle()
            
    def setSelectedStyle(self):
        self.setStyleSheet("background-color: brown;")

    def setInactiveStyle(self):
        self.setStyleSheet("background-color: #444;")
    
    def setNormalStyle(self):
        self.setStyleSheet("background-color: #333;")
        
    def setEvaluatedStyle(self):
        self.setStyleSheet("background-color: #49967d")