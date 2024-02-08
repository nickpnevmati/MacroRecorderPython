from io import TextIOWrapper
from pynput.mouse import Button, Controller as mouseController
from pynput.keyboard import Key, Controller as keyboardController
import threading
from typing import Callable
from abc import ABCMeta, abstractmethod
import time

class Action():
    def __init__(self, runner: Callable, *args, **kwargs) -> None:
        self.__runner = runner
        self.__args = args
        self.__kwargs = kwargs

    def execute(self) -> None:
        self.__runner(*self.__args, **self.__kwargs)

class MacroPlayer():
    def __init__(self, macroFile: TextIOWrapper) -> None:
        self.__mouse = mouseController()
        self.__keyboard = keyboardController()
        self.__thread = threading.Thread(target=self.__worker)
        self.__stopEvent = threading.Event()
        self.__actions = self.__parseMacroFile(macroFile)
        self.__currentAction = 0

    def start(self) -> None:
        self.__thread.start()

    def stop(self) -> None:
        self.__stopEvent.set()

    def __worker(self) -> None:
        while self.__stopEvent.is_set() and self.__currentAction < len(self.__actions):
            self.__updateLoop()
        self.__currentAction = 0

    def __updateLoop(self) -> None:
        self.__actions[self.__currentAction].execute()
        self.__currentAction += 1
    
    def __playerSleep(self, seconds: int, interval: int):
        sleeps = seconds * 1000 / interval
        for i in range(sleeps):
            time.sleep(interval)
            if (self.__stopEvent.is_set()):
                break

    def __parseMacroFile(self, file: TextIOWrapper) -> list[Action]:
        # TODO parse preliminary data (like settings)
        actions: list[Action] = []
        for _, line in enumerate(file):
            kwrds = line.split(' ')
            match kwrds[0]:
                case 'wait':
                    actions.append(Action(self.__playerSleep, seconds=int(kwrds[1]), interval=int(kwrds[2]))) # NOTE maybe change this to be pulled from settings?
                case 'keypress':
                    actions.append(Action(self.__keyboard.press, key=kwrds[1]))
                case 'keyrelease':
                    actions.append(Action(self.__keyboard.release, key=kwrds[1]))
                case 'mousemove':
                    actions.append(Action(self.__mouse.move, dx=kwrds[1], dy=kwrds[2]))
                case 'mousebutton':
                    actions.append(Action(self.__mouse.move, dx=kwrds[1], dy=kwrds[2])) # NOTE this may be redundant in some cases, depends on how pynput works...
                    actions.append(Action(self.__mouse.press, button=kwrds[3]))
                case 'mousescroll':
                    actions.append(Action(self.__mouse.scroll, dx=kwrds[1], dy=kwrds[2]))
                case _:
                    pass

        return actions