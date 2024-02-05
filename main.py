from src.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

def main():
	app = QApplication(sys.argv)
	w = MainWindow(app)
	app.exec()

if __name__ == '__main__':
   	main()