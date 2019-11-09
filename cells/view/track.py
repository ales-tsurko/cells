from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (QAction, QLabel, QLineEdit, QMessageBox,
                               QVBoxLayout, QWidget)

from cells import events
from cells.model import CellModel
from cells.observation import Observation

from .code import CodeDelegate
from .dialogs import ConfirmationDialog


class Track(Observation, QWidget):
    def __init__(self, editor, subject, index, name, template):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self.index = index
        self.selected = False
        self.selectedCellIndex = -1
        self.cells = []
        self._pasteBuffer = None
        self.editor = editor
        self.template = template

        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")

        self.setFixedWidth(200)

        self.header = Header(self, subject)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.header)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignTop)

        self.setName(name)

        self.add_responder(events.view.main.RowAdd, self.rowAddResponder)
        self.add_responder(events.view.main.RowEvaluate,
                           self.rowEvaluateResponder)
        self.add_responder(events.view.main.RowSelectUp,
                           self.rowSelectUpResponder)
        self.add_responder(events.view.main.RowSelectDown,
                           self.rowSelectDownResponder)
        self.add_responder(events.view.track.RowRemove,
                           self.rowRemoveResponder)
        self.add_responder(events.view.main.RowMoveUp, self.rowMoveUpResponder)
        self.add_responder(events.view.main.RowMoveDown,
                           self.rowMoveDownResponder)
        self.add_responder(events.view.main.RowCopy, self.rowCopyResponder)
        self.add_responder(events.view.main.RowCut, self.rowCutResponder)
        self.add_responder(events.view.main.RowPaste, self.rowPasteResponder)
        self.add_responder(events.view.main.CellCopy, self.cellCopyResponder)
        self.add_responder(events.view.main.CellCut, self.cellCutResponder)
        self.add_responder(events.view.main.CellPaste, self.cellPasteResponder)
        self.add_responder(events.view.track.CellClicked,
                           self.cellClickedResponder)

    def rowAddResponder(self, e):
        self.addCell()

    def rowEvaluateResponder(self, e):
        if not self.hasSelectedCell():
            return

        self.cells[self.selectedCellIndex].evaluate()

    def rowSelectUpResponder(self, e):
        if len(self.cells) < 1 or \
                not self.editor.hasSelectedTrack():

            return

        if not self.hasSelectedCell():
            self.selectCellAt(len(self.cells) - 1)
        else:
            self.selectCellAt(self.selectedCellIndex - 1)

    def rowSelectDownResponder(self, e):
        if len(self.cells) < 1 or \
                not self.editor.hasSelectedTrack():

            return

        if not self.hasSelectedCell():
            self.selectCellAt(0)
        else:
            self.selectCellAt(self.selectedCellIndex + 1)

    def rowRemoveResponder(self, e):
        self.removeCellAt(e.index)

    def rowMoveUpResponder(self, e):
        self.moveSelectedCellTo(self.selectedCellIndex - 1)

    def rowMoveDownResponder(self, e):
        self.moveSelectedCellTo(self.selectedCellIndex + 1)

    def rowCopyResponder(self, e):
        if self.editor.hasSelectedTrack():
            self.copySelectedCellIntoBuffer()

    def rowCutResponder(self, e):
        if not self.hasSelectedCell():
            return

        self.rowCopyResponder(e)
        self.removeCellAt(self.selectedCellIndex)
        self.selectCellAt(self.selectedCellIndex)

    def rowPasteResponder(self, e):
        if not self.editor.hasSelectedTrack() or \
                self._pasteBuffer is None:

            return

        cell = self.addCell()
        cell.deserialize(self._pasteBuffer, True)
        pasteIndex = self.selectedCellIndex + 1
        self.selectCellAt(cell.index)
        self.moveSelectedCellTo(pasteIndex)

    def cellCopyResponder(self, e):
        if not self.editor.hasSelectedTrack():
            return

        if (not self.selected and self._pasteBuffer is None) or \
                self.selected:
            self.copySelectedCellIntoBuffer()

    def cellCutResponder(self, e):
        if not self.hasSelectedCell():
            return

        self.cellCopyResponder(e)

        if self.selected:
            self.cells[self.selectedCellIndex].clear(False)

    def cellPasteResponder(self, e):
        if not self.hasSelectedCell() or \
                not self.editor.hasSelectedTrack() or \
                not self.selected or \
                self._pasteBuffer is None:

            return

        cell = self.cells[self.selectedCellIndex]
        cell.deserialize(self._pasteBuffer, True)

    def cellClickedResponder(self, e):
        self.selectCellAt(e.index)

    def addCell(self, notify=True):
        index = len(self.cells)
        cell = Cell(self, self.subject, index)
        cell.setName(str(index + 1))
        self.cells.append(cell)
        self.layout().addWidget(cell)

        if notify:
            self.notify(events.view.track.CellAdd(self.index, cell.name()))

        return cell

    def removeCellAt(self, index):
        if self.selectedCellIndex != index:
            return

        cell = self.cells.pop(index)

        cell.delete()
        self.notify(events.view.track.CellRemove(self.index, index))

        for cell in self.cells[index:]:
            cell.index -= 1
        self.selectCellAt(self.selectedCellIndex)

    def moveSelectedCellTo(self, index):
        if len(self.cells) < 2 or \
                self.selectedCellIndex == index or \
                not self.hasSelectedCell() or \
                not index in range(len(self.cells)) or \
                not self.editor.hasSelectedTrack():

            return
        cell = self.cells.pop(self.selectedCellIndex)
        self.cells.insert(index, cell)
        self.layout().insertWidget(index + 1, cell)
        cell.index = index

        previous = self.cells[self.selectedCellIndex]
        previous.index = self.selectedCellIndex

        self.notify(
            events.view.track.CellMove(self.index, self.selectedCellIndex,
                                       index))
        self.selectedCellIndex = index

    def copySelectedCellIntoBuffer(self):
        if not self.hasSelectedCell():
            return

        self._pasteBuffer = None
        source = self.cells[self.selectedCellIndex]
        self._pasteBuffer = source.serialize()

    def edit(self):
        view = self.editor.trackEditor
        view.setTemplate(self.template)
        view.onTemplateUpdate = self.onTemplateUpdate
        view.show()

    def onTemplateUpdate(self):
        self.notify(
            events.view.track.TemplateUpdated(self.index, self.template))

        confirmation = ConfirmationDialog(
            "Restart Interpreter", "Do you want to restart track's " +
            "interpreter for the changes to " + "take effect?")

        if confirmation.exec_() == QMessageBox.Yes:
            self.notify(
                events.view.track.InterpreterRestart(self.index,
                                                     self.template))

    def saveAsTemplate(self):
        self.notify(events.view.track.SaveAsTemplate(self.template))

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

    def selectCellAt(self, index):
        if self.hasSelectedCell():
            self.cells[self.selectedCellIndex].setSelected(False)

        self.selectedCellIndex = min(max(-1, index), len(self.cells))

        if self.hasSelectedCell():
            self.cells[self.selectedCellIndex].setSelected(True)

    def hasSelectedCell(self):
        return self.selectedCellIndex in range(len(self.cells))

    def delete(self):
        [cell.delete() for cell in self.cells]
        self.header.delete()
        self.unregister()
        self.setParent(None)
        self.deleteLater()

    def deserialize(self, model):
        self.setName(model.name)
        self.template = model.template

        for cell in model.cells:
            newCell = self.addCell(False)
            newCell.deserialize(cell)

    def isPasteBufferEmpty(self):
        return self._pasteBuffer is None

    def fillPasteBuffer(self):
        self._pasteBuffer = CellModel(str(len(self.cells) + 1), "")


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

    def delete(self):
        self.unregister()
        self.setParent(None)
        self.deleteLater()


