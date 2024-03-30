from PyQt5 import QtWidgets
from src.frontend.ui.uimainwindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__onMinimizeOnCloseToggled(False)
        self.ui.minimizeOnCloseToggle.setChecked(False)
        self.ui.minimizeOnCloseToggle.toggled.connect(lambda value : self.__onMinimizeOnCloseToggled(value))
        
    def __onMinimizeOnCloseToggled(self, value: bool):
        app = QtWidgets.QApplication.instance()
        if app is None:
            raise Exception('Application not found')
        else:
            if isinstance(app, QtWidgets.QApplication):
                # The instance is a QApplication, so we can set the property
                app.setQuitOnLastWindowClosed(not value)
                print(f'Set quit on last window closed to {value}')
            else:
                # The instance is not a QApplication, handle accordingly
                print("Current instance is not a QApplication.")