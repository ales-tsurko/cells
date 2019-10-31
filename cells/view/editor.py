from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QWidget

from cells import events
from cells.observation import Observation

from .track import Track


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

        self.add_responder(events.track.New, self.track_new_responder)
        self.add_responder(events.document.New, self.document_new_responder)
        self.add_responder(events.document.Open, self.document_open_responder)

    def track_new_responder(self, e):
        length = self.innerLayout.count()
        name = "Track " + str(length + 1)
        track = Track(self.subject, length, name)
        self.innerLayout.addWidget(track)

    def document_new_responder(self, e):
        self.clear()

    def document_open_responder(self, e):
        self.clear()

        for (n, track) in enumerate(e.document.tracks):
            track_view = Track(self.subject, n, track.name)
            self.innerLayout.addWidget(track_view)

    def clear(self):
        for i in reversed(range(self.innerLayout.count())):
            self.innerLayout.itemAt(i).widget().deleteLater()
