from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QWidget, QMessageBox

from cells import events
from cells.observation import Observation

from .track import Track
from .dialogs import ConfirmationDialog


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
        self.add_responder(events.view.main.TrackNew, self.trackNewResponder)
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
        self.add_responder(events.view.main.RowRemove,
                           self.rowRemoveResponder)
        self.add_responder(events.view.track.CellSelected,
                           self.cellSelectedResponder)

    def documentOpenResponder(self, e):
        self.clear()

        for (n, track) in enumerate(e.document.tracks):
            trackView = Track(self, self.subject, n, track.name)
            for cell in track.cells:
                newCell = trackView.addCell(False)
                newCell.setName(cell.name)
            self.innerLayout.addWidget(trackView)

    def trackClickedResponder(self, e):
        self.selectTrackAt(e.index)

    def trackSelectLeftResponder(self, e):
        if self.numOfTracks() < 1:
            return

        if not self.hasSelectedTrack():
            self.selectTrackAt(self.numOfTracks() - 1)
        else:
            self.selectTrackAt(self.selectedTrackIndex - 1)

    def trackSelectRightResponder(self, e):
        if self.numOfTracks() < 1:
            return

        if not self.hasSelectedTrack():
            self.selectTrackAt(0)
        else:
            self.selectTrackAt(self.selectedTrackIndex + 1)

    def trackNewResponder(self, e):
        length = self.innerLayout.count()
        name = "Track " + str(length + 1)
        track = Track(self, self.subject, length, name)
        self.innerLayout.addWidget(track)
        self.notify(events.view.track.New(name))

        if self.numOfTracks() > 0:
            firstTrack = self.trackAt(0)
            for cell in firstTrack.cells:
                new_cell = track.addCell()
                new_cell.setSelected(cell.selected)

    def trackMoveLeftResponder(self, e):
        self.moveSelectedTrackTo(self.selectedTrackIndex - 1)

    def trackMoveRightResponder(self, e):
        self.moveSelectedTrackTo(self.selectedTrackIndex + 1)

    def moveSelectedTrackTo(self, index):
        if self.numOfTracks() < 2 or \
                not self.hasSelectedTrack() or \
                not index in range(self.numOfTracks()) or \
                self.selectedTrackIndex == index:
            return

        track = self.innerLayout.takeAt(self.selectedTrackIndex)
        self.innerLayout.insertWidget(index, track.widget())
        track.widget().setIndex(index)

        previous = self.trackAt(self.selectedTrackIndex)
        previous.setIndex(self.selectedTrackIndex)

        self.notify(events.view.track.Move(self.selectedTrackIndex, index))

        self.selectTrackAt(index)

    def trackRemoveResponder(self, e):
        if not self.hasSelectedTrack():
            return

        track = self.trackAt(self.selectedTrackIndex)
        question = f'Do you really want to delete track {track.name()}?'
        confirmation = ConfirmationDialog("Delete Track", question)

        if confirmation.exec_() == QMessageBox.No:
            return

        track.delete()
        self.notify(events.view.track.Remove(self.selectedTrackIndex))
        self.selectTrackAt(self.selectedTrackIndex-1)
        for n in range(self.selectedTrackIndex+1, self.numOfTracks()):
            track = self.trackAt(n)
            track.setIndex(track.index - 1)

    def rowRemoveResponder(self, e):
        if not self.hasSelectedTrack():
            return

        track = self.trackAt(self.selectedTrackIndex)

        if not track.isThereSelectedCell() or len(track.cells) < 1:
            return

        confirmation = ConfirmationDialog(
            "Row Deletion", "Do you really want to delete this row?")
        if confirmation.exec_() == QMessageBox.No:
            return

        self.notify(events.view.track.RowRemove(track.selectedCellIndex))
        track.selectRowAt(track.selectedCellIndex - 1)

    def cellSelectedResponder(self, e):
        self.ensureTrackVisible(self.selectedTrackIndex)

    def selectTrackAt(self, index):
        if self.selectedTrackIndex == index:
            return

        if self.hasSelectedTrack():
            track = self.trackAt(self.selectedTrackIndex)
            track.setSelected(False)

        if index in range(self.numOfTracks()):
            track = self.trackAt(index)
            track.setSelected(True)
            self.ensureTrackVisible(index)

        self.selectedTrackIndex = min(max(-1, index), self.numOfTracks())
        self.notify(events.view.track.Select(self.selectedTrackIndex))

    def ensureTrackVisible(self, index):
        if index not in range(self.numOfTracks()):
            return

        track = self.trackAt(index)

        if track.selectedCellIndex in range(len(track.cells)):
            cell = track.cells[track.selectedCellIndex]
            self.ensureWidgetVisible(
                cell, track.header.width(), track.header.height())
        else:
            self.ensureWidgetVisible(
                track, track.header.width(), track.header.height())

    def hasSelectedTrack(self):
        return self.selectedTrackIndex in range(self.numOfTracks())

    def numOfTracks(self):
        return self.innerLayout.count()

    def clear(self):
        for i in reversed(range(self.numOfTracks())):
            self.trackAt(i).setParent(None)

    def trackAt(self, index):
        return self.innerLayout.itemAt(index).widget()
    
    def closeEvent(self, e):
        self.unregister()
        return super().closeEvent(e)
