from typing import Callable
import threading
from pynput.keyboard import Listener 

class KeystrokeNotifier():
    """
    This class starts a keyboard listener and calls the "notify" callback every time a key is pressed
    
    Notify is passed a list of all the keys that are currently pressed
    """
    def __init__(self, notify: Callable[[list[str]], None]) -> None:
        self.keyLock: threading.Lock = threading.Lock()
        self.keys: list = list()
        
        self.notifyLock = threading.Lock()
        self.notifyLock.acquire(blocking=True)
        self.notify: Callable[[list[str]], None] = notify
        
        self.listener = Listener(on_press=self.__onPress, on_release=self.__onRelease)
        self.listener.start()
    
    def start(self):
        self.notifyLock.release()
        self.notify(self.keys)
    
    def stop(self):
        self.notifyLock.acquire(blocking=True)
        
    def __onPress(self, key):
        with self.keyLock:
            self.keys.append(key)
            
            if not self.notifyLock.acquire(blocking=False):
                return
            try:
                self.notify(self.keys.copy())
            finally:
                    self.notifyLock.release()
    
    def __onRelease(self, key):
        with self.keyLock:
            self.keys.remove(key)