from PySide2.QtWidgets import (QListWidget, QListWidgetItem, QWidget,
                               QFrame, QLabel, QVBoxLayout)

from cells.observation import Observation

from cells import events
from cells.model import TrackTemplateManager


class Browser(Observation, QListWidget):
    def __init__(self, document, subject):
        self.templateManager = TrackTemplateManager(document, subject)

        Observation.__init__(self, subject)
        QListWidget.__init__(self)

        self.setStyleSheet("border: 0;")
        self.setFrameStyle(QFrame.NoFrame | QFrame.Plain)
        self.setMaximumWidth(250)
        self.setMinimumWidth(150)

        [self.addTemplate(t) for t in self.templateManager.templates]

        self.add_responder(events.track.TrackTemplateSaved,
                           self.trackTemplateSavedResponder)

    def addTemplate(self, template):
        item = QListWidgetItem()
        # item.setText(template.backend_name)
        view = Item(template, self.subject)
        item.setSizeHint(view.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, view)

    def trackTemplateSavedResponder(self, e):
        self.addTemplate(e.template)

    def delete(self):
        self.unregister()
        self.setParent(None)

    def closeEvent(self, e):
        self.delete()
        return super().closeEvent(e)


class Item(Observation, QWidget):
    def __init__(self, template, subject):
        Observation.__init__(self, subject)
        QWidget.__init__(self)
        self.maxLineLen = 35
        
        name = self.shortenString(template.backend_name)
        description = self.shortenString(template.description)
        runCommand = self.shortenString(template.run_command)
        
        self.name = QLabel(name, wordWrap=True)
        self.command = QLabel(runCommand, wordWrap=True)
        self.description = QLabel(description, wordWrap=True)

        layout = QVBoxLayout()
        layout.addWidget(self.name)
        layout.addWidget(self.command)
        layout.addWidget(self.description)

        self.setLayout(layout)
        
    def shortenString(self, value):
        if len(value) <= self.maxLineLen:
            return value
        return value[:self.maxLineLen] + "..."
