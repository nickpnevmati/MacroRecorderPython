from PyQt5 import QtWidgets
from frontend.trayIcon import IconThread
from frontend.ui.uiMainWindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)