import json
from src import user_data_dir
from src.backend.macroManager import MacroManager
from src.frontend.mainWindow import MainWindow

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