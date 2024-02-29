import platform
import threading
from pystray import Icon

class IconThread():
    def __init__(self):
        if platform.uname().system == 'Linux':
            pass #TODO
        elif platform.uname().system == 'Windows':
            pass #TODO