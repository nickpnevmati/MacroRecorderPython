from PyQt6.QtGui import QDropEvent
from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QMessageBox
from pystray import Icon, MenuItem
from PIL import Image

class MainWindow(QMainWindow):
	def __init__(self, app : QApplication):
		super().__init__()

		self.app = app

		self.setWindowTitle("Macro Recorder Python")

		button = QPushButton("Hide to tray")
		button.pressed.connect(self.hide)

		self.__createTrayIcon()
		self.setCentralWidget(button)
		self.show()

	def closeEvent(self, event):
		# Create a message box
		reply = QMessageBox.question(self, 'Window Close', 'Close or Minimize to tray? \"Yes\" to minimize (lmao this is horrible)',
			QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

		if reply == QMessageBox.StandardButton.Yes:
			event.ignore()
			self.hide()
		else:
			event.accept()

	def __createTrayIcon(self):
		menu = (MenuItem("Show", self.__TrayShow), MenuItem("Exit", self.__TrayExit))
		image = Image.open('resources/logo512.png')
		icon = Icon('Macro Recorder Python', icon=image, menu=menu)
		icon.run_detached()

	def __TrayShow(self, icon, item):
		self.show()

	def __TrayExit(self, icon, item):
		self.app.quit()

