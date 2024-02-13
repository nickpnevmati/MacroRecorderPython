from pynput import keyboard, mouse
from pynput.mouse import Button
from abc import ABC, abstractmethod

class AbstractMacroEncoder(ABC):
    @abstractmethod
    def handleKeyPress(self, key) -> None:
        pass

    @abstractmethod
    def handleKeyRelease(self, key) -> None:
        pass

    @abstractmethod
    def handleMouseMove(self, x: int, y: int) -> (bool | None):
        pass

    @abstractmethod
    def handleMouseClick(self, x: int, y: int, button: Button, pressed: bool) -> (bool | None):
        pass

    @abstractmethod
    def handleMouseScroll(self, x: int, y: int, dx: int, dy: int) -> (bool | None):
        pass

class MacroRecorder():
    def __init__(self, handler: AbstractMacroEncoder) -> None:
        self.handler = handler
        self.running = False

    def start(self, mouseListener: bool = True, keyboardListener: bool = True):
        if self.running:
            raise Exception("Recorder is already running, cannot re-instantiate")
        
        self.__initListeners()

        if mouseListener:
            self.mouseListener.start()
        if keyboardListener:
            self.keyboardListener.start()
            
        self.running = True
    
    def stop(self):
        self.mouseListener.stop()
        self.keyboardListener.stop()
        self.running = False
    
    def __initListeners(self):
        self.mouseListener = mouse.Listener(on_click=self.handler.handleMouseClick, 
                                            on_move=self.handler.handleMouseMove, 
                                            on_scroll=self.handler.handleMouseScroll)
        
        self.keyboardListener = keyboard.Listener(on_press=self.handler.handleKeyPress,
                                               on_release=self.handler.handleKeyRelease)