import os
os.environ["QT_API"] = "pyqt6"

from qtpy.QtWidgets import QApplication, QMainWindow
from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy.QtCore import QUrl
from qtpy.QtCore import QObject, QThread,  Signal, Slot, QTimer,QCoreApplication

import sys

import qtpy

class GrafanaWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.load(QUrl("http://localhost:3000/"))
        self.setCentralWidget(self.browser)
        self.showMaximized()

app = QApplication(sys.argv)

window = GrafanaWindow()
sys.exit(app.exec())
