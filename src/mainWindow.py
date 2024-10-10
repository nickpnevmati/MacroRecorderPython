from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QCheckBox, QAction, QPushButton, QKeySequenceEdit, QVBoxLayout
)
from PyQt5.uic import loadUi

from src.ShortcutWidget import KeySequenceWidget
from src.backend.macroManager import MacroManager


class MainWindow(QMainWindow):
    def __init__(self, app : QApplication):
        super().__init__()
        self.app = app
        self.win = loadUi('ui/MainWindow.ui', self)

        self.ui_prefabs = {
            "macroItem": 'ui/MacroItem.ui',
            'macroActions' : 'ui/MacroAction.ui'
        }

        # Create Shortcut Widget
        stop_shortcut_container : QVBoxLayout = self.win.findChild(QVBoxLayout, "stopShortcutContainer")
        clear_button: QPushButton = self.win.findChild(QPushButton, "clearShortcutButton")
        key_seq_widget = KeySequenceWidget()
        key_seq_widget.connect_shortcut_changed_callback(self.stop_recording_shortcut_changed)
        clear_button.clicked.connect(key_seq_widget.clear_sequence)
        stop_shortcut_container.addWidget(key_seq_widget)


        self.settings = QSettings("MacroRecorderPython", "settings")

        self.macro_manager = MacroManager()

        #region Initialize Signals
        self.hide_to_tray_when_closing_action: QAction = self.win.findChild(QAction, 'actionHide_To_Tray_When_Closing')
        self.hide_to_tray_when_closing_action.triggered.connect(self.hide_to_tray_when_closing_trigger)
        self.hide_to_tray_when_closing_action.setChecked(self.settings.value("minimizeWhenClose", True) == "true")

        self.hide_when_recording_checkbox : QCheckBox = self.win.findChild(QCheckBox, "hideWhenRecordingCheckbox")
        self.hide_when_recording_checkbox.stateChanged.connect(self.hide_when_recording_trigger)
        self.hide_when_recording_checkbox.setCheckState(3 if self.settings.value("hideWhenRecording", True) == "true" else 0)

        self.minimize_on_startup_action : QAction = self.win.findChild(QAction, 'actionMinimize_On_Startup')
        self.minimize_on_startup_action.triggered.connect(self.minimize_on_startup_toggle)
        self.minimize_on_startup_action.setChecked(self.settings.value("minimizeOnStartup", False) == "true")

        self.start_recording_button: QPushButton = self.win.findChild(QPushButton, 'startRecordingButton')
        self.start_recording_button.clicked.connect(self.start_recording_trigger)

        # self.stop_recording_shortcut_setter : QKeySequenceEdit = self.win.findChild(QKeySequenceEdit, 'stopRecordingShortcutSetter')
        # self.stop_recording_shortcut_setter.keySequenceChanged.connect(self.something)

        #endregion

        if self.settings.value("minimizeOnStartup", False) == "true":
            self.hide()
        else:
            self.show()

    def stop_recording_shortcut_changed(self, keys: list):
        pass # TODO this shit

    def start_recording_trigger(self):
        if self.settings.value('hideWhenRecording', True):
            self.hide()
            self.macro_manager.start_recording("PLACEHOLDER", self.show)

    def hide_to_tray_when_closing_trigger(self, check_state):
        self.settings.setValue("minimizeWhenClose", check_state)

    def hide_when_recording_trigger(self, state):
        self.settings.setValue("hideWhenRecording", False if state == 0 else True)

    def minimize_on_startup_toggle(self, checked_state):
        self.settings.setValue("minimizeOnStartup", checked_state)

    def closeEvent(self, event):
        if self.settings.value("minimizeWhenClose", True) == "true":
            event.ignore()
            self.hide()
        else:
            self.app.quit()