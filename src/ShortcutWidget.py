from PyQt5.QtWidgets import QLineEdit, QSizePolicy
from pynput.keyboard import Listener, Key, KeyCode, HotKey

from src.backend.macroManager import ShortcutListener

_modifier_order = ["Ctrl", "Cmd", "Alt", "Option", "Shift"]

# TODO actually make it so the fucking shortcut can be saved....
class KeySequenceWidget(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Press keys for shortcut...")
        self.setReadOnly(True)

        size_policy = QSizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.Policy.Maximum)
        self.setSizePolicy(size_policy)

        self.string_sequence = []
        self.key_sequence = []

        self.shortcut_changed_callback = None

        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.listening = False

    def on_press(self, key):
        if not self.listening:
            return
        if isinstance(key, Key):  # For modifiers
            self.key_sequence.append(key)
            key_str = key.name.capitalize() if key.name else str(key)
            self.string_sequence.append(key_str)
            self.string_sequence = sorted(
                self.string_sequence,
                key=lambda x: _modifier_order.index(x)
                if x in _modifier_order
                else len(_modifier_order)
            )
            self.setText(' + '.join(self.string_sequence))

        elif isinstance(key, KeyCode):  # For character keys
            self.key_sequence.append(key)

            key_str = key.char.capitalize()
            self.string_sequence.append(key_str)
            self.setText(' + '.join(self.string_sequence))

            self.listening = False
            self.shortcut_changed_callback(self.key_sequence)

    def on_release(self, key):
        if not self.listening:
            return
        self.key_sequence.remove(key)

        key_str = key.name.capitalize() if key.name else str(key)
        self.string_sequence.remove(key_str)

    def clear_sequence(self):
        self.key_sequence.clear()
        self.string_sequence.clear()
        self.clear()

    def connect_shortcut_changed_callback(self, callback):
        self.shortcut_changed_callback = callback

    def mousePressEvent(self, a0):
        if a0.button() == 1:
            a0.accept()
            self.listening = True