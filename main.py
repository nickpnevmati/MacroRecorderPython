# from src.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
from src.mainWindow import MainWindow
from src.logger import logger
import sys

def main():
	logger.info('App start')
	app = QApplication(sys.argv)
	w = MainWindow(app)
	app.exec()

if __name__ == '__main__':
   	main()