import threading
from PyQt5.QtCore import pyqtSignal
from appdirs import user_data_dir
import os
from src.backend.macroRecorder import MacroRecorder

class MacroManager:

    def __init__(self, recorder_stopped_callback) -> None:
        self.__macroFilePath: str = user_data_dir('MacroRecorderPython')
        os.makedirs(self.__macroFilePath, exist_ok=True)

        self.on_recorder_stop = recorder_stopped_callback

        self.__lock = threading.Lock()
        self.__recorder = None
        self.is_recording = False

    def start_recording(self):
        self.is_recording = True
        self.__recorder = MacroRecorder(self.__lock, lambda : (self.on_recorder_stop(),
                                                               setattr(self, 'is_recording', False)))

    def stop_recording(self):
        data = self.__recorder.recorder_stop()
        # TODO

