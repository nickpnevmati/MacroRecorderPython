from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

class ShortcutInputField(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Enter a shortcut")

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Escape:
            self.clear()
        else:
            modifiers = event.modifiers()
            key_sequence = QKeySequence(modifiers | key)
            self.setText(key_sequence.toString(QKeySequence.NativeText))

# TESTING PURPOSES ONLY
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Keyboard Shortcut Input Field Example")

#         self.shortcut_line_edit = ShortcutInputField(self)

#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)
#         layout.addWidget(self.shortcut_line_edit)