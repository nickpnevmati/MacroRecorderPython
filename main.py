import sys
import faulthandler
from PyQt5.QtWidgets import QApplication
from src.frontend.trayIcon import TrayIcon
from src.frontend.mainWindow import MainWindow
from src.connectionLayer import ConnectionLayer

def main():
    faulthandler.enable()
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    win = MainWindow()
    tray = TrayIcon(app, win) # Must keep references here otherwise they gets garbage collected :) kill me
    connectionLayer = ConnectionLayer(win)
    win.show()
    app.exec()
    
if __name__ == '__main__':
   	main()
