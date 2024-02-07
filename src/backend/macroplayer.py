from pynput.mouse import Button, Controller as mouseController
from pynput.keyboard import Key, Controller as keyboardController

class MacroPlayer():
    def __init__(self) -> None:
        self.mouse = mouseController()
        self.keyboard = keyboardController()

        # # Move the self.mouse to a position on the screen
        # self.mouse.position = (100, 150)

        # # Click the left self.mouse button
        # self.mouse.click(Button.left, 1)

        # # Type out a string
        # self.keyboard.type('Hello, world!')

        # # Press and release a single key
        # self.keyboard.press(Key.enter)
        # self.keyboard.release(Key.enter)

        # # Perform a combination of key presses
        # with self.keyboard.pressed(Key.ctrl):
        #     self.keyboard.press('c')
        #     self.keyboard.release('c')