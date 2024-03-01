from PyQt5 import QtWidgets
from src.backend.macroManager import MacroManager
from src.frontend.ui.uimainwindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.startRecordingButton.clicked.connect(self.OnStartRecordingClicked)
        self.macroManager = MacroManager()
        
    def OnStartRecordingClicked(self):
        # TODO start recording
        self.hide()
        self.macroManager.startRecording(self.show)