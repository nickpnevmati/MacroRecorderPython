from PyQt5.QtWidgets import (
	QApplication,
	QMainWindow,
	QMessageBox,
	QCheckBox
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
		
		self.win = loadUi('ui/MainWindow.ui', self)
		self.show()

	def closeEvent(self, event):
		if self.win.findChild(QCheckBox, 'minimizeOrCloseButton').isChecked():
			event.ignore()
			self.hide()
		else:	
			self.app.quit


	def __createTrayIcon(self):
		menu = (MenuItem("Show", self.__TrayShow), MenuItem("Exit", self.__TrayExit))
		image = Image.open('resources/logo512.png')
		icon = IconThread(name='Macro Recorder Python', icon=image, menu=menu)
		icon.start()

	def __TrayShow(self, icon, item):
		self.show()

	def __TrayExit(self, icon, item):
		self.app.quit()