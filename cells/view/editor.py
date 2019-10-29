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
        self.add_responder(events.document.Load, self.document_load_responder)

    def track_new_responder(self, e):
        track = Track(self.subject)
        track.setName("Track " + str(self.innerLayout.count() + 1))
        self.innerLayout.addWidget(track)

    def document_load_responder(self, e):
        for i in reversed(range(self.innerLayout.count())):
            self.innerLayout.itemAt(i).widget().deleteLater()

        for track in e.document.tracks:
            track_view = Track(self.subject)
            track_view.setName(track['name'])
            self.innerLayout.addWidget(track_view)
