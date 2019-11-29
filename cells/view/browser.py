from copy import deepcopy

from cells import events
from cells.model import TrackTemplateManager
from cells.observation import Observation
from PySide2.QtCore import Qt
from PySide2.QtSvg import QSvgWidget
from PySide2.QtWidgets import (QAction, QFrame, QHBoxLayout, QLabel,
                               QListWidget, QListWidgetItem, QMenu, QTextEdit,
                               QVBoxLayout, QWidget)

from .dialogs import ConfirmationDialog
from .theme import ScrollBar, Theme
from .track_editor import TrackEditor


class Browser(QWidget):
    def __init__(self, document, subject, powermode=False):
        super().__init__()
        self.document = document
        self.subject = subject
        self.powermode = powermode

        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("border: 0;")
        self.setFixedWidth(Theme.browser.width)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        self._initList()
        self._initDescription()

    def _initList(self):
        self.listView = BrowserList(self, self.document, self.subject,
                                    self.powermode)
        self.layout().addWidget(self.listView)

    def _initDescription(self):
        self.templateInfo = TemplateInfo()
        self.layout().addWidget(self.templateInfo)

    def onSelectionChanged(self, template):
        self.templateInfo.setTemplate(template)

    def delete(self):
        self.listView.delete()

    def closeEvent(self, e):
        self.delete()


