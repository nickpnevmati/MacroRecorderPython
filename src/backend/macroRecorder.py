import threading
import time
from typing import Callable
from pynput import keyboard, mouse
from pynput.mouse import Button
from src.logger import logger

class MacroRecorder:
    def __init__(self, on_stop_callback: Callable[[list[str]], None]) -> None:
        self.__on_stop_callback = on_stop_callback
        self.__lock = threading.Lock()
        self.__data: list[str] = []
        self.__running = False
        self.__time = None

    def start(self):
        logger.info('Recorder Started')
        self.__time = time.time_ns()
        self.__running = True
        self.__init_listeners()
        self.mouseListener.start()
        self.keyboardListener.start()

    def stop(self):
        if not self.__running:
            return
        with self.__lock:
            self.__running = False
        self.mouseListener.stop()
        self.keyboardListener.stop()
        self.__on_stop_callback(self.__fix_data())

    def __fix_data(self) -> list[str]:
        return self.__data # TODO

    def __init_listeners(self):
        self.mouseListener = mouse.Listener(
            on_click=self.__handle_mouse_click,
            on_move=self.__handle_mouse_move,
            on_scroll=self.__handle_mouse_scroll
        )
        
        self.keyboardListener = keyboard.Listener(
            on_press=self.__handle_key_press,
            on_release=self.__handle_key_release
        )
    
    def __handle_key_press(self, key) -> None:
        with self.__lock:
            self.__write_data(f'keypress {key}')

    def __handle_key_release(self, key) -> None:
        with self.__lock:
            self.__write_data(f'keyrelease {key}')

    def __handle_mouse_move(self, x: int, y: int) -> None:
        with self.__lock:
            self.__write_data(f'mousemove {x} {y}')

    def __handle_mouse_click(self, x: int, y: int, button: Button, pressed: bool) -> None:
        with self.__lock:
            action = 'mouseclick' if pressed else 'mouserelease'
            self.__write_data(f'{action} {x} {y} {button}')

    def __handle_mouse_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        with self.__lock:
            self.__write_data(f'mousescroll {x} {y} {dx} {dy}')
    
    def __write_data(self, data:str) -> None:
        if self.__running:
            self.__data.append(f"{data} {self.__ns_since_last_action()}")
        
    def __ns_since_last_action(self) -> int:
        dtime = time.time_ns() - self.__time
        self.__time = time.time_ns()
        return dtime