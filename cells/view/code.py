import os

from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWidgets import QShortcut
from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QKeySequence
from cells.observation import Observation
from cells import events
import cells.utility as utility


class CodeView(Observation, QWebEngineView):
    def __init__(self, subject, cell=None):
        self.cell = cell

        Observation.__init__(self, subject)
        QWebEngineView.__init__(self)

        page = Ace(cell, subject)
        self.setPage(page)
        self.setMinimumSize(500, 300)

        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setWindowModality(Qt.ApplicationModal)

        self.page().loadFinished.connect(self.onLoadFinished)

        QShortcut(QKeySequence("Alt+Esc"), self, self.close)

    def onLoadFinished(self, ok):
        self.loadCell()

    def setCell(self, cell):
        self.cell = cell
        self.page().cell = cell
        self.loadCell()

    def loadCell(self):
        if self.cell is None:
            return

        if len(self.cell.code()) < 1:
            self.setCodeAsync(self.tip())
            self.page().runJavaScript("editor.selectAll();")
        else:
            self.setCodeAsync(self.cell.code())
        self.page().runJavaScript("editor.focus();")

    def setCodeAsync(self, code):
        self.page().runJavaScript(
            f"editor.session.setValue({repr(code)});")

    def postContent(self):
        self.page().runJavaScript(
            f"console.log('{Token.getContent}' + editor.getValue());")

    def tip(self):
        return "Shift+Enter    - evaluate line or selection\n" +\
               "Ctrl/Cmd+Enter - evaluate the whole buffer\n" +\
               "Alt+Esc        - close the editor\n" +\
               "Ctrl/Cmd+Alt+H - view all shortcuts"

    def paintEvent(self, event):
        return super().paintEvent(event)

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
    def __init__(self, cell, subject):
        self.cell = cell

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
        if message.startswith(Token.evaluate):
            self.evaluate(message[len(Token.evaluate):])
        elif message.startswith(Token.getContent):
            self.getContent(message[len(Token.getContent):])

    def evaluate(self, code):
        self.notify(events.view.code.Evaluate(code))

    def getContent(self, content):
        self.cell is not None and self.cell.setCode(content, True)


class Token:
    evaluate = "<-!code_evaluation_triggered!->"
    getContent = "<-!get_content_triggered!->"
