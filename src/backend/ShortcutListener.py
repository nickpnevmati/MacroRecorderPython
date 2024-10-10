from pynput.keyboard import Listener, HotKey

class ShortcutListener:
    def __init__(self, keys, callback):
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.hotkey = HotKey(keys, callback)

    def on_press(self, key):
        self.hotkey.press(self.listener.canonical(key))

    def on_release(self, key):
        self.hotkey.release(self.listener.canonical(key))