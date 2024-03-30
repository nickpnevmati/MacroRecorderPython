import json
import src
from src.backend.macroManager import MacroManager, RecorderSettings
from src.frontend.mainWindow import MainWindow
from PyQt5 import QtWidgets

class ConnectionLayer():
    """
    This class acts like an intermediate layer (hence the name) between the UI madness,
    the multithreading macro recording/playback madness and any other module that adds the overall
    madness. 
    
    I'm not even sure why I undertook this project at this point to be honest....
    """
    def __init__(self, window: MainWindow) -> None:
        self.manager = MacroManager()
        self.recorderPrefs : RecorderSettings = RecorderSettings()
        self.window = window
        
        self.__setup()
        
    def __setup(self):
        """
        This is where the UI layer is connected to the connlayer
        """
        self.window.ui.startRecordingButton.clicked.connect(self.__onStartRecording)
        self.window.ui.captureMouseToggle.toggled.connect(lambda value : self.recorderPrefs.setCaptureMouse(value))
    
    def __onStartRecording(self):
        self.window.hide()
        self.manager.startRecording(self.__onStopRecording, self.recorderPrefs)
        
    def __onStopRecording(self):
        self.window.show()
        actions = self.manager.getActions()
        self.__writeMacroFile('tmp.macro', actions)
    
    
            
    def __writeMacroFile(self, filename: str, data):
        path = src.app_data_path / 'macros' / filename
        with open(path, 'w') as fp:
            json.dump(data, fp)
            
    def __editPreferece(self, key, value):
        path = src.app_data_path / 'prefs'
        with open(path, 'rw') as prefsFile:
            prefs = json.load(prefsFile)
            prefs[key] = value
            json.dump(prefs, prefsFile)