from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QWidget, QMessageBox

from cells import events
from cells.observation import Observation

from .track import Track, Header, Cell


class Editor(Observation, QScrollArea):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        QScrollArea.__init__(self)

        self.setFrameShape(QFrame.NoFrame)

        self.selectedTrackIndex = -1

        self.innerLayout = QHBoxLayout()

        self.innerLayout.setSpacing(0)
        self.innerLayout.setContentsMargins(0, 0, 0, 0)
        self.innerLayout.setAlignment(Qt.AlignLeft)

        widget = QWidget()
        widget.setLayout(self.innerLayout)
        self.setWidget(widget)
        self.setWidgetResizable(True)

        self.add_responder(events.document.Open, self.documentOpenResponder)
        self.add_responder(events.track.New, self.trackNewResponder)
        self.add_responder(events.view.track.Clicked,
                           self.trackClickedResponder)
        self.add_responder(events.view.main.TrackSelectLeft,
                           self.trackSelectLeftResponder)
        self.add_responder(events.view.main.TrackSelectRight,
                           self.trackSelectRightResponder)
        self.add_responder(events.view.main.TrackMoveLeft,
                           self.trackMoveLeftResponder)
        self.add_responder(events.view.main.TrackMoveRight,
                           self.trackMoveRightResponder)
        self.add_responder(events.view.main.TrackRemove,
                           self.trackRemoveResponder)
        self.add_responder(events.view.track.CellSelected,
                           self.cellSelectedResponder)

    def documentOpenResponder(self, e):
        self.clear()

        for (n, track) in enumerate(e.document.tracks):
            trackView = Track(self.subject, n, track.name)
            for cell in track.cells:
                newCell = trackView.addCell(False)
                newCell.setName(cell.name)
            self.innerLayout.addWidget(trackView)

    def trackClickedResponder(self, e):
        self.selectTrackAt(e.index)

    def trackSelectLeftResponder(self, e):
        if self.numOfTracks() < 1:
            return

        if not self.isThereSelectedTrack():
            self.selectTrackAt(self.numOfTracks() - 1)
        else:
            self.selectTrackAt(self.selectedTrackIndex - 1)

    def trackSelectRightResponder(self, e):
        if self.numOfTracks() < 1:
            return

        if not self.isThereSelectedTrack():
            self.selectTrackAt(0)
        else:
            self.selectTrackAt(self.selectedTrackIndex + 1)

    def trackNewResponder(self, e):
        length = self.innerLayout.count()
        name = "Track " + str(length + 1)
        track = Track(self.subject, length, name)
        if self.numOfTracks() > 0:
            firstTrack = self.innerLayout.itemAt(0).widget()
            for cell in firstTrack.cells:
                new_cell = track.addCell()
                new_cell.setSelected(cell.selected)
        self.innerLayout.addWidget(track)

    def trackMoveLeftResponder(self, e):
        self.moveSelectedTrackTo(self.selectedTrackIndex - 1)

    def trackMoveRightResponder(self, e):
        self.moveSelectedTrackTo(self.selectedTrackIndex + 1)

    def moveSelectedTrackTo(self, index):
        if self.numOfTracks() < 1 or \
                not self.isThereSelectedTrack() or \
                not index in range(self.numOfTracks()) or \
                self.selectedTrackIndex == index:
            return

        track = self.innerLayout.takeAt(self.selectedTrackIndex)
        self.innerLayout.insertWidget(index, track.widget())
        track.widget().setIndex(index)

        previous = self.innerLayout.itemAt(self.selectedTrackIndex)
        previous.widget().setIndex(self.selectedTrackIndex)

        self.notify(events.view.track.Move(self.selectedTrackIndex, index))

        self.selectTrackAt(index)

    def trackRemoveResponder(self, e):
        if not self.isThereSelectedTrack():
            return

        track = self.innerLayout.itemAt(self.selectedTrackIndex).widget()
        msgBox = self.initConfirmDelete(track.name())
        reply = msgBox.exec_()

        if reply == QMessageBox.Yes:
            track.setParent(None)
            self.notify(events.view.track.Remove(self.selectedTrackIndex))
            self.selectTrackAt(self.selectedTrackIndex-1)
            for n in range(self.selectedTrackIndex+1, self.numOfTracks()):
                track = self.innerLayout.itemAt(n).widget()
                track.setIndex(track.index - 1)

    def cellSelectedResponder(self, e):
        self.ensureTrackVisible(self.selectedTrackIndex)

    def selectTrackAt(self, index):
        if self.selectedTrackIndex == index:
            return

        if self.isThereSelectedTrack():
            track = self.innerLayout.itemAt(self.selectedTrackIndex)
            track.widget().setSelected(False)

        if index in range(self.numOfTracks()):
            track = self.innerLayout.itemAt(index)
            track.widget().setSelected(True)
            self.ensureTrackVisible(index)

        self.selectedTrackIndex = min(max(-1, index), self.numOfTracks())
        self.notify(events.view.track.Select(self.selectedTrackIndex))

    def ensureTrackVisible(self, index):
        if index not in range(self.numOfTracks()):
            return

        track = self.innerLayout.itemAt(index).widget()

        if track.selectedCellIndex in range(len(track.cells)):
            cell = track.cells[track.selectedCellIndex]
            self.ensureWidgetVisible(
                cell, track.header.width(), track.header.height())
        else:
            self.ensureWidgetVisible(
                track, track.header.width(), track.header.height())

    def isThereSelectedTrack(self):
        return self.selectedTrackIndex in range(self.numOfTracks())

    def numOfTracks(self):
        return self.innerLayout.count()

    def clear(self):
        for i in reversed(range(self.numOfTracks())):
            self.innerLayout.itemAt(i).widget().setParent(None)

    def initConfirmDelete(self, name):
        question = f'Do you really want to delete track {name}?'
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Delete Track")
        msgBox.setText(question)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)

        return msgBox
