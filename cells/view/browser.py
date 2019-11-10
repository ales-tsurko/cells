from copy import deepcopy

from PySide2.QtWidgets import (QListWidget, QListWidgetItem, QWidget,
                               QFrame, QLabel, QVBoxLayout, QMenu,
                               QAction)
from PySide2.QtCore import Qt

from cells.observation import Observation

from cells import events
from cells.model import TrackTemplateManager
from .dialogs import ConfirmationDialog
from .track_editor import TrackEditor


class Browser(Observation, QListWidget):
    def __init__(self, document, subject, powermode=False):
        self.templateManager = TrackTemplateManager(document, subject)

        Observation.__init__(self, subject)
        QListWidget.__init__(self)
        self.templateEditor = TrackEditor(self.subject)
        self.templateEditor.onTemplateUpdate = self.onTemplateUpdate

        self.setStyleSheet("border: 0;")
        self.setFrameStyle(QFrame.NoFrame | QFrame.Plain)
        self.setMaximumWidth(250)
        self.setMinimumWidth(165)

        self._initActions()

        [self.addTemplate(t) for t in self.templateManager.templates]

        self.add_responder(events.track.TrackTemplateSaved,
                           self.trackTemplateSavedResponder)

    def _initActions(self):
        # as far as ownership of actions isn't transfered
        # to add action, we need to keep them by reference counter,
        # so we make them attributes
        self._newTrackAct = QAction("New Track")
        self._newTrackAct.setShortcut(self.tr("Return"))
        self._newTrackAct.triggered.connect(self.onTrackNewFromTemplate)
        self._newTrackAct.setShortcutContext(Qt.WidgetShortcut)

        self._deleteAct = QAction("Delete")
        self._deleteAct.setShortcut(self.tr("Alt+Backspace"))
        self._deleteAct.triggered.connect(self.onTemplateDelete)
        self._deleteAct.setShortcutContext(Qt.WidgetShortcut)

        self._editAct = QAction("Edit")
        self._editAct.triggered.connect(self.onTemplateEdit)
        # self._editAct.setShortcutContext(Qt.WidgetShortcut)

        self.addActions([self._newTrackAct, self._deleteAct, self._editAct])

    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.addActions(self.actions())
        menu.exec_(event.globalPos())

    def onTrackNewFromTemplate(self, e):
        if not self.currentItem():
            return

        template = self.templateManager.templates[self.currentRow()]
        self.notify(events.view.browser.TrackNewFromTemplate(deepcopy(template)))

    def onTemplateDelete(self, e):
        if not self.currentItem():
            return

        item = self.currentItem()
        name = self.itemWidget(item).template.backend_name

        confirmation = ConfirmationDialog(
            "Delete Track Template",
            f"Do you really want to delete {name} track template?")
        if confirmation.exec_() == ConfirmationDialog.Yes:
            self.templateManager.delete_at(self.currentRow())
            self.takeItem(self.currentRow())

    def onTemplateEdit(self, e):
        if not self.currentItem():
            return

        template = self.templateManager.templates[self.currentRow()]
        self.templateEditor.setTemplate(template)
        self.templateEditor.show()

    def onTemplateUpdate(self):
        if not self.currentItem():
            return

        template = self.templateManager.templates[self.currentRow()]
        itemWidget = self.itemWidget(self.currentItem())
        itemWidget.deserialize(template)
        self.templateManager.save(template, template.path, False)

    def addTemplate(self, template):
        item = QListWidgetItem()
        view = Item(template, self.subject)
        item.setSizeHint(view.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, view)

    def trackTemplateSavedResponder(self, e):
        self.addTemplate(e.template)

    def delete(self):
        self.templateEditor.delete()
        self.unregister()
        self.setParent(None)
        self.deleteLater()

    def closeEvent(self, e):
        self.delete()


class Item(Observation, QWidget):
    def __init__(self, template, subject):
        Observation.__init__(self, subject)
        QWidget.__init__(self)
        self.maxLineLen = 35
        self.template = template

        name = self.shortenString(template.backend_name)
        description = self.shortenString(template.description)
        runCommand = self.shortenString(template.run_command)

        self.name = QLabel(name, wordWrap=True)
        self.command = QLabel(runCommand, wordWrap=True)
        self.description = QLabel(description, wordWrap=True)

        layout = QVBoxLayout()

        layout.setSpacing(3)
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.name)
        layout.addWidget(self.command)
        layout.addWidget(self.description)

        self.setLayout(layout)

    def shortenString(self, value):
        if len(value) <= self.maxLineLen:
            return value
        return value[:self.maxLineLen] + "..."

    def deserialize(self, template):
        self.name.setText(self.shortenString(template.backend_name))
        self.command.setText(self.shortenString(template.run_command))
        self.description.setText(self.shortenString(template.description))
