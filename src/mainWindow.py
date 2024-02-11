from PyQt5.QtWidgets import (
	QApplication,
	QMainWindow,
	QMessageBox,
)

from pystray import Icon, MenuItem, Menu
from PIL import Image
from PyQt5.uic import loadUi
from src.TrayIcon import IconThread

class MainWindow(QMainWindow):
	def __init__(self, app : QApplication):
		super().__init__()

		self.app = app
		self.__createTrayIcon()
		
		loadUi('ui/MainWindow.ui', self)
		self.show()

	def closeEvent(self, event):
		QMessageBox.information(self, 'App Tray Behavior', 'The app will minimize to the system tray when you close it', QMessageBox.StandardButton.Ok)
		event.ignore()
		self.hide()

	def __createTrayIcon(self):
		menu = (MenuItem("Show", self.__TrayShow), MenuItem("Exit", self.__TrayExit))
		image = Image.open('resources/logo512.png')
		icon = IconThread('Macro Recorder Python', icon=image, menu=menu)
		icon.start()

	def __TrayShow(self, icon, item):
		self.show()

	def __TrayExit(self, icon, item):
		self.app.quit()