from PySide2.QtWidgets import QMessageBox

class ConfirmationDialog(QMessageBox):
    def __init__(self, title, message, hasCancel=False):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        buttons = QMessageBox.Yes | QMessageBox.No
        if hasCancel:
            buttons |= QMessageBox.Cancel
        self.setStandardButtons(buttons)
        self.setDefaultButton(QMessageBox.Yes)