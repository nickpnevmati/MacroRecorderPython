import io
import json
import threading
import time
from typing import Callable
from uuid import uuid4
from PyQt5.QtCore import pyqtSignal
from appdirs import user_data_dir
import os
from src.backend.HotkeyListener import HotkeyListener
from src.backend.macroPlayer import MacroPlayer
from src.backend.macroRecorder import MacroRecorder
import uuid
from src.logger import logger


class MacroManager:
    def __init__(self, stop_keys, ui_construct_signal: Callable[[dict], None]) -> None:
        self.__macroFilePath: str = user_data_dir('MacroRecorderPython')
        os.makedirs(self.__macroFilePath, exist_ok=True)

        self.__ui_construct_signal = ui_construct_signal
        self.__recorder = MacroRecorder(self.__on_recording_stopped)
        self.__stop_listener = HotkeyListener(stop_keys, self.__recorder.stop)

        self.__macros: dict[str, MacroPlayer] = {}
        self.__read_macro_files()

    def start_recording(self):
        self.__stop_listener.set_enabled(True)
        self.__recorder.start()

    def play_macro(self, uid: str):
        self.__macros[uid].start()

    def update_stop_keys(self, stop_keys):
        self.__stop_listener.set_hotkey(stop_keys)

    def update_macro_file(self, filename, name, hotkey):
        macro = self.get_macro_file_data(filename)
        macro['name'] = name
        macro['hotkey'] = hotkey
        filepath = self.__macro_path(filename)
        with open(filepath, 'w') as f:
            json.dump(macro, f)
        logger.info(f'Macro {filename} updated with: Name {name} | Hotkey {hotkey}')

    def delete_macro_file(self, filename):
        os.remove(self.__macro_path(filename))
        logger.info(f'Deleted macro file {filename}')

    def get_macro_file_data(self, filename):
        return self.__read_macro_file(self.__macro_path(filename))

    def __on_recording_stopped(self, actions: list[str]):
        self.__stop_listener.set_enabled(False)
        filename = str(uuid4())
        macro = self.__create_macro_file(filename, '\n'.join(actions))
        self.__macros[filename] = MacroPlayer(macro)
        self.__ui_construct_signal(
            {
                'filename': filename,
                'macro': macro
            }
        )

    def __macro_path(self, uid: str):
        return os.path.join(self.__macroFilePath, uid)

    def __read_macro_files(self):
        for filename in os.listdir(self.__macroFilePath):
            filepath = self.__macro_path(filename)
            if not os.path.isfile(filepath):
                continue
            macro = self.__read_macro_file(filepath)
            if macro is not None:
                self.__macros[filename] = MacroPlayer(macro)
                logger.info(f'Read macro file {filepath}')
                self.__ui_construct_signal(
                    {
                        'filename': filename,
                        'macro': macro
                    }
                )

    def __read_macro_file(self, filepath):
        with open(filepath, 'r') as f:
            try:
                macro = json.load(f)
                return macro
            except json.JSONDecodeError as e:
                logger.error(f'Failed to parse macro file {filepath} - JSON Decoder Error {e}')
                return None

    def __create_macro_file(self, filename, data: str):
        filepath = os.path.join(self.__macroFilePath, filename)
        macro = {
            'name': '',
            'hotkey': '',
            'actions': data
        }

        with open(filepath, 'w') as f:
            json.dump(macro, f)
        return macro