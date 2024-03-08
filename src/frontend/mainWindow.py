from PyQt5 import QtWidgets
from src.connectionLayer import ConnectionLayer
from src.frontend.ui.uimainwindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.connectionLayer = ConnectionLayer(self)