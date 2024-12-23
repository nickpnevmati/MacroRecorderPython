from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from src.ui.mainWindow import MainWindow
from src.logger import logger
import sys

from src.qtTrayIcon import SystemTrayIcon

def main():
    logger.info('App start')
    app = QApplication(sys.argv)
    w = MainWindow(app)

    tray_icon = SystemTrayIcon(QIcon("resources/logo512.png"), w)
    tray_icon.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()