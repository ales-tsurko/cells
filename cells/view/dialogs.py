from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMessageBox

from .theme import Theme


class ConfirmationDialog(QMessageBox):
    def __init__(self, title, message, hasCancel=False):
        super().__init__()
        self.setText(title)
        self.setInformativeText(message)
        buttons = QMessageBox.Yes | QMessageBox.No

        if hasCancel:
            buttons |= QMessageBox.Cancel

        self.setStandardButtons(buttons)
        self.setDefaultButton(QMessageBox.Yes)

        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet(Theme.confirmation.style)
