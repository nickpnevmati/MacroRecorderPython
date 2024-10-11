import io
from typing import Callable
from PyQt5.QtCore import pyqtSignal
from appdirs import user_data_dir
import os
from src.backend.macroPlayer import MacroPlayer
from src.backend.macroRecorder import MacroRecorder

class MacroManager:
    def __init__(self) -> None:
        self.__macroFilePath: str = user_data_dir('MacroRecorderPython')
        os.makedirs(self.__macroFilePath, exist_ok=True)

        self.__stop_recording_callback = None
        self.__macroRecorder = MacroRecorder()

    def start_recording(self, on_stop_callback: Callable[[io.StringIO], None]):
        self.on_recording_stopped.connect(on_stop_callback)
        self.__macroRecorder.start()

    def stop_recording(self):
        self.__macroRecorder.stop()