class TemplateInfo(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(Theme.browser.info.height)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet(Theme.browser.info.style)

        self._initName()
        self._initDescription()

    def _initName(self):
        self.name = QLabel()
        self.name.setWordWrap(True)
        self.name.setStyleSheet(Theme.browser.info.headerStyle)
        self.name.setFont(Theme.browser.info.headerFont)
        self.layout().addWidget(self.name)

    def _initDescription(self):
        self.description = QTextEdit()
        self.description.setReadOnly(True)
        self.description.setVerticalScrollBar(ScrollBar())
        self.description.setStyleSheet(Theme.browser.info.textAreaStyle)
        self.description.setFont(Theme.browser.info.textAreaFont)
        self.description.setTextColor(Theme.browser.info.textAreaFontColor)
        self.layout().addWidget(self.description)

    def setTemplate(self, template):
        if template is None:
            self.name.setText("")
            self.description.setText("")
        else:
            self.name.setText(template.backend_name)
            self.description.setText(template.description)

        self.name.adjustSize()
        self.description.adjustSize()


class BrowserList(Observation, QListWidget):
    def __init__(self, delegate, document, subject, powermode=False):
        self.templateManager = TrackTemplateManager(document, subject)
        self.delegate = delegate
        self.powermode = powermode

        Observation.__init__(self, subject)
        QListWidget.__init__(self)

        self.setStyleSheet(Theme.browser.style)
        
        self.templateEditor = TrackEditor(self.subject, self.powermode, True)
        self.templateEditor.onTemplateUpdate = self.onTemplateUpdate


        self.setFrameStyle(QFrame.NoFrame | QFrame.Plain)
        self.setHorizontalScrollBar(ScrollBar())
        self.setVerticalScrollBar(ScrollBar())

        self._initActions()

        [self.addTemplate(t) for t in self.templateManager.templates]

        self.add_responder(events.track.TrackTemplateSaved,
                           self.trackTemplateSavedResponder)

        self.itemSelectionChanged.connect(self.onSelectionChanged)
        self.currentItemChanged.connect(self.onCurrentItemChanged)

    def _initActions(self):
        # as far as ownership of actions isn't transfered
        # to add action, we need to keep them by reference counter,
        # so we make them attributes
        self._newTrackAct = QAction("New Track (Return)")
        self._newTrackAct.setShortcut(self.tr("Return"))
        self._newTrackAct.triggered.connect(self.onTrackNewFromTemplate)
        self._newTrackAct.setShortcutContext(Qt.WidgetShortcut)
        self.addAction(self._newTrackAct)

        if self.powermode:
            self._deleteAct = QAction("Delete (Alt+Backspace)")
            self._deleteAct.setShortcut(self.tr("Alt+Backspace"))
            self._deleteAct.triggered.connect(self.onTemplateDelete)
            self._deleteAct.setShortcutContext(Qt.WidgetShortcut)
            self.addAction(self._deleteAct)

        self._editAct = QAction("Edit")
        self._editAct.triggered.connect(self.onTemplateEdit)
        self.addAction(self._editAct)

    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.setStyleSheet(Theme.contextMenu.style)
        menu.setFont(Theme.contextMenu.font)
        menu.addActions(self.actions())
        menu.exec_(event.globalPos())

    def onTrackNewFromTemplate(self, e):
        if not self.currentItem():
            return

        template = self.templateManager.templates[self.currentRow()]
        self.notify(
            events.view.browser.TrackNewFromTemplate(deepcopy(template)))

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

    def onSelectionChanged(self):
        if not self.currentItem():
            self.delegate.onSelectionChanged(None)

        template = self.templateManager.templates[self.currentRow()]
        self.delegate.onSelectionChanged(template)

        self.itemWidget(self.currentItem()).setSelected(True)

    def onCurrentItemChanged(self, current, previous):
        if previous:
            self.itemWidget(previous).setSelected(False)

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
        self.maxNameLen = 13
        self.maxDescLen = 27
        self.maxCommandLen = 13
        self.template = template

        self.selected = False

        name = self.shortenString(template.backend_name, self.maxNameLen)
        description = self.shortenString(template.description, self.maxDescLen)
        runCommand = self.shortenString(template.run_command, self.maxCommandLen)
        self.setFixedSize(Theme.browser.item.size)

        layout = QVBoxLayout()

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)

        self.setLayout(layout)

        self.__initHeader__(name, runCommand)
        self.__initDescription__(description)

    def __initHeader__(self, name, command):
        hlayout = QHBoxLayout()
        hlayout.setSpacing(0)
        hlayout.setContentsMargins(18, 18, 18, 18)

        self.iconLight = QSvgWidget(self.template.icon_path())
        self.iconLight.setFixedSize(36, 36)
        self.iconDark = QSvgWidget(self.template.icon_path(False))
        self.iconDark.setFixedSize(36, 36)
        self.iconDark.setHidden(True)

        hlayout.addWidget(self.iconLight)
        hlayout.addWidget(self.iconDark)

        vlayout = QVBoxLayout()
        vlayout.setSpacing(0)
        vlayout.setContentsMargins(0, 0, 0, 0)

        self.name = QLabel(name, wordWrap=True)
        self.name.setFont(Theme.browser.item.headerFont)
        self.name.setStyleSheet(Theme.browser.item.headerStyle)
        vlayout.addWidget(self.name)

        self.command = QLabel(command, wordWrap=True)
        self.command.setFont(Theme.browser.item.commandFont)
        self.command.setStyleSheet(Theme.browser.item.commandStyle)
        vlayout.addWidget(self.command)

        hlayout.addLayout(vlayout)

        self.layout().addLayout(hlayout)

    def __initDescription__(self, description):
        self.description = QLabel(description, wordWrap=True)
        self.description.setFont(Theme.browser.item.descriptionFont)
        self.description.setStyleSheet(Theme.browser.item.descriptionStyle)
        self.layout().addWidget(self.description)

    def shortenString(self, value, length):
        lines = value.splitlines()

        if len(lines) < 1:
            return value

        firstLine = lines[0]

        if len(firstLine) <= length:
            return firstLine

        return firstLine[:length] + "..."

    def setSelected(self, selected):
        self.selected = selected
        if self.selected:
            self.name.setStyleSheet(Theme.browser.item.headerStyleSelected)
            self.command.setStyleSheet(Theme.browser.item.commandStyleSelected)
            self.description.setStyleSheet(Theme.browser.item.descriptionStyleSelected)

            self.iconLight.setHidden(True)
            self.iconDark.setHidden(False)
            return

        self.name.setStyleSheet(Theme.browser.item.headerStyle)
        self.command.setStyleSheet(Theme.browser.item.commandStyle)
        self.description.setStyleSheet(Theme.browser.item.descriptionStyle)

        self.iconLight.setHidden(False)
        self.iconDark.setHidden(True)

    def deserialize(self, template):
        self.name.setText(self.shortenString(template.backend_name, self.maxNameLen))
        self.command.setText(self.shortenString(template.run_command, self.maxCommandLen))
        self.description.setText(self.shortenString(template.description, self.maxDescLen))

    def sizeHint(self):
        return Theme.browser.item.size
