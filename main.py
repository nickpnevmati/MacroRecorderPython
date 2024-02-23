# from src.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
from src.frontend.mainwindow import Ui_MainWindow
import sys
from PyQt5 import QtWidgets
from src.frontend.TrayIcon import IconThread
from pystray import Icon, MenuItem
from PIL import Image

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__createTrayIcon()
        self.ui.minimizeOrCloseButton.clicked.connect(self.toggleTrayOnClose)
        
    def __createTrayIcon(self):
        menu = (MenuItem("Show", self.__TrayShow), MenuItem("Exit", self.__TrayExit))
        image = Image.open("resources/logo512.png")
        icon = IconThread(name="Macro Recorder Python", icon=image, menu=menu)
        icon.start()

    def __TrayShow(self, icon, item):
        self.show()

    def __TrayExit(self, icon, item):
        self.app.quit()
        
    def toggleTrayOnClose(self, clicked: bool):
        if clicked:
            pass # TODO
        else:
            pass # TODO

def main():
	app = QApplication(sys.argv)
	win = Window()
	win.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
   	main()