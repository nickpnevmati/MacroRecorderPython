from io import TextIOWrapper
import time
from pynput import keyboard, mouse
from pynput.mouse import Button

class MacroRecorder():
    def __init__(self, filePointer: TextIOWrapper) -> None:
        self.file = filePointer
        self.running = False
        self.time = time.time_ns()

    def start(self, mouseListener: bool = True, keyboardListener: bool = True):
        if self.running:
            raise Exception("Recorder is already running, cannot re-instantiate")
        
        self.__initListeners()

        # if mouseListener:
        #     self.mouseListener.start()
        if keyboardListener:
            self.keyboardListener.start()
            
        self.running = True
    
    def stop(self):
        # self.mouseListener.stop()
        self.keyboardListener.stop()
        # must join to ensure thread have stopped
        self.keyboardListener.join()
        self.mouseListener.join()
        self.running = False
    
    def __initListeners(self):
        self.mouseListener = mouse.Listener(on_click=self.__handleMouseClick, 
                                            on_move=self.__handleMouseMove, 
                                            on_scroll=self.__handleMouseScroll)
        
        self.keyboardListener = keyboard.Listener(on_press=self.__handleKeyPress,
                                               on_release=self.__handleKeyRelease)
    
    def __handleKeyPress(self, key) -> None:
        self.__writeFile(f'keypress {key}')

    def __handleKeyRelease(self, key) -> None:
        self.__writeFile(f'keypress {key}')

    def __handleMouseMove(self, x: int, y: int) -> (bool | None):
        self.__writeFile(f'mousemove {x} {y}')

    def __handleMouseClick(self, x: int, y: int, button: Button, pressed: bool) -> (bool | None):
        action = 'mouseclick' if pressed else 'mouserelease'
        self.__writeFile(f'{action} {x} {y} {button}')

    def __handleMouseScroll(self, x: int, y: int, dx: int, dy: int) -> (bool | None):
        self.__writeFile(f'mousescroll {x} {y} {dx} {dy}')
    
    def __writeFile(self, data:str) -> None:
        self.file.write(f'{data} {self.__nsSinceLastAction()}\n')
        
    def __nsSinceLastAction(self) -> int:
        dtime = time.time_ns() - self.time
        self.time = time.time_ns()
        return dtime