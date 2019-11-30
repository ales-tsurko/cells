import os

import cells.utility as utility
from PySide2.QtCore import QSize
from PySide2.QtGui import QColor, QFont, QFontDatabase
from PySide2.QtWidgets import QScrollBar


class Fonts:
    def initDb():
        monoRegular = os.path.join(utility.viewResourcesDir(), "fonts",
                                   "FiraCode_2", "FiraCode-Regular.ttf")
        monoLight = os.path.join(utility.viewResourcesDir(), "fonts",
                                 "FiraCode_2", "FiraCode-Light.ttf")
        regular = os.path.join(utility.viewResourcesDir(), "fonts",
                               "Open_Sans", "OpenSans-Regular.ttf")
        lightItalic = os.path.join(utility.viewResourcesDir(), "fonts",
                                   "Open_Sans", "OpenSans-LightItalic.ttf")
        semibold = os.path.join(utility.viewResourcesDir(), "fonts",
                                "Open_Sans", "OpenSans-SemiBold.ttf")

        QFontDatabase.addApplicationFont(regular)
        QFontDatabase.addApplicationFont(lightItalic)
        QFontDatabase.addApplicationFont(semibold)
        QFontDatabase.addApplicationFont(monoRegular)
        QFontDatabase.addApplicationFont(monoLight)


class Main:
    def __init__(self):
        self.style = """
            QSplitter {
                background: #272629;
            }

            QSplitter::handle:horizontal {
                width: 9px;
            }

            QSplitter::handle:vertical {
                height: 9px;
            }
        """
        self.menu = MenuBar()


class MenuBar:
    def __init__(self):
        self.style = """
            QMenuBar {
                background-color: #272629;
                border: none;
            }

            QMenuBar::item {
                spacing: 18px;
                padding: 1px 9px;
                background: transparent;
                color: #DAD6DE;
            }

            QMenuBar::item:selected { /* when selected using mouse or keyboard */
                background: #DAD6DE;
                color: #272629;
            }

            QMenu {
                background-color: rgba(0, 0, 0, 0.6);
                font-family: Open Sans;
                font-size: 13px;
            }

            QMenu::item {
                color: #DAD6DE;
            }

            QMenu::item:selected {
                color: #322F35;
                background: #DAD6DE;
            }

            QMenu::separator {
                height: 2px;
                background: rgba(255, 255, 255, 0.14);
                margin: 9px;
            }
        """
        self.font = QFont("Open Sans", 13)
        self.font.setPixelSize(13)


class Console:
    def __init__(self):
        self.style = "background-color: #242127; margin: 0; padding: 0; selection-background-color: #5B00C3;"
        self.stdoutFontColor = QColor(255, 246, 255)
        self.stderrFontColor = QColor(206, 24, 1)
        self.font = QFont("Fira Code", 12)
        self.font.setPixelSize(12)
        self.font.setWeight(QFont.Thin)


class Browser:
    def __init__(self):
        self.style = """
            QListView {
                show-decoration-selected: 1;
                background: #19181B;
            }

            QListView::item:selected {
                border: none;
                background: #D9EBF5;
            }

            QListView::item {
                border-top: 1px solid #19181B;
                background: #322F35;
            }
        """
        self.width = 216
        self.item = BrowserItem()
        self.info = TemplateInfo()


class BrowserItem:
    def __init__(self):
        self.size = QSize(216, 108)

        self.headerFont = QFont("Open Sans", 13)
        self.headerFont.setPixelSize(13)
        self.headerFont.setWeight(QFont.DemiBold)
        self.headerStyle = "margin-left: 18px; margin-right: 9px; color: #DAD6DE;"
        self.headerStyleSelected = "margin-left: 18px; margin-right: 9px; color: #322F35;"

        self.commandFont = QFont("Fira Code", 11)
        self.commandFont.setPixelSize(11)
        self.commandFont.setWeight(QFont.Light)
        self.commandStyle = "margin-left: 18px; margin-right: 9px; color: #DAD6DE;"
        self.commandStyleSelected = "margin-left: 18px; margin-right: 9px; color: #322F35;"

        self.descriptionFont = QFont("Open Sans", 12)
        self.descriptionFont.setPixelSize(12)
        self.descriptionStyle = "margin-left: 9px; margin-right: 9px; color: #DAD6DE;"
        self.descriptionStyleSelected = "margin-left: 9px; margin-right: 9px; color: #322F35;"


class TemplateInfo:
    def __init__(self):
        self.style = "background-color: #272629; margin: 0; padding: 0;"
        self.height = 204
        self.width = 216

        self.headerFont = QFont("Open Sans", 15)
        self.headerFont.setPixelSize(15)
        self.headerFont.setWeight(QFont.Light)
        self.headerFont.setItalic(True)
        self.headerStyle = "margin: 13px 9px 18px 9px; color: #4C4452;"

        self.textAreaStyle = "background-color: #272629; margin: 0 0 18px 9px; selection-background-color: #5B00C3;"
        self.textAreaFont = QFont("Open Sans", 13)
        self.textAreaFont.setPixelSize(13)
        self.textAreaFont.setWeight(QFont.Normal)
        self.textAreaFontColor = QColor(218, 214, 222)


