from PySide2.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QWidget
from PySide2.QtCore import Qt

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
        self.innerLayout.setDirection(QHBoxLayout.LeftToRight)
        self.innerLayout.setAlignment(Qt.AlignLeft)

        for n in range(0, 5):
            self.innerLayout.addWidget(Track(subject))

        widget = QWidget()
        widget.setLayout(self.innerLayout)
        self.setWidget(widget)
        self.setWidgetResizable(True)
