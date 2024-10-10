import json
import pathlib
import re
import threading
from typing import Callable
from pynput.keyboard import Listener
from appdirs import user_data_dir
import os
from src.backend.macroPlayer import MacroPlayer
from src.backend.macroRecorder import MacroRecorder

class ShortcutListener:
    def __init__(self, notify: Callable[[list[str]], None]) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._keys: list = list()
        self._notify: Callable[[list[str]], None] = notify
        self.__listener = Listener(on_press=self.__on_press, on_release=self.__on_release)
        self.__active = False
    
    def start(self):
        with self._lock:
            self.__active = True

    def stop(self):
        with self._lock:
            self.__active = False
        
    def __on_press(self, key):
        with self._lock:
            self._keys.append(key)
            keys = self._keys.copy()
        if self.__active:
            self._notify(keys)
    
    def __on_release(self, key):
        with self._lock:
            self._keys.remove(key)

class MacroManager:
    def __init__(self) -> None:
        self.__macroFilePath: str = user_data_dir('MacroRecorderPython')
        os.makedirs(self.__macroFilePath, exist_ok=True)

        self.__listen_shortcuts = True
        self.__stop_recording_callback = None
        self.__stop_recording_shortcut = 'esc'

        self.__macros: dict[str, str] = dict()
        self.__shortcutListener: ShortcutListener = ShortcutListener(self.__check_shortcuts)
        self.__shortcutListener.start()

    def start_recording(self, stop_shortcut: str, stop_callback: Callable):
        self.__listen_shortcuts = False # Shouldn't trigger macros while recording
        self.__stop_recording_shortcut = stop_shortcut
        self.__stop_recording_callback = stop_callback
    
    def refresh(self) -> None:
        self.__macros.clear()
        for pathItem in pathlib.Path(self.__macroFilePath).iterdir():
            if not pathItem.is_file() or re.match(r'.*\.macro', pathItem.name) is None:
                continue
            self.__parse_macro_file(pathItem.name)
            
    def __parse_macro_file(self, filename: str) -> None:
        if filename in self.__macros:
            return # TODO raise a warning
        
        fp = open(filename, 'r')
        macro = json.load(fp)
    
    def __check_shortcuts(self, keys_down: list[str]) -> None:
        if self.__listen_shortcuts:
            pass # TODO
        elif set(keys_down) == set(self.__stop_recording_shortcut):
            self.__stop_recording_callback()
            # TODO stop recording
