import os

import cells.utility as utility
from PySide2.QtCore import QSize
from PySide2.QtGui import QColor, QFont, QFontDatabase
from PySide2.QtWidgets import QScrollBar


class Fonts:
    def __init__(self):
        self.regulars = QFont("OpenSans-Regular", 12)
        self.lightItalic = QFont("OpenSans-LightItalic", 12)
        self.semibold = QFont("OpenSans-SemiBold", 12)
        self.mono = QFont("Fira Code", 12)

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


class Console:
    def __init__(self):
        self.style = "background-color: #242127; margin: 0; padding: 0; selection-background-color: #19181B;"
        self.stdoutFontColor = QColor(255, 246, 255)
        self.stderrFontColor = QColor(206, 24, 1)
        self.font = QFont("Fira Code", 12)
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
        self.headerFont.setWeight(QFont.DemiBold)
        self.headerStyle = "margin-left: 18px; margin-right: 9px; color: #DAD6DE;"
        self.headerStyleSelected = "margin-left: 18px; margin-right: 9px; color: #322F35;"

        self.commandFont = QFont("Fira Code", 11)
        self.commandFont.setWeight(QFont.Light)
        self.commandStyle = "margin-left: 18px; margin-right: 9px; color: #DAD6DE;"
        self.commandStyleSelected = "margin-left: 18px; margin-right: 9px; color: #322F35;"

        self.descriptionFont = QFont("Open Sans", 12)
        self.descriptionStyle = "margin-left: 9px; margin-right: 9px; color: #DAD6DE;"
        self.descriptionStyleSelected = "margin-left: 9px; margin-right: 9px; color: #322F35;"


class TemplateInfo:
    def __init__(self):
        self.style = "background-color: #272629; margin: 0; padding: 0;"
        self.height = 204
        self.width = 216

        self.headerFont = QFont("Open Sans", 15)
        self.headerFont.setWeight(QFont.Light)
        self.headerFont.setItalic(True)
        self.headerStyle = "margin: 13px 9px 18px 9px; color: #4C4452;"

        self.textAreaStyle = "background-color: #272629; margin: 0 0 18px 9px;"
        self.textAreaFont = QFont("Open Sans", 13)
        self.textAreaFont.setWeight(QFont.Normal)
        self.textAreaFontColor = QColor(218, 214, 222)


class ContextMenu:
    def __init__(self):
        self.style = """
        QMenu {
            background-color: rgba(0, 0, 0, 0.7);
        }
        QMenu::item {
            color: #FFF6FF;
        }
        QMenu::item:selected {
            color: #322F35;
            background: #D9EBF5;
        }
        """
        self.font = QFont("Open Sans", 12)


class Theme:
    fonts = Fonts()
    browser = Browser()
    console = Console()
    editor = None
    templateEditor = None
    contextMenu = ContextMenu()


class ScrollBar(QScrollBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QScrollBar:horizontal {
                border: none;
                background: rgba(0, 0, 0, 0.07);
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
                background: rgba(0, 0, 0, 0.07);
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
