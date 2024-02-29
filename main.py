import sys
import faulthandler
from PyQt5.QtWidgets import QApplication
from src.frontend.mainWindow import MainWindow

def main():
    faulthandler.enable()
    # TODO start icon thread here
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
    
if __name__ == '__main__':
   	main()
