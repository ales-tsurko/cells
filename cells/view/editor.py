from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QWidget, QMessageBox

from cells import events
from cells.observation import Observation

from .track import Track, Header


class Editor(Observation, QScrollArea):
    def __init__(self, subject):
        Observation.__init__(self, subject)
        QScrollArea.__init__(self)

        self.setFrameShape(QFrame.NoFrame)

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
        self.add_responder(events.view.track.Select, self.trackSelectResponder)
        self.add_responder(events.view.track.Move,
                           self.trackMoveResponder)
        self.add_responder(events.view.track.WillRemove, self.trackRemoveResponder)

    def documentOpenResponder(self, e):
        self.clear()

        for (n, track) in enumerate(e.document.tracks):
            track_view = Track(self.subject, n, track.name)
            self.innerLayout.addWidget(track_view)

    def trackNewResponder(self, e):
        length = self.innerLayout.count()
        name = "Track " + str(length + 1)
        track = Track(self.subject, length, name)
        self.innerLayout.addWidget(track)

    def trackSelectResponder(self, e):
        track = self.innerLayout.itemAt(e.index).widget()
        track.setFocus()

    def trackMoveResponder(self, e):
        track = self.innerLayout.takeAt(e.index)
        self.innerLayout.insertWidget(e.new_index, track.widget())

    def trackRemoveResponder(self, e):
        track = self.innerLayout.itemAt(e.index).widget()
        msgBox = self.initConfirmDelete(track.name())
        reply = msgBox.exec_()

        if reply == QMessageBox.Yes:
            self.innerLayout.removeWidget(track)
            track.close()
            self.notify(events.view.track.Remove(e.index))
            self.setFocusToTrack(e.index-1)
            for n in range(e.index, self.innerLayout.count()):
                track = self.innerLayout.itemAt(n).widget()
                track.setIndex(track.index - 1)

    def clear(self):
        for i in reversed(range(self.innerLayout.count())):
            self.innerLayout.itemAt(i).widget().deleteLater()

    def initConfirmDelete(self, name):
        question = f'Do you really want to delete track {name}?'
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Delete Track")
        msgBox.setText(question)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)

        return msgBox

    def setFocusToTrack(self, index):
        track = self.innerLayout.itemAt(index)
        if track is not None:
            track.widget().setFocus()