class ContextMenu:
    def __init__(self):
        self.style = """
            QMenu {
                background-color: rgba(0, 0, 0, 0.6);
                font-family: Open Sans;
                font-size: 13px;
            }

            QMenu::item {
                color: #D9EBF5;
            }

            QMenu::item:selected {
                color: #322F35;
                background: #D9EBF5;
            }

            QMenu::separator {
                height: 2px;
                background: rgba(255, 255, 255, 0.14);
                margin: 9px;
            }
        """
        self.font = QFont("Open Sans", 12)
        self.font.setPixelSize(12)


class Editor:
    def __init__(self):
        self.style = "background: #272629;"
        self.tip = EditorTip()


class EditorTip:
    def __init__(self):
        self.style = "color: #3D3B40;"
        self.font = QFont("Open Sans", 30)
        self.font.setPixelSize(30)
        self.font.setWeight(QFont.Bold)


class Track:
    def __init__(self):
        self.style = "background: #3D3B40;"
        self.width = 198
        self.header = TrackHeader()
        self.cell = Cell()


class TrackHeader:
    def __init__(self):
        self.style = "background: #3D3B40;"
        self.styleSelected = "background: #0059FB;"
        self.height = 72

        self.backendNameFont = QFont("Open Sans", 13)
        self.backendNameFont.setPixelSize(13)
        self.backendNameFont.setWeight(QFont.DemiBold)
        self.backendNameStyle = "color: #D9EBF5;"

        self.userNameFont = QFont("Open Sans", 12)
        self.userNameFont.setPixelSize(12)
        self.userNameStyle = "color: #D9EBF5; \
                background: transparent; \
                border: none; \
                selection-background-color: #5B00C3;"


class Cell:
    def __init__(self):
        self.style = "background: #646167;"
        self.styleSelected = "background: #30EDD5;"
        self.styleSelectedTrackNormal = "background: #8B878F;"
        self.styleEvaluated = "background: #5B00C3;"

        self.height = 90

        self.nameStyle = "background: rgba(255, 255, 255, 0.1); \
                border: none; \
                color: #343136; \
                selection-background-color: #5B00C3; \
                padding: 0 18px 0 18px; \
                margin: 0;"
        self.nameFont = QFont("Open Sans", 12)
        self.nameFont.setPixelSize(12)
        self.nameHeight = 18

        self.previewStyle = "padding: 5px 9px 9px 9px; \
                margin: 0; \
                border: none; \
                line-height: 14px; \
                color: #E1F0F9;"
        self.previewStyleSelected = "padding: 5px 9px 9px 9px; \
                margin: 0; \
                border: none; \
                line-height: 14px; \
                color: #343136;"
        self.previewFont = QFont("Fira Code", 11)
        self.previewFont.setWeight(QFont.Light)
        self.previewFont.setPixelSize(11)


class Confirmation:
    def __init__(self):
        self.style = """
            QMessageBox {
                background: #272629;
            }

            QMessageBox QTextEdit {
                color: #DAD6DE;
                font-family: \"Open Sans\";
            }
        """

class TemplateEditor:
    def __init__(self):
        self.style = """
            QWidget {
                background: #272629;
            }

            QWidget QLabel {
                font-family: \"Open Sans\";
                font-size: 12px;
                color: #DAD6DE;
            }
        """
        self.inputStyle = "background: rgba(255, 255, 255, 0.1); \
                border: none; \
                color: #DAD6DE; \
                selection-background-color: #5B00C3;"
        self.inputHeight = 18
        self.inputCodeFont = QFont("Fira Code", 11)
        self.inputCodeFont.setPixelSize(11)
        self.inputCodeFont.setWeight(QFont.Light)
        self.inputFont = QFont("Open Sans", 12)
        self.inputFont.setPixelSize(12)

        self.descriptionStyle = "background: #19181B; \
                border: none; \
                color: #DAD6DE; \
                selection-background-color: #5B00C3;"
        self.descriptionFont = QFont("Open Sans", 12)
        self.descriptionFont.setPixelSize(12)


class Theme:
    browser = Browser()
    confirmation = Confirmation()
    console = Console()
    contextMenu = ContextMenu()
    editor = Editor()
    main = Main()
    templateEditor = TemplateEditor()
    track = Track()


class ScrollBar(QScrollBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QScrollBar:horizontal {
                border: none;
                background: rgba(0, 0, 0, 0);
                height: 9px;
                margin: 0;
            }

            QScrollBar::handle:horizontal {
                background: rgba(255, 255, 255, 0.1);
                min-width: 9px;
            }

            QScrollBar::add-line:horizontal {
                background: none;
                width: 9px;
                subcontrol-position: right;
                subcontrol-origin: margin;

            }

            QScrollBar::sub-line:horizontal {
                background: none;
                width: 9px;
                subcontrol-position: top left;
                subcontrol-origin: margin;
                position: absolute;
            }

            QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                width: 9px;
                height: 9px;
                background: none;
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }

            /* VERTICAL */
            QScrollBar:vertical {
                border: none;
                background: rgba(0, 0, 0, 0);
                width: 9px;
                margin: 0;
            }

            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.1);
                min-width: 9px;
            }

            QScrollBar::add-line:vertical {
                background: none;
                height: 9px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical {
                background: none;
                height: 9px;
                subcontrol-position: top left;
                subcontrol-origin: margin;
                position: absolute;
            }

            QScrollBar:up-arrow:vertical, QScrollBar::down-arrow:vertical {
                width: 9px;
                height: 9px;
                background: none;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
