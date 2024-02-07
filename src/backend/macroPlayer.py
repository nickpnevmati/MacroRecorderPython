from pynput.mouse import Button, Controller as mouseController
from pynput.keyboard import Key, Controller as keyboardController

class MacroPlayer():
    def __init__(self) -> None:
        self.mouse = mouseController()
        self.keyboard = keyboardController()
        # TODO load actions so we have them ready for execution

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass