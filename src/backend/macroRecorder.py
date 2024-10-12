import io
import threading
import time
from typing import Callable
from pynput import keyboard, mouse
from pynput.mouse import Button

class MacroRecorder(threading.Thread):
    def __init__(self, lock: threading.Lock, on_stop_callback: Callable) -> None:
        super().__init__()
        self.daemon = True
        self.__data = io.StringIO()
        self.__time = None
        self.__lock = lock
        self.__running = True
        self.__init_listeners()
        self.__on_stop_callback = on_stop_callback
        self.start()

    def run(self):
        self.mouseListener.start()
        self.keyboardListener.start()
        self.__time = time.time_ns()
        while self.__running:
            with self.__lock:
                continue

        self.mouseListener.stop()
        self.keyboardListener.stop()

        self.mouseListener.join()
        self.keyboardListener.join()
        self.__on_stop_callback()
        print("recorder stopped")

    def recorder_stop(self):
        return_data = None
        with self.__lock:
            self.__running = False
            return_data = self.__data
        return return_data
    
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
            self.__write_file(f'keypress {key}')

    def __handle_key_release(self, key) -> None:
        with self.__lock:
            self.__write_file(f'keypress {key}')

    def __handle_mouse_move(self, x: int, y: int) -> None:
        with self.__lock:
            self.__write_file(f'mousemove {x} {y}')

    def __handle_mouse_click(self, x: int, y: int, button: Button, pressed: bool) -> None:
        with self.__lock:
            action = 'mouseclick' if pressed else 'mouserelease'
            self.__write_file(f'{action} {x} {y} {button}')

    def __handle_mouse_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        with self.__lock:
            self.__write_file(f'mousescroll {x} {y} {dx} {dy}')
    
    def __write_file(self, data:str) -> None:
        self.__data.write(f"{data} {self.__ns_since_last_action()}")
        
    def __ns_since_last_action(self) -> int:
        dtime = time.time_ns() - self.__time
        self.__time = time.time_ns()
        return dtime