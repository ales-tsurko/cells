from cells.observation import Observation
from cells import events
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QLineEdit, QMessageBox, QVBoxLayout,
                               QWidget, QAction)
from PySide2.QtGui import QIcon

from .dialogs import ConfirmationDialog


class Track(Observation, QWidget):
    def __init__(self, subject, index, name):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self.index = index
        self.selected = False
        self.selectedCellIndex = -1
        self.cells = []

        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")

        self.setFixedWidth(200)

        self.header = Header(subject, index)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.header)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignTop)

        self.setName(name)

        self.add_responder(events.view.main.RowAdd, self.rowAddResponder)
        self.add_responder(events.view.main.RowSelectUp,
                           self.rowSelectUpResponder)
        self.add_responder(events.view.main.RowSelectDown,
                           self.rowSelectDownResponder)
        self.add_responder(events.view.track.RowRemove, self.rowRemoveResponder)

    def rowAddResponder(self, e):
        self.addCell()

    def rowSelectUpResponder(self, e):
        if not self.selected or len(self.cells) < 1:
            return

        if not self.isThereSelectedCell():
            self.selectRowAt(len(self.cells) - 1)
        else:
            self.selectRowAt(self.selectedCellIndex - 1)

    def rowSelectDownResponder(self, e):
        if not self.selected or len(self.cells) < 1:
            return

        if not self.isThereSelectedCell():
            self.selectRowAt(0)
        else:
            self.selectRowAt(self.selectedCellIndex + 1)

    def rowRemoveResponder(self, e):
        if self.selectedCellIndex != e.index:
            return
        
        cell = self.cells.pop(e.index)
        
        cell.setParent(None)
        self.notify(events.view.track.CellRemove(self.index, e.index))
        for cell in self.cells[e.index:]:
            cell.index -= 1

    def addCell(self, notify=True):
        index = len(self.cells)
        cell = Cell(self, self.subject, index)
        cell.setName(str(index + 1))
        self.cells.append(cell)
        self.layout().addWidget(cell)

        if notify:
            self.notify(events.view.track.CellAdd(self.index, cell.name()))

        return cell

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

    def selectRowAt(self, index):
        if self.selectedCellIndex == index:
            return

        self.selectedCellIndex = min(max(-1, index), len(self.cells))
        self.notify(events.view.track.RowSelect(self.selectedCellIndex))

    def isThereSelectedCell(self):
        return self.selectedCellIndex in range(len(self.cells))


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
            self.nameLabel.selectAll()

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

    def name(self):
        return self.nameLabel.text()


class Header(CellBase):
    def __init__(self, subject, index):
        super().__init__(subject, index)

        self.add_responder(events.view.main.TrackEditName,
                           self.editNameResponder)

    def onEditingNameFinished(self):
        self.notify(events.view.track.NameChanged(self.index, self.name()))
        return super().onEditingNameFinished()

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

        self.layout().setAlignment(Qt.AlignTop)

        self.add_responder(events.view.main.CellEditName,
                           self.editNameResponder)
        self.add_responder(events.view.track.Select,
                           self.trackSelectResponder)
        self.add_responder(events.view.track.RowSelect,
                           self.rowSelectResponder)

    def _initNameLabel(self):
        super()._initNameLabel()
        self.nameLabel.setAlignment(Qt.AlignLeft)
        self.nameLabel.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.1); border: none;")

    def editNameResponder(self, e):
        if self.selected and self.track.selected:
            self.nameLabel.setFocus()
            self.nameLabel.selectAll()

    def trackSelectResponder(self, e):
        self.updateStyle()

    def rowSelectResponder(self, e):
        if self.index == e.index:
            self.setSelected(True)
        else:
            self.setSelected(False)
            
    def setSelected(self, value):
        if value:
            self.track.selectedCellIndex = self.index
            self.notify(events.view.track.CellSelected(
                self.track.index, self.index))
        super().setSelected(value)

    def mousePressEvent(self, event):
        self.track.selectRowAt(self.index)
        return super().mousePressEvent(event)

    def onEditingNameFinished(self):
        self.notify(events.view.track.CellNameChanged(
            self.track.index, self.index, self.name()))
        return super().onEditingNameFinished()

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
