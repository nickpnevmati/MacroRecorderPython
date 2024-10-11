from pynput.keyboard import Listener, HotKey

from src.logger import logger


class ShortcutListener:
    def __init__(self):
        self.listener = Listener(on_press=self.__on_press, on_release=self.__on_release)
        self.hotkeys: list[HotKey] = []
        self.__enabled = True
        self.listener.start()

    def register_hotkey(self, hotkey: HotKey):
        logger.info('Hotkey listener registered a hotkey')
        self.hotkeys.append(hotkey)

    def update_hotkey(self, old_hotkey: HotKey, new_hotkey: HotKey):
        logger.info('Hotkey listener updated a hotkey')
        if old_hotkey:
            self.hotkeys.remove(old_hotkey)
        if new_hotkey:
            self.hotkeys.append(new_hotkey)

    def set_enabled(self, enabled: bool):
        logger.info('Hotkey listener ' + 'enabled' if enabled else 'disabled')
        self.__enabled = enabled

    def __on_press(self, key):
        if not self.__enabled:
            return
        for hotkey in self.hotkeys:
            if hotkey:
                hotkey.press(self.listener.canonical(key))

    def __on_release(self, key):
        if not self.__enabled:
            return
        for hotkey in self.hotkeys:
            if hotkey:
                hotkey.release(self.listener.canonical(key))