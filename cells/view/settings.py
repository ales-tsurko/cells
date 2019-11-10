import os
import glob

from PySide2.QtWidgets import (QDialog, QVBoxLayout,
                               QDialogButtonBox, QTabWidget, QWidget,
                               QFormLayout, QComboBox)
from PySide2.QtCore import Qt
from cells.observation import Observation
from cells.settings import Settings as SettingsModel
import cells.utility as utility
from .code import acePropertyNames


class Settings(Observation, QDialog):
    def __init__(self, subject, settings):
        Observation.__init__(self, subject)
        QDialog.__init__(self)

        self.model = settings
        self.model.open()

        self.setWindowTitle("Settings")
        self.setFixedSize(300, 300)
        self.setModal(True)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        self._initTabs()
        self._initButtons()

    def _initTabs(self):
        tabbed = QTabWidget()
        self.editor = EditorPage(self.model['editor'])
        tabbed.addTab(self.editor, "Editor")
        self.layout().addWidget(tabbed)

    def _initButtons(self):
        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).clicked.connect(self.onOkClicked)
        buttons.button(QDialogButtonBox.Cancel).clicked.connect(
            self.onCancelClicked)
        self.layout().addWidget(buttons)

    def onOkClicked(self, e):
        self.save()
        self.close()

    def onCancelClicked(self, e):
        self.close()

    def deserialize(self, model):
        pass

    def save(self):
        self.editor.save()
        self.model.save()

    def closeEvent(self, arg__1):
        self.unregister()
        self.setParent(None)
        self.deleteLater()
        return super().closeEvent(arg__1)


class EditorPage(QWidget):
    def __init__(self, model):
        self.model = model

        super().__init__()

        layout = QFormLayout()
        self.setLayout(layout)

        self._initThemeChooser()
        self._initKeybindingsChooser()

        self.deserialize(self.model)

    def _initThemeChooser(self):
        self.theme = QComboBox()
        [self.theme.addItem(theme) for theme in self._themes()]
        self.layout().addRow(self.tr("Theme:"), self.theme)

    def _initKeybindingsChooser(self):
        self.kb = QComboBox()
        [self.kb.addItem(kb) for kb in self._keybindings()]
        self.layout().addRow(self.tr("Keybindings:"), self.kb)

    def _themes(self):
        return acePropertyNames("theme-", ".js")

    def _keybindings(self):
        return acePropertyNames("keybinding-", ".js")

    def deserialize(self, model):
        self.theme.setCurrentText(model.get("theme"))
        self.kb.setCurrentText(model.get("keybindings"))

    def save(self):
        self.model["theme"] = self.theme.currentText()
        self.model["keybindings"] = self.kb.currentText()
