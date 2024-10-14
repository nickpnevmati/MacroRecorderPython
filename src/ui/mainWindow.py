from typing import Callable
from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QCheckBox, QAction, QPushButton, QLayout, QWidget, QLineEdit, QSizePolicy, QScrollArea
)
from PyQt5.uic import loadUi
from src.ui import HotkeyWidget
from src.ui.HotkeyWidget import HotkeyWidget
from src.backend.KeyCodeSerializer import serialize_keys, deserialize_keys
from src.backend.macroManager import MacroManager
from src.logger import logger

class MainWindow(QMainWindow):

    ui_construct_signal = pyqtSignal(object)

    def __init__(self, app : QApplication):
        super().__init__()
        self.app = app
        self.win = loadUi('ui/MainWindow.ui', self)

        self.settings = QSettings("MacroRecorderPython", "settings")

        self.macro_items_container: QWidget = self.win.findChild(QWidget, 'macroItemsContainer')
        self.macro_actions_container: QWidget = self.win.findChild(QWidget, 'macroActionsContainer')
        self.scroll_area_action: QScrollArea = self.win.findChild(QScrollArea, 'scrollAreaAction')
        self.scroll_area_item: QScrollArea = self.win.findChild(QScrollArea, 'scrollAreaItem')

        #region Initialize Widgets & Signals

        key_seq_widget = HotkeyWidget(
            self.stop_recording_hotkey_changed,
            self.settings.value('stopRecordingHotkey', '[]'),
            self.win.findChild(QWidget, "stopShortcutContainer").layout()
        )

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

        #endregion

        self.macro_manager = MacroManager(self.settings.value('stopRecordingHotkey', '[]'), self.__stopped_recording_callback)

        if self.settings.value("minimizeOnStartup", False) == "true":
            self.hide()
        else:
            self.show()

    #region Callbacks & Triggers

    def start_recording_trigger(self):
        self.start_recording_button.setEnabled(False)
        if self.settings.value('hideWhenRecording', "true") == "true":
            self.hide()
        self.macro_manager.start_recording()

    def stop_recording_hotkey_changed(self, keys: list | None):
        self.settings.setValue("stopRecordingHotkey", serialize_keys(keys))

    def hide_to_tray_when_closing_changed(self, check_state):
        self.settings.setValue("minimizeWhenClose", "true" if check_state else "false")
        logger.info(f'set minimizeWhenClose to {check_state}')

    def hide_when_recording_changed(self, state):
        self.settings.setValue("hideWhenRecording", "false" if state == 0 else "true")

    def minimize_on_startup_changed(self, checked_state):
        self.settings.setValue("minimizeOnStartup", checked_state)

    #endregion

    def __stopped_recording_callback(self, macro: dict):
        self.ui_construct_signal.emit(macro)
        self.start_recording_button.setEnabled(True)
        if self.settings.value('hideWhenRecording', "true") == 'true':
            self.show()

    def create_macro_item_ui(self, macro: object):
        if not isinstance(macro, dict):
            logger.error("Macro object is not a dict")
            return

        filename = macro['filename']
        macro_data = macro['macro']

        item_widget: QWidget = loadUi("ui/MacroItem.ui")

        self.macro_items_container.layout().addWidget(item_widget)
        self.scroll_area_item.setMinimumWidth(item_widget.minimumWidth())

        name_field: QLineEdit = item_widget.findChild(QLineEdit, 'MacroNameField')
        name_field.setText(macro_data['name'])

        delete_button: QPushButton = item_widget.findChild(QPushButton, 'DeleteMacroButton')
        delete_button.clicked.connect(
            lambda :
            (
                self.macro_manager.delete_macro_file(filename),
                self.macro_items_container.layout().removeWidget(item_widget)
            )
        )

        hotkey_container: QWidget = item_widget.findChild(QWidget, 'MacroHotkey')
        hotkey_widget: HotkeyWidget = HotkeyWidget(
            callback = None,
            preload = macro_data['hotkey'],
            parent = hotkey_container.layout()
        )

        save_button: QPushButton = item_widget.findChild(QPushButton, 'SaveButton')
        save_button.clicked.connect(
            lambda :(
                self.macro_manager.update_macro_file(
                    filename=filename,
                    name=name_field.text(),
                    hotkey=hotkey_widget.get_sequence_serialized()
                )
            )
        )

        def restore_previous():
            mac = self.macro_manager.get_macro_file_data(filename)
            if mac is None:
                return
            mac_name = mac['name']
            mac_hotkey = mac['hotkey']
            # hotkey_container.set_sequence(mac_hotkey)
            name_field.setText(mac_name)
            logger.info(f'Changes to macro {filename} discarded')

        discard_button: QPushButton = item_widget.findChild(QPushButton, 'DiscardChanges')
        discard_button.clicked.connect(restore_previous)

        logger.info("Added MacroItem")

        actions_widget: QWidget = loadUi('ui/MacroAction.ui')

        # TODO add macro actions

    def closeEvent(self, event):
        if self.settings.value("minimizeWhenClose", "true") == "true":
            event.ignore()
            self.hide()
        else:
            self.app.quit()