import atexit
import os
from pathlib import Path
import sys
import faulthandler
from PyQt5.QtWidgets import QApplication
from src.frontend.trayIcon import TrayIcon
from src.frontend.mainWindow import MainWindow
from src.connectionLayer import ConnectionLayer
import src

def ensureSingleInstance():
    """
    Ensured the existance of only one instance of the app using a file as a "lock"
    """
    lockFile = src.app_data_path / '~instance.lock'
    if Path.exists(lockFile):
        exit(1)
    Path.touch(lockFile)
    atexit.register(func=lambda : os.remove(lockFile))

def main():
    faulthandler.enable()
    ensureSingleInstance()
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    win = MainWindow()
    tray = TrayIcon(app, win) # Must keep references here otherwise they gets garbage collected :) kill me
    connectionLayer = ConnectionLayer(win)
    win.show()
    app.exec()
    
if __name__ == '__main__':
   	main()
