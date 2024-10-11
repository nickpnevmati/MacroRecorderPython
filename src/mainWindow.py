import io
from optparse import Option
from typing import Callable

from PyQt5.QtCore import QSettings, pyqtSignal, QEvent
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QCheckBox, QAction, QPushButton, QVBoxLayout, QLayout, QWidget, QLineEdit, QHBoxLayout, QSizePolicy, QScrollArea
)
from PyQt5.uic import loadUi
import os
from appdirs import user_data_dir
from pynput.keyboard import HotKey
from src import ShortcutWidget
from src.ShortcutWidget import KeySequenceWidget
from src.backend.KeyCodeSerializer import serialize_keys, deserialize_keys
from src.backend.ShortcutListener import ShortcutListener
from src.backend.macroRecorder import MacroRecorder
from src.logger import logger


def create_hotkey_widget(on_changed: Callable[[list | None], None], preload: list | None, parent: QLayout) -> ShortcutWidget:
    widget = KeySequenceWidget()
    widget.connect_shortcut_changed_callback(on_changed)
    widget.set_sequence(preload)
    widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    parent.addWidget(widget)
    return widget

class MainWindow(QMainWindow):

    ui_construct_signal = pyqtSignal()

    def __init__(self, app : QApplication):
        super().__init__()
        self.app = app
        self.win = loadUi('ui/MainWindow.ui', self)

        self.ui_prefabs = {
            "macroItem": 'ui/MacroItem.ui',
            'macroActions' : 'ui/MacroAction.ui'
        }

        self.macro_hotkey_listener = ShortcutListener()
        self.misc_hotkey_listener = ShortcutListener()
        self.settings = QSettings("MacroRecorderPython", "settings")

        stop_recording_keys = self.settings.value('stopRecordingHotkey', 'None')
        keys_deserialized = deserialize_keys(stop_recording_keys) if stop_recording_keys != 'None' else None
        self.stop_recording_hotkey = HotKey(keys_deserialized, self.stop_recording) if keys_deserialized else None
        self.misc_hotkey_listener.register_hotkey(self.stop_recording_hotkey)

        self.macro_items_container: QWidget = self.win.findChild(QWidget, 'macroItemsContainer')
        self.macro_actions_container: QWidget = self.win.findChild(QWidget, 'macroActionsContainer')
        self.scroll_area_action: QScrollArea = self.win.findChild(QScrollArea, 'scrollAreaAction')
        self.scroll_area_item: QScrollArea = self.win.findChild(QScrollArea, 'scrollAreaItem')

        #region Initialize Widgets & Signals

        key_seq_widget = create_hotkey_widget(self.stop_recording_shortcut_changed, keys_deserialized,
                                              self.win.findChild(QWidget, "stopShortcutContainer").layout())

        clear_button: QPushButton = self.win.findChild(QPushButton, "clearShortcutButton")
        clear_button.clicked.connect(key_seq_widget.clear_sequence)

        self.hide_to_tray_when_closing_action: QAction = self.win.findChild(QAction, 'actionHide_To_Tray_When_Closing')
        self.hide_to_tray_when_closing_action.triggered.connect(self.hide_to_tray_when_closing_changed)
        self.hide_to_tray_when_closing_action.setChecked(self.settings.value("minimizeWhenClose", "true") == "true")

        self.hide_when_recording_checkbox : QCheckBox = self.win.findChild(QCheckBox, "hideWhenRecordingCheckbox")
        self.hide_when_recording_checkbox.stateChanged.connect(self.hide_when_recording_changed)
        self.hide_when_recording_checkbox.setCheckState(3 if self.settings.value("hideWhenRecording", "true") == "true" else 0)

        self.minimize_on_startup_action : QAction = self.win.findChild(QAction, 'actionMinimize_On_Startup')
        self.minimize_on_startup_action.triggered.connect(self.minimize_on_startup_changed)
        self.minimize_on_startup_action.setChecked(self.settings.value("minimizeOnStartup", "false") == "true")

        self.start_recording_button: QPushButton = self.win.findChild(QPushButton, 'startRecordingButton')
        self.start_recording_button.clicked.connect(self.start_recording_trigger)

        self.ui_construct_signal.connect(self.create_macro_item_ui) # This UI framework is great but I hate it
        self.ui_construct_signal.connect(self.create_macro_actions_ui)

        #endregion

        if self.settings.value("minimizeOnStartup", False) == "true":
            self.hide()
        else:
            self.show()

    #region Callbacks & Triggers

    def start_recording_trigger(self):
        self.start_recording_button.setEnabled(False)
        self.macro_hotkey_listener.set_enabled(False)
        if self.settings.value('hideWhenRecording', "true") == "true":
            self.hide()

    def stop_recording_shortcut_changed(self, keys: list | None):
        serialized_keys = serialize_keys(keys) if keys else 'None'
        self.settings.setValue("stopRecordingHotkey", serialized_keys)
        new_hotkey = HotKey(keys, self.stop_recording) if keys else None
        self.misc_hotkey_listener.update_hotkey(self.stop_recording_hotkey, new_hotkey)
        self.stop_recording_hotkey = new_hotkey

    def hide_to_tray_when_closing_changed(self, check_state):
        self.settings.setValue("minimizeWhenClose", "true" if check_state else "false")
        logger.info(f'set minimizeWhenClose to {check_state}')

    def hide_when_recording_changed(self, state):
        self.settings.setValue("hideWhenRecording", "false" if state == 0 else "true")

    def minimize_on_startup_changed(self, checked_state):
        self.settings.setValue("minimizeOnStartup", checked_state)

    #endregion

    def stop_recording(self):
        self.start_recording_button.setEnabled(True)
        self.macro_hotkey_listener.set_enabled(True)
        self.ui_construct_signal.emit()
        logger.info('Stopped recording')

    def create_macro_item_ui(self):
        item_widget: QWidget = loadUi("ui/MacroItem.ui")
        name_field = item_widget.findChild(QLineEdit, 'MacroNameField')
        delete_button = item_widget.findChild(QPushButton, 'DeleteMacroButton')
        save_button = item_widget.findChild(QPushButton, 'SaveButton')
        hotkey_field : QWidget = item_widget.findChild(QWidget, 'MacroHotkey')

        create_hotkey_widget(lambda k: print('aylmao'), None, hotkey_field.layout())
        self.macro_items_container.layout().addWidget(item_widget)
        self.scroll_area_item.setMinimumWidth(item_widget.minimumWidth())
        logger.info("Added MacroItem")

    def create_macro_actions_ui(self):
        actions_widget: QWidget = loadUi('ui/MacroAction.ui')

    def closeEvent(self, event):
        if self.settings.value("minimizeWhenClose", "true") == "true":
            event.ignore()
            self.hide()
        else:
            self.app.quit()