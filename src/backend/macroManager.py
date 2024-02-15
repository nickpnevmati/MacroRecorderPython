from io import StringIO
from pynput.keyboard._base import Key, KeyCode
from src.backend.macroPlayer import MacroPlayer
from src.backend.macroRecorder import MacroRecorder
import pathlib
import re
import json
from typing import Callable
from pynput.keyboard import Listener
import threading

class __ShortcutListener():
    def __init__(self, notify: Callable[[list[str]], None]) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._keys: list = list()
        self._notify: Callable[[list[str]], None] = notify
        self.__listener = Listener(on_press=self.__on_press, on_release=self.__on_release)
        self.__listener.start()
        self.__active = False
    
    def start(self):
        self.__active = True
        self._notify(self._keys)
    
    def stop(self):
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

class MacroManager():
    def __init__(self) -> None:
        self.__macroFilePath: str = '' #TODO actually set the path for the macros
        self.__macros: dict[str, str] = dict()
        self.__shortcutListener: __ShortcutListener = __ShortcutListener(self.__checkShortcuts)
    
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
    
    def __checkShortcuts(self, keysDown: list[str]) -> None:
        pass
