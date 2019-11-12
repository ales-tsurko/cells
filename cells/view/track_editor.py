from PySide2.QtCore import Qt
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (QComboBox, QFormLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPlainTextEdit, QShortcut,
                               QVBoxLayout, QWidget)

from cells.observation import Observation

from .code import CodeDelegate, CodeView, acePropertyNames


class FinalMeta(type(QWidget), type(CodeDelegate)):
    pass


class TrackEditor(Observation, QWidget, metaclass=FinalMeta):
    def __init__(self, subject, powermode=False, allowEditBackend=False):
        Observation.__init__(self, subject)
        QWidget.__init__(self)

        self._template = None
        self.powermode = powermode
        self.allowEditBackend = allowEditBackend
        self.descriptionMaxLen = 500

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        if self.allowEditBackend:
            self._initForm()
        self._initCodeEditor()

        self.setFixedSize(630, 600)

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

            self.commandPrompt = QLineEdit(self, maxLength=100)
            self.commandPrompt.setToolTip("regex")
            self.commandPrompt.textChanged.connect(
                self.onPromptIndicatorChanged)

            self.editorMode = QComboBox()
            [self.editorMode.addItem(mode) for mode in self._availableModes()]
            self.editorMode.currentIndexChanged.connect(
                self.onEditorModeChanged)

            self.stdinRegex = QLineEdit(self, maxLength=100)
            self.stdinRegex.setToolTip("regex")
            self.stdinRegex.textChanged.connect(self.onStdinRegexChanged)
            self.stdinReplace = QLineEdit(self, maxLength=100)
            self.stdinReplace.setToolTip("substitution string")
            self.stdinReplace.textChanged.connect(self.onStdinReplaceChanged)

            self.stdoutRegex = QLineEdit(self, maxLength=100)
            self.stdoutRegex.setToolTip("regex")
            self.stdoutRegex.textChanged.connect(self.onStdoutRegexChanged)
            self.stdoutReplace = QLineEdit(self, maxLength=100)
            self.stdoutReplace.setToolTip("substitution string")
            self.stdoutReplace.textChanged.connect(self.onStdoutReplaceChanged)

            self.description = QPlainTextEdit(self, fixedHeight=100)

        layout.addRow(self.tr("Run Command:"), self.runCommand)

        if self.powermode:
            layout.addRow(self.tr("Backend Name:"), self.backendName)
            layout.addRow(self.tr("Command Prompt (Regex):"),
                          self.commandPrompt)
            layout.addRow(self.tr("Editor Mode:"), self.editorMode)

            stdinMiddlewareLayout = QHBoxLayout()
            stdinMiddlewareLayout.addWidget(self.stdinRegex)
            stdinMiddlewareLayout.addWidget(self.stdinReplace)
            layout.addRow(self.tr("Stdin Middleware:"), stdinMiddlewareLayout)

            stdoutMiddlewareLayout = QHBoxLayout()
            stdoutMiddlewareLayout.addWidget(self.stdoutRegex)
            stdoutMiddlewareLayout.addWidget(self.stdoutReplace)
            layout.addRow(self.tr("Stdout Middleware:"),
                          stdoutMiddlewareLayout)

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
        if self._template is not None:
            self._template.backend_name = e.strip()

    def onRunCommandChanged(self, e):
        if self._template is not None:
            self._template.run_command = e.strip()

    def onPromptIndicatorChanged(self, e):
        if self._template is not None:
            self._template.command_prompt = e.strip()

    def onEditorModeChanged(self, e):
        mode = self.editorMode.itemText(e)
        self.codeView.setMode(mode)

        if self._template is not None:
            self._template.editor_mode = mode

    def onStdinRegexChanged(self, e):
        if self._template is not None:
            self._template.backend_middleware.stdin.regex = e.strip()

    def onStdinReplaceChanged(self, e):
        if self._template is not None:
            self._template.backend_middleware.stdin.substitution = e

    def onStdoutRegexChanged(self, e):
        if self._template is not None:
            self._template.backend_middleware.stdout.regex = e.strip()

    def onStdoutReplaceChanged(self, e):
        if self._template is not None:
            self._template.backend_middleware.stdout.substitution = e

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

        if self.allowEditBackend:
            self.runCommand.setText(self._template.run_command.strip())

        if self.powermode and self.allowEditBackend:
            self.backendName.setText(self._template.backend_name.strip())
            self.commandPrompt.setText(self._template.command_prompt.strip())
            self.editorMode.setCurrentText(self._template.editor_mode)
            self.stdinRegex.setText(
                self._template.backend_middleware.stdin.regex)
            self.stdinReplace.setText(
                self._template.backend_middleware.stdin.substitution)
            self.stdoutRegex.setText(
                self._template.backend_middleware.stdout.regex)
            self.stdoutReplace.setText(
                self._template.backend_middleware.stdout.substitution)
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
        super().showEvent(event)

    def closeEvent(self, event):
        if self._template is not None and \
                self.powermode and \
                self.allowEditBackend:
            self._template.description = self.description.toPlainText(
            )[:self.descriptionMaxLen]

        self.codeView.close()
        super().closeEvent(event)
