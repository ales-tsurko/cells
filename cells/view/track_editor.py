from PySide2.QtCore import Qt
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (QComboBox, QFormLayout, QLabel, QLineEdit,
                               QPlainTextEdit, QShortcut, QVBoxLayout, QWidget)

from cells.observation import Observation

from .code import CodeDelegate, CodeView, acePropertyNames


class FinalMeta(type(QWidget), type(CodeDelegate)):
    pass


class TrackEditor(Observation, QWidget, metaclass=FinalMeta):
    def __init__(self, subject, powermode=False):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self._template = None
        self.powermode = powermode
        self.descriptionMaxLen = 500

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._initForm()
        self._initCodeEditor()

        self.setFixedSize(630, 500)

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
        self.runCommand.textChanged.connect(self.onRunCommandChanged)

        if self.powermode:
            self.backendName = QLineEdit(self, maxLength=20)
            self.backendName.textChanged.connect(self.onBackendNameChanged)

            self.commandPrompt = QLineEdit(self, maxLength=20)
            self.commandPrompt.textChanged.connect(
                self.onPromptIndicatorChanged)

            self.editorMode = QComboBox()
            [self.editorMode.addItem(mode) for mode in self._availableModes()]
            self.editorMode.currentIndexChanged.connect(
                self.onEditorModeChanged)

            self.description = QPlainTextEdit(self, fixedHeight=100)

        layout.addRow(self.tr("Run Command:"), self.runCommand)

        if self.powermode:
            layout.addRow(self.tr("Backend Name:"), self.backendName)
            layout.addRow(self.tr("Command Prompt (Regex):"),
                          self.commandPrompt)
            layout.addRow(self.tr("Editor Mode:"), self.editorMode)
            layout.addRow(self.tr("Description:"), self.description)

        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        self.layout().addLayout(layout)

    def _initCodeEditor(self):
        self.codeView = CodeView(self.subject)
        self.layout().addWidget(QLabel("Setup Code:", margin=10))
        self.layout().addWidget(self.codeView)
        self.codeView.setDelegate(self)

    def _availableModes(self):
        return acePropertyNames("mode-", ".js", False)

    def onBackendNameChanged(self, e):
        if self._template is None:
            return

        self._template.backend_name = e.strip()

    def onRunCommandChanged(self, e):
        if self._template is None:
            return

        self._template.run_command = e.strip()

    def onPromptIndicatorChanged(self, e):
        if self._template is None:
            return

        self._template.command_prompt = e.strip()

    def onEditorModeChanged(self, e):
        mode = self.editorMode.itemText(e)
        self.codeView.setMode(mode)

        if self._template is not None:
            self._template.editor_mode = mode

    def setTemplate(self, delegate):
        self._template = delegate
        self.codeView.setDelegate(self)
        self.deserialize()

    def setCode(self, code, notify):
        if self._template is None:
            return

        self._template.setup_code = code
        self.onTemplateUpdate()

    def onTemplateUpdate(self):
        pass

    def code(self):
        if self._template is None:
            return ""

        return self._template.setup_code

    def codeWindowTitle(self):
        return "Track Editor"

    def deserialize(self):
        if self._template is None:
            return

        self.runCommand.setText(self._template.run_command.strip())

        if self.powermode:
            self.backendName.setText(self._template.backend_name.strip())
            self.commandPrompt.setText(self._template.command_prompt.strip())
            self.editorMode.setCurrentText(self._template.editor_mode)
            self.description.document().setPlainText(
                self._template.description)
        else:
            self.codeView.setMode(self._template.editor_mode)

        self.setWindowTitle("Track Editor")

    def delete(self):
        self.codeView.delete()
        self.unregister()
        self.setParent(None)
        self.deleteLater()

    def template(self):
        return self._template

    def showEvent(self, event):
        self.codeView.show()

        return super().showEvent(event)

    def closeEvent(self, event):
        if self._template is not None and self.powermode:
            self._template.description = self.description.toPlainText(
            )[:self.descriptionMaxLen]

        self.codeView.close()

        return super().closeEvent(event)
