import sys
import faulthandler
from PyQt5.QtWidgets import QApplication
from src.frontend.trayIcon import TrayIcon
from src.frontend.mainWindow import MainWindow

def main():
    faulthandler.enable()
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    win = MainWindow()
    
    _ = TrayIcon(app, win) # Must keep reference here otherwise it gets garbage collected :) 
    win.show()
    app.exec()
    
if __name__ == '__main__':
   	main()
