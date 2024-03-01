from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from src.frontend.mainWindow import MainWindow

class TrayIcon():
    def __init__(self, app: QApplication, win: MainWindow):
        self.icon = QIcon('resources/logo512.png')
        self.tray = QSystemTrayIcon()
        self.menu = QMenu()
        
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)
        
        self.exitAction = QAction("Exit")
        self.showAction = QAction("Show")
        
        self.exitAction.triggered.connect(app.quit)
        self.showAction.triggered.connect(win.show)
        
        self.menu.addAction(self.exitAction)
        self.menu.addAction(self.showAction)
        
        self.tray.setContextMenu(self.menu)