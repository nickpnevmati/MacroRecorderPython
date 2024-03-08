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
        self.__writeMacroFile('tmp.macro', actions)
            
    def __writeMacroFile(self, filename: str, data):
        path = user_data_dir() / ('macros' + filename)
        with open(path, 'w') as fp:
            json.dump(data, fp)
            
    def __editPreferece(self, key, value):
        path = user_data_dir() / 'prefs'
        with open(path, 'rw') as prefsFile:
            prefs = json.load(prefsFile)
            prefs[key] = value
            json.dump(prefs, prefsFile)