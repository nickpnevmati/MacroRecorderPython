from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.uic import loadUi
from src.ui.HotkeyWidget import HotkeyWidget


class MacroItemWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self, macro: dict, parent=None):
        super().__init__(parent)

        loadUi('ui/MacroItem.ui', self)

        self.filename = macro['filename']
        self.macro_data = macro['macro']

        self.__has_focus = False

        hotkey_container: QWidget = self.findChild(QWidget, 'MacroHotkey')
        self.hotkey_widget: HotkeyWidget = HotkeyWidget(
            on_changed_callback=None,
            preload=self.macro_data['hotkey'],
            parent=hotkey_container.layout()
        )

        self.name_field: QLineEdit = self.findChild(QLineEdit, 'MacroNameField')
        self.name_field.setText(self.macro_data['name'])

        self.save_button: QPushButton = self.findChild(QPushButton, 'SaveButton')
        self.discard_button: QPushButton = self.findChild(QPushButton, 'DiscardChanges')
        self.delete_button: QPushButton = self.findChild(QPushButton, 'DeleteMacroButton')

    def create_ui_actions(self) -> list[QWidget]:
        ui_actions = []
        for index, action in enumerate(self.macro_data['actions'].split('\n')):
            ui_actions.append(MacroActionWidget(index, action))
        return ui_actions


    def __restore_previous(self):
        self.hotkey_widget.set_sequence(self.macro_data['hotkey'])
        self.name_field.setText(self.macro_data['name'])
        # TODO restore previous actions

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

class MacroActionWidget(QWidget):
    def __init__(self, index: int, action: str, parent=None):
        super().__init__(parent)

        loadUi('ui/MacroAction.ui', self)

        self.index = index

        action_items = action.split(' ')

        self.action_label: QLabel = self.findChild(QLabel, 'action_label')
        self.action_label.setText(' '.join(action_items[0:2]))

        self.time_line_edit: QLineEdit = self.findChild(QLineEdit, 'time_edit')
        self.time_line_edit.setText(action_items[2])

        self.save_button: QPushButton = self.findChild(QPushButton, 'save_button')
        self.delete_button: QPushButton = self.findChild(QPushButton, 'delete_button')