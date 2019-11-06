import os
import glob
from abc import ABC, abstractmethod

from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWidgets import QShortcut, QAction
from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QKeySequence
from cells.observation import Observation
from cells import events
import cells.utility as utility
from cells.settings import Settings


class CodeView(Observation, QWebEngineView):
    def __init__(self, subject, delegate=None):
        self.delegate = delegate

        Observation.__init__(self, subject)
        QWebEngineView.__init__(self)
        self.settings = Settings(subject)
        self.settings.open()

        page = Ace(delegate, subject)
        self.setPage(page)
        self.setMinimumSize(500, 300)

        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setWindowModality(Qt.ApplicationModal)

        self.page().loadFinished.connect(self.onLoadFinished)
        self.setWindowFlags(Qt.Tool | Qt.WindowTitleHint | Qt.CustomizeWindowHint |
                            Qt.WindowCloseButtonHint | Qt.WindowMaximizeButtonHint)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)

        self.closeShortcut = QShortcut(
            QKeySequence(self.tr("Ctrl+w")), self, self.close)

        self.add_responder(events.settings.Save, self.settingsSaveResponder)

    def onLoadFinished(self, ok):
        self.loadDelegate()
        self.loadSettings()

    def settingsSaveResponder(self, e):
        self.settings = e.settings
        self.loadSettings()

    def setDelegate(self, delegate):
        self.delegate = delegate
        self.page().delegate = delegate
        self.setWindowTitle(self.delegate.codeWindowTitle())
        self.loadDelegate()

    def loadDelegate(self):
        if self.delegate is None:
            return

        if len(self.delegate.code()) < 1:
            self.setCodeAsync(self.tip())
            self.page().runJavaScript("editor.selectAll();")
        else:
            self.setCodeAsync(self.delegate.code())
        self.page().runJavaScript("editor.focus();")

    def setTheme(self, name):
        aceName = self.asAceProperty(name)
        self.page().runJavaScript(f"editor.setTheme('ace/theme/{aceName}');")

    def setKeybindings(self, name):
        aceName = self.asAceProperty(name)
        self.page().runJavaScript(
            f"editor.setKeyboardHandler('ace/keyboard/{aceName}');")

    def setMode(self, name):
        aceName = self.asAceProperty(name)
        self.page().runJavaScript(
            f"editor.session.setMode('ace/mode/{aceName}');")

    def asAceProperty(self, name):
        return name.lower().replace(" ", "_")

    def setCodeAsync(self, code):
        self.page().runJavaScript(
            f"editor.session.setValue({repr(code)});")

    def postContent(self):
        self.page().runJavaScript(
            f"console.log('{Token.getContent}' + editor.getValue());")

    def tip(self):
        return "Shift+Enter    - evaluate line or selection\n" +\
               "Ctrl/Cmd+Enter - evaluate the whole buffer\n" +\
               "Ctrl/Cmd+W     - close the editor\n" +\
               "Ctrl/Cmd+Alt+H - view all shortcuts"

    def loadSettings(self):
        self.setTheme(self.settings['editor'].get('theme'))
        self.setKeybindings(self.settings['editor'].get('keybindings'))

    def delete(self):
        self.page().unregister()
        self.page().setParent(None)
        self.page().deleteLater()
        self.unregister()
        self.setParent(None)
        self.deleteLater()

    def closeEvent(self, event):
        self.postContent()
        return super().closeEvent(event)


class Ace(Observation, QWebEnginePage):
    def __init__(self, delegate, subject):
        self.delegate = delegate

        QWebEnginePage.__init__(self)
        Observation.__init__(self, subject)

        aceUrl = QUrl.fromLocalFile(os.path.join(
            utility.viewResourcesDir(), "ace", "index.html"))
        self.load(aceUrl)
        # I'd like to move all the python<->js communication here
        # but when I'm starting to implement something more than just
        # virtual functions, I get:
        # ERROR:mach_port_broker.mm(193)] Unknown process  is sending Mach IPC messages!
        # so here is implementations of callbacks only

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        self.parseConsoleOutput(message)

    def parseConsoleOutput(self, message):
        if self.delegate is None:
            return

        if message.startswith(Token.evaluate):
            self.evaluate(message[len(Token.evaluate):])
        elif message.startswith(Token.getContent):
            self.getContent(message[len(Token.getContent):])

    def evaluate(self, code):
        self.notify(events.view.code.Evaluate(code))

    def getContent(self, content):
        self.delegate is not None and self.delegate.setCode(content, True)


class Token:
    evaluate = "<-!code_evaluation_triggered!->"
    getContent = "<-!get_content_triggered!->"


class CodeDelegate(ABC):

    @abstractmethod
    def setCode(self, code, notify):
        pass

    @abstractmethod
    def code(self):
        return ""

    @abstractmethod
    def codeWindowTitle(self):
        return ""


def aceSrcDir():
    return os.path.join(
        utility.viewResourcesDir(), "ace", "ace-builds", "src")


def acePropertyNames(prefix, postfix, title=True):
    themesDir = aceSrcDir()
    names = sorted(glob.glob(os.path.join(
        themesDir, prefix + "*" + postfix)))
    names = [os.path.basename(name) for name in names]
    names = [name[len(prefix):-len(postfix)].replace("_", " ")
             for name in names]
    if title:
        names = [name.title() for name in names]

    return names
