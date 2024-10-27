from typing import Callable

from PyQt5.QtWidgets import QLineEdit, QSizePolicy, QLayout
from pynput.keyboard import Listener, Key, KeyCode, HotKey

from src.backend.KeyCodeSerializer import deserialize_keys, serialize_keys

_modifier_order = ["Ctrl", "Cmd", "Alt", "Option", "Shift"]

class HotkeyWidget(QLineEdit):
    def __init__(self, on_changed_callback: Callable[[list | None], None] | None, preload: str, parent: QLayout):
        super().__init__(None)
        self.setPlaceholderText("Hotkey...")
        self.setReadOnly(True)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.string_sequence = []
        self.key_sequence = []

        self.shortcut_changed_callback = on_changed_callback
        self.set_sequence(preload)

        parent.addWidget(self)

        self.listener = Listener(on_press=self.__on_press, on_release=self.__on_release)
        self.listener.start()
        self.listening = False
        self.__is_set = True

    def set_sequence(self, keys_str: str):
        self.clear_sequence()
        keys = deserialize_keys(keys_str)
        if len(keys) == 0:
            return
        for key in keys:
            if isinstance(key, Key):
                self.string_sequence.append(key.name.capitalize() if key.name else str(key))
            if isinstance(key, KeyCode):
                self.string_sequence.append(key.char.capitalize())
        self.__order_sequence()
        self.setText(' + '.join(self.string_sequence))
        self.__execute_callback(keys)

    def get_sequence_serialized(self):
        return serialize_keys(self.key_sequence)

    def clear_sequence(self):
        self.key_sequence.clear()
        self.string_sequence.clear()
        self.clear()
        self.__execute_callback([])

    def mousePressEvent(self, a0):
        if a0.button() == 1:
            a0.accept()
            self.listening = True

    def __on_press(self, key):
        if not self.listening:
            return
        if self.__is_set:
            self.clear_sequence()
            self.__is_set = False
        if isinstance(key, Key):  # For modifiers
            self.key_sequence.append(self.listener.canonical(key))
            key_str = key.name.capitalize() if key.name else str(key)
            self.string_sequence.append(key_str)
            self.__order_sequence()
            self.setText(' + '.join(self.string_sequence))

        elif isinstance(key, KeyCode):  # For character keys
            self.key_sequence.append(self.listener.canonical(key))

            key_str = key.char.capitalize()
            self.string_sequence.append(key_str)
            self.setText(' + '.join(self.string_sequence))

            self.listening = False
            self.__is_set = True
            self.__execute_callback(self.key_sequence)

    def __execute_callback(self, seq):
        if self.shortcut_changed_callback:
            self.shortcut_changed_callback(seq)

    def __on_release(self, key):
        if not self.listening:
            return
        self.key_sequence.remove(key)

        key_str = key.name.capitalize() if key.name else str(key)
        self.string_sequence.remove(key_str)

    def __order_sequence(self):
        self.string_sequence = sorted(
            self.string_sequence,
            key=lambda x: _modifier_order.index(x)
            if x in _modifier_order
            else len(_modifier_order)
        )