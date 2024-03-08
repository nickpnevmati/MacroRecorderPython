from PyQt5 import QtWidgets
from src.frontend.ui.uimainwindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.connectionLayer = ConnectionLayer(self)
        

import json
from src import user_data_dir
from src.backend.macroManager import MacroManager

class ConnectionLayer():
    def __init__(self, window: MainWindow) -> None:
        self.manager = MacroManager()
        self.window = window
        
        self.__setup()
        
    def __setup(self):
        """
        This is where the UI layer is connected to the connlayer
        """
        self.window.ui.startRecordingButton.clicked.connect(self.__onStartRecording)
        
    def __onStartRecording(self):
        self.window.hide()
        self.manager.startRecording(self.__onStopRecording)
        
    def __onStopRecording(self):
        self.window.show()
        actions = self.manager.getActions()
        self.__writeToFile('macros/tmp.macro', actions)
        
    def __writeToFile(self, filename: str, data):
        path = user_data_dir() / filename
        fp = open(path, 'w')
        json.dump(data, fp)