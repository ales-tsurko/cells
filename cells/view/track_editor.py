from cells.observation import Observation
from PySide2.QtCore import Qt
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (QComboBox, QFormLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPlainTextEdit, QShortcut,
                               QVBoxLayout, QWidget)

from .code import CodeDelegate, CodeView, acePropertyNames
from .dialogs import ConfirmationDialog
from .theme import Theme


class FinalMeta(type(QWidget), type(CodeDelegate)):
    pass


class TrackEditor(Observation, QWidget, metaclass=FinalMeta):
    def __init__(self,
                 subject,
                 powermode=False,
                 allowEditBackend=False,
                 confirmUpdate=True):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self._template = None
        self.deleted = False
        self.shouldSave = False
        self.powermode = powermode
        self.allowEditBackend = allowEditBackend
        self.confirmUpdate = confirmUpdate
        self.descriptionMaxLen = 1000
        self._code = ""

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        if self.allowEditBackend:
            self._initForm()
        self._initCodeEditor()

        self.setFixedSize(630, 600)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet(Theme.templateEditor.style)

        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setWindowModality(Qt.ApplicationModal)

        self.setWindowFlags(Qt.Tool | Qt.WindowTitleHint
                            | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint
                            | Qt.WindowMaximizeButtonHint)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)

        self.codeView.closeShortcut.setEnabled(False)

        QShortcut(QKeySequence(self.tr("Ctrl+w")), self, self.close)

    def _initForm(self):

        layout = QFormLayout()
        self.runCommand = QLineEdit(self, maxLength=200)
        self.runCommand.setStyleSheet(Theme.templateEditor.inputStyle)
        self.runCommand.setFont(Theme.templateEditor.inputCodeFont)
        self.runCommand.setFixedHeight(Theme.templateEditor.inputHeight)

        if self.powermode:
            self.backendName = QLineEdit(self, maxLength=20)
            self.backendName.setStyleSheet(Theme.templateEditor.inputStyle)
            self.backendName.setFont(Theme.templateEditor.inputFont)
            self.backendName.setFixedHeight(Theme.templateEditor.inputHeight)

            self.editorMode = QComboBox()
            [self.editorMode.addItem(mode) for mode in self._availableModes()]
            self.editorMode.currentIndexChanged.connect(
                self.onEditorModeChanged)

            self.inputRegex = QLineEdit(self, maxLength=100)
            self.inputRegex.setToolTip("regex")
            self.inputRegex.setStyleSheet(Theme.templateEditor.inputStyle)
            self.inputRegex.setFont(Theme.templateEditor.inputCodeFont)
            self.inputRegex.setFixedHeight(Theme.templateEditor.inputHeight)

            self.inputReplace = QLineEdit(self, maxLength=100)
            self.inputReplace.setToolTip("substitution string")
            self.inputReplace.setStyleSheet(Theme.templateEditor.inputStyle)
            self.inputReplace.setFont(Theme.templateEditor.inputCodeFont)
            self.inputReplace.setFixedHeight(Theme.templateEditor.inputHeight)

            self.outputRegex = QLineEdit(self, maxLength=100)
            self.outputRegex.setToolTip("regex")
            self.outputRegex.setStyleSheet(Theme.templateEditor.inputStyle)
            self.outputRegex.setFont(Theme.templateEditor.inputCodeFont)
            self.outputRegex.setFixedHeight(Theme.templateEditor.inputHeight)

            self.outputReplace = QLineEdit(self, maxLength=100)
            self.outputReplace.setToolTip("substitution string")
            self.outputReplace.setStyleSheet(Theme.templateEditor.inputStyle)
            self.outputReplace.setFont(Theme.templateEditor.inputCodeFont)
            self.outputReplace.setFixedHeight(Theme.templateEditor.inputHeight)

            self.description = QPlainTextEdit(self, minimumHeight=80)
            self.description.setStyleSheet(
                Theme.templateEditor.descriptionStyle)
            self.description.setFont(Theme.templateEditor.descriptionFont)

        layout.addRow(self.tr("Run Command:"), self.runCommand)

        if self.powermode:
            layout.addRow(self.tr("Backend Name:"), self.backendName)
            layout.addRow(self.tr("Editor Mode:"), self.editorMode)

            inputMiddlewareLayout = QHBoxLayout()
            inputMiddlewareLayout.addWidget(self.inputRegex)
            inputMiddlewareLayout.addWidget(self.inputReplace)
            layout.addRow(self.tr("Input Middleware:"), inputMiddlewareLayout)

            outputMiddlewareLayout = QHBoxLayout()
            outputMiddlewareLayout.addWidget(self.outputRegex)
            outputMiddlewareLayout.addWidget(self.outputReplace)
            layout.addRow(self.tr("Output Middleware:"),
                          outputMiddlewareLayout)

            layout.addRow(self.tr("Description:"), self.description)

        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        self.layout().addLayout(layout)

    def _initCodeEditor(self):
        self.codeView = CodeView(self.subject, viewTip=False)
        self.layout().addWidget(QLabel("Setup Code:", margin=10))
        self.layout().addWidget(self.codeView)
        self.codeView.setDelegate(self)

    def _availableModes(self):
        return acePropertyNames("mode-", ".js", False)

    def onEditorModeChanged(self, e):
        mode = self.editorMode.itemText(e)
        self.codeView.setMode(mode)

        if self._template is not None:
            self._template.editor_mode = mode

    def onSave(self):
        self.shouldSave = True

        if self.allowEditBackend:
            self._template.run_command = self.runCommand.text().strip()

        if self.powermode and self.allowEditBackend:
            self._template.backend_name = self.backendName.text().strip()

            self._template.editor_mode = self.editorMode.currentText()

            self._template.backend_middleware.input.regex = \
                self.inputRegex.text()
            self._template.backend_middleware.input.substitution = \
                self.inputReplace.text()

            self._template.backend_middleware.output.regex = \
                self.outputRegex.text()
            self._template.backend_middleware.output.substitution = \
                self.outputReplace.text()

            self._template.description = self.description.toPlainText(
            )[:self.descriptionMaxLen]

        self._template.setup_code = self._code

    def setTemplate(self, delegate):
        self._template = delegate
        self.codeView.setDelegate(self)
        self.deserialize()

    def setCode(self, code, notify):
        if self._template is None:
            return

        self._code = code

        if self.shouldSave:
            self._template.setup_code = code
            self.onTemplateUpdate()

    def onTemplateUpdate(self):
        pass

    def code(self):
        if self._template is None:
            return ""

        return self._template.setup_code

    def codeWindowTitle(self):
        return "Track Template Editor"

    def deserialize(self):
        if self._template is None:
            return

        if self.allowEditBackend:
            self.runCommand.setText(self._template.run_command.strip())

        if self.powermode and self.allowEditBackend:
            self.backendName.setText(self._template.backend_name.strip())
            self.editorMode.setCurrentText(self._template.editor_mode)
            self.inputRegex.setText(
                self._template.backend_middleware.input.regex)
            self.inputReplace.setText(
                self._template.backend_middleware.input.substitution)
            self.outputRegex.setText(
                self._template.backend_middleware.output.regex)
            self.outputReplace.setText(
                self._template.backend_middleware.output.substitution)
            self.description.document().setPlainText(
                self._template.description)
        else:
            self.codeView.setMode(self._template.editor_mode)
        self._code = self._template.setup_code

        self.setWindowTitle("Track Template Editor")

    def delete(self):
        self.deleted = True
        self.codeView.delete()
        self.unregister()
        self.setParent(None)
        self.deleteLater()

    def template(self):
        return self._template

    def showEvent(self, event):
        self.shouldSave = False
        self.codeView.show()
        super().showEvent(event)

    def closeEvent(self, event):
        if self._template is not None and not self.deleted:
            if self.confirmUpdate:
                question = "Do you want to save changes in " +\
                        f"{self._template.backend_name} template?"
                confirmation = ConfirmationDialog("Update Track Template",
                                                  question)

                if confirmation.exec_() == ConfirmationDialog.Yes:
                    self.onSave()
            else:
                self.onSave()

        self.codeView.close()
        super().closeEvent(event)
