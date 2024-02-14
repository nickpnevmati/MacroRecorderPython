from io import TextIOWrapper
from typing_extensions import deprecated
from pynput.mouse import Button, Controller as mouseController
from pynput.keyboard import Key, KeyCode, Controller as keyboardController
import threading
from typing import Callable
from abc import ABCMeta, abstractmethod
import time

class Action():
    def __init__(self, runner: Callable, time:int, *args, **kwargs) -> None:
        self.__runner = runner
        self.time = time
        self.__args = args
        self.__kwargs = kwargs

    def execute(self) -> None:
        time.sleep(self.time / 10**9)
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
        
    def join(self) -> None:
        if self.__thread.is_alive():
            self.__thread.join()

    def stop(self) -> None:
        self.__stopEvent.set()

    def __worker(self) -> None:
        while not self.__stopEvent.is_set() and self.__currentAction < len(self.__actions):
            self.__updateLoop()
        self.__currentAction = 0
        self.__stopEvent.clear()

    def __updateLoop(self) -> None:
        self.__actions[self.__currentAction].execute()
        self.__currentAction += 1
    
    # NOTE this is completely redundant
    def __playerSleep(self, seconds: int, interval: int):
        sleeps = seconds * 1000 / interval
        for i in range(round(sleeps)):
            time.sleep(interval)
            if (self.__stopEvent.is_set()):
                break

    def __parseMacroFile(self, file: TextIOWrapper) -> list[Action]:
        # TODO parse preliminary data (like settings)
        actions: list[Action] = []
        for _, line in enumerate(file):
            kwrds = line.strip('\n').replace('\'', '').split(' ')
            match kwrds[0]:
                case 'wait': # NOTE this is currently un-used, the way the events are recorded makes this redundant
                    actions.append(Action(self.__playerSleep, time=int(kwrds[len(kwrds)-1]), seconds=int(kwrds[1]), interval=int(kwrds[2]))) # NOTE maybe change this to be pulled from settings?
                case 'keypress':
                    actions.append(Action(self.__keyboard.press, time=int(kwrds[len(kwrds)-1]), key=KeyCode.from_char(kwrds[1])))
                case 'keyrelease':
                    actions.append(Action(self.__keyboard.release, time=int(kwrds[len(kwrds)-1]), key=KeyCode.from_char(kwrds[1])))
                case 'mousemove':
                    actions.append(Action(self.__mouse.move, time=int(kwrds[len(kwrds)-1]), dx=int(kwrds[1]), dy=int(kwrds[2])))
                case 'mousepress':
                    actions.append(Action(self.__mouse.move, time=int(kwrds[len(kwrds)-1]), dx=int(kwrds[1]), dy=int(kwrds[2])))
                    actions.append(Action(self.__mouse.press, time=int(kwrds[len(kwrds)-1]), button=kwrds[3]))
                case 'mouserelease':
                    actions.append(Action(self.__mouse.move, time=int(kwrds[len(kwrds)-1]), dx=int(kwrds[1]), dy=int(kwrds[2])))
                    actions.append(Action(self.__mouse.release, time=int(kwrds[len(kwrds)-1]), button=Button(kwrds[3])))
                case 'mousescroll':
                    actions.append(Action(self.__mouse.scroll, time=int(kwrds[len(kwrds)-1]), dx=int(kwrds[1]), dy=int(kwrds[2])))
                case _:
                    pass

        return actions