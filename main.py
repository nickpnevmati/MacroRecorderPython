# from src.MainWindow import MainWindow
from src.Application import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

def main():
	app = QApplication(sys.argv)
	w = MainWindow(app)
	app.exec()

if __name__ == '__main__':
   	main()