class Header(CellBase):
    def __init__(self, track, subject):
        super().__init__(subject, track.index)
        self.track = track

        self.add_responder(events.view.main.TrackEditName,
                           self.editNameResponder)

    def onEditingNameFinished(self):
        self.notify(events.view.track.NameChanged(self.index, self.name()))

        return super().onEditingNameFinished()

    def mouseDoubleClickEvent(self, event):
        self.track.edit()

        return super().mouseDoubleClickEvent(event)

    def updateStyle(self):
        if self.selected:
            self.setSelectedStyle()
        else:
            self.setNormalStyle()

    def setSelectedStyle(self):
        self.setStyleSheet("background-color: green;")

    def setNormalStyle(self):
        self.setStyleSheet("background-color: grey;")


class FinalMeta(type(QWidget), type(CodeDelegate)):
    pass


class Cell(CellBase, metaclass=FinalMeta):
    def __init__(self, track, subject, index):
        self.track = track
        self._code = ""

        super().__init__(subject, index)
        self._initContentPreview()

        self.layout().setAlignment(Qt.AlignTop)

        self.add_responder(events.view.main.CellEditName,
                           self.editNameResponder)
        self.add_responder(events.view.track.Select, self.trackSelectResponder)

    def _initNameLabel(self):
        super()._initNameLabel()
        self.nameLabel.setAlignment(Qt.AlignLeft)
        self.nameLabel.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.1); border: none;")

    def _initContentPreview(self):
        self.preview = QLabel()

        font = QFont("Fira Code", 12)
        font.setWeight(QFont.Normal)
        self.preview.setFont(font)
        self.preview.setFocusPolicy(Qt.NoFocus)
        self.preview.setWindowFlags(Qt.FramelessWindowHint)
        self.preview.setStyleSheet("margin: 10;")
        self.preview.setContextMenuPolicy(Qt.NoContextMenu)

        self.layout().addWidget(self.preview)

    def editNameResponder(self, e):
        if self.selected and self.track.selected:
            self.nameLabel.setFocus()
            self.nameLabel.selectAll()

    def trackSelectResponder(self, e):
        self.updateStyle()

    def setSelected(self, value):
        if value:
            self.notify(
                events.view.track.CellSelected(self.track.index, self.index))
        super().setSelected(value)

    def mousePressEvent(self, event):
        self.notify(events.view.track.CellClicked(self.index))

        return super().mousePressEvent(event)

    def onEditingNameFinished(self):
        self.notify(
            events.view.track.CellNameChanged(self.track.index, self.index,
                                              self.name()))

        return super().onEditingNameFinished()

    def evaluate(self):
        self.notify(
            events.view.track.CellEvaluate(self.track.template, self.code()))

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

    def serialize(self):
        return CellModel(self.name(), self.code())

    def deserialize(self, model, notify=False):
        self.setName(model.name)
        self.setCode(model.code)

        if notify:
            self.notify(
                events.view.track.CellNameChanged(self.track.index, self.index,
                                                  model.name))
            self.notify(
                events.view.track.CellCodeChanged(self.track.index, self.index,
                                                  model.code))

    def edit(self):
        view = self.track.editor.codeView
        view.setDelegate(self)
        view.setMode(self.track.template.editor_mode)
        view.show()

    def setCode(self, code, notify=False):
        self._code = code
        self.preview.setText(code)

        if notify:
            self.notify(
                events.view.track.CellCodeChanged(self.track.index, self.index,
                                                  self.code()))

    def code(self):
        return self._code

    def template(self):
        return self.track.template

    def codeWindowTitle(self):
        return self.track.name() + " | " + self.name()

    def clear(self, confirm=True):
        if confirm:
            confirmation = ConfirmationDialog(
                "Clear Cell", "Do you really want to clear the selected cell?")

            if confirmation.exec_() == QMessageBox.No:
                return

        self.setName(str(self.index + 1))
        self.setCode("", True)

        self.notify(
            events.view.track.CellNameChanged(self.track.index, self.index,
                                              self.name()))

    def mouseDoubleClickEvent(self, event):
        self.edit()

        return super().mouseDoubleClickEvent(event)

    def delete(self):
        self.track.editor.codeView.close()

        return super().delete()

    def closeEvent(self, event):
        self.track.editor.codeView.close()

        return super().closeEvent(event)
