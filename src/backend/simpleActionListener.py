from io import TextIOWrapper
import time
from pynput import keyboard, mouse
from pynput.mouse import Button
from typing import Callable, Any

class SimpleActionListener():
    """
    Calls the parser every time an event is captured by the listeners
    
    The event data is a string formatted like so: {action} {args} {deltaTime}
    
    Actions - Args:
        keypress {key}\n
        keyrelease {key}\n
        mousemove {x} {y}\n
        mouseclick {x} {y} {button}\n
        mouserelease {x} {y} {button}\n
        mousescroll {x} {y} {dx} {dy}
    """
    def __init__(self, parser: Callable[[Any], Any]) -> None:
        self.parser = parser
        self.ran = False
        self.time = time.time_ns()

    def start(self, mouseListener: bool = True, keyboardListener: bool = True):
        """
        Initializes Keyboard & Mouse listeners and starts them
        """
        self.__initListeners()

        self.time = time.time_ns()
        if mouseListener:
            self.mouseListener.start()
        if keyboardListener:
            self.keyboardListener.start()
    
    
    def stop(self):
        """
        This calls *stop* on the listeners
        """
        self.mouseListener.stop()
        self.keyboardListener.stop()
    
    def __initListeners(self):
        self.mouseListener = mouse.Listener(
            on_click=self.__handleMouseClick,
            on_move=self.__handleMouseMove, 
            on_scroll=self.__handleMouseScroll
        )
        
        self.keyboardListener = keyboard.Listener(
            on_press=self.__handleKeyPress,
            on_release=self.__handleKeyRelease
        )
    
    def __handleKeyPress(self, key) -> None:
        self.__passActionData(f'keypress {str(self.__keyToString(key)).strip('\'')}')

    def __handleKeyRelease(self, key) -> None:
        self.__passActionData(f'keyrelease {str(self.__keyToString(key)).strip('\'')}')

    def __handleMouseMove(self, x: int, y: int) -> (bool | None):
        self.__passActionData(f'mousemove {x} {y}')

    def __handleMouseClick(self, x: int, y: int, button: Button, pressed: bool) -> (bool | None):
        action = 'mouseclick' if pressed else 'mouserelease'
        self.__passActionData(f'{action} {x} {y} {button.name}')

    def __handleMouseScroll(self, x: int, y: int, dx: int, dy: int) -> (bool | None):
        self.__passActionData(f'mousescroll {x} {y} {dx} {dy}')
    
    def __passActionData(self, data:str) -> None:
        self.parser(f'{data} {self.__nsSinceLastAction()}')
        
    def __nsSinceLastAction(self) -> int:
        dtime = time.time_ns() - self.time
        self.time = time.time_ns()
        return dtime
        
    def __keyToString(self, key) -> str | None:
        if type(key) is str:
            return key
        elif type(key) is keyboard.Key:
            return key.name
        elif type(key) is keyboard.KeyCode:
            return key.char