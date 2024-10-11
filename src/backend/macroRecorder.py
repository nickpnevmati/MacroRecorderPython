import io
import threading
from collections.abc import Callable
from io import TextIOWrapper
import time
from PyQt5.QtCore import pyqtSignal
from pynput import keyboard, mouse
from pynput.mouse import Button

class MacroRecorder(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.file = io.StringIO()
        self.running = False
        self.time = time.time_ns()
        self.daemon = True

    def start(self, mouse_listener: bool = True, keyboard_listener: bool = True):
        if self.running:
            raise Exception("Recorder is already running, cannot re-instantiate")

        self.__init_listeners()

        if mouse_listener:
            self.mouseListener.start()
        if keyboard_listener:
            self.keyboardListener.start()

        self.running = True
    
    def stop(self):
        self.mouseListener.stop()
        self.keyboardListener.stop()
        # must join to ensure thread have stopped
        self.keyboardListener.join()
        self.mouseListener.join()
        self.running = False
    
    def __init_listeners(self):
        self.mouseListener = mouse.Listener(on_click=self.__handle_mouse_click,
                                            on_move=self.__handle_mouse_move,
                                            on_scroll=self.__handle_mouse_scroll)
        
        self.keyboardListener = keyboard.Listener(on_press=self.__handle_key_press,
                                                  on_release=self.__handle_key_release)
    
    def __handle_key_press(self, key) -> None:
        self.__write_file(f'keypress {key}')

    def __handle_key_release(self, key) -> None:
        self.__write_file(f'keypress {key}')

    def __handle_mouse_move(self, x: int, y: int) -> None:
        self.__write_file(f'mousemove {x} {y}')

    def __handle_mouse_click(self, x: int, y: int, button: Button, pressed: bool) -> None:
        action = 'mouseclick' if pressed else 'mouserelease'
        self.__write_file(f'{action} {x} {y} {button}')

    def __handle_mouse_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        self.__write_file(f'mousescroll {x} {y} {dx} {dy}')
    
    def __write_file(self, data:str) -> None:
        self.file.write(f"{data} {self.__ns_since_last_action()}")
        
    def __ns_since_last_action(self) -> int:
        dtime = time.time_ns() - self.time
        self.time = time.time_ns()
        return dtime