import threading
from typing import Callable
from pynput.keyboard import Listener, HotKey
from src.backend.KeyCodeSerializer import deserialize_keys
from src.logger import logger

class HotkeyListener:
    def __init__(self, keys: str, callback: Callable):
        self.listener = Listener(on_press=self.__on_press, on_release=self.__on_release)
        self.__callback = callback
        dsk = []
        for k in deserialize_keys(keys):
            dsk.append(self.listener.canonical(k))
        self.hotkey = HotKey(deserialize_keys(keys), self.__callback_wrapper)
        self.__enabled = False
        self.__lock = threading.Lock()
        self.listener.start()

    def set_hotkey(self, keys: str):
        with self.__lock:
            self.hotkey = HotKey(deserialize_keys(keys), self.__callback_wrapper)

    def set_enabled(self, enabled: bool):
        self.__enabled = enabled

    def __callback_wrapper(self):
        if self.__enabled:
            logger.info('HotkeyListener callback called')
            self.__callback()

    def __on_press(self, key):
        with self.__lock:
            if self.__enabled:
                logger.info(f'HotkeyListener - pressed {str(key)}')
            self.hotkey.press(self.listener.canonical(key))

    def __on_release(self, key):
        with self.__lock:
            if self.__enabled:
                logger.info(f'HotkeyListener - released {str(key)}')
            self.hotkey.release(self.listener.canonical(key))