import os

import cells.utility as utility
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
        self.style = "background-color: #242127;"
        self.stdoutFontColor = QColor(255, 246, 255)
        self.stderrFontColor = QColor(206, 24, 1)
        self.font = QFont("Fira Code", 12)
        self.font.setWeight(QFont.Thin)


class Theme:
    fonts = Fonts()
    browser = ""
    console = Console()
    editor = ""
    templateEditor = ''


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
