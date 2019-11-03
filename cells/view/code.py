from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWidgets import QDialog
from cells.observation import Observation

class Code(Observation, QDialog):
    def __init__(self, subject, code=None):
        
        self.code = code is not None if code else ""
        
        Observation.__init__(self, subject)
        QDialog.__init__(self)
        
        self.setModal(True)
        
        self.webView = QWebEngineView()
        
    def open(self):
        self.webView.load("http://alestsurko.by")

    def closeEvent(self, event):
        self.delete()
        return super().closeEvent(event)
    
    def delete(self):
        self.unregister()
        self.setParent(None)
        self.deleteLater()