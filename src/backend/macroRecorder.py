from pynput import keyboard, mouse
from pynput.mouse import Button
from abc import ABCMeta, abstractmethod
import time

class AbstractMacroEncoder(ABCMeta):
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
    def __init__(self) -> None:
        self.running = False
        self.keyboard = keyboard
        self.mouse = mouse
        self.hasReleased=True

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
        self.running = False
    
    def __initListeners(self):
        # self.mouseListener = mouse.Listener(on_click=self.handleMouseClick, 
        #                                     on_move=self.handleMouseMove, 
        #                                     on_scroll=self.handleMouseScroll)
        
        self.keyboardListener = keyboard.Listener(on_press=self.handleKeyPress,
                                               on_release=self.handleKeyRelease)

    def handleKeyPress(self, key):
        if self.hasReleased:
            self.hasReleased=False
            print('You pressed the %s key' %key)    
            self.timer = time.perf_counter()

    def handleKeyRelease(self, key):
        self.hasReleased = True
        print(f'You released the {key} key after {(time.perf_counter() - self.timer): .5f} seconds')    
                                               