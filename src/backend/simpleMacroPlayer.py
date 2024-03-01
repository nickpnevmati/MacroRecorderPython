from io import TextIOWrapper
from pynput.mouse import Button, Controller as mouseController
from pynput.keyboard import KeyCode, Controller as keyboardController
import threading
from typing import Any, Callable
import time
import re

class SimpleMacroPlayer():
    """
    The event data is a string formatted like so: {action} {args} {deltaTime}
    
    Actions - Args:
        keypress {key}\n
        keyrelease {key}\n
        mousemove {x} {y}\n
        mouseclick {x} {y} {button}\n
        mouserelease {x} {y} {button}\n
        mousescroll {x} {y} {dx} {dy}
    """
    def __init__(self, actions: list[str]) -> None:
        self.__mouse = mouseController()
        self.__keyboard = keyboardController()
        self.__actions = self.__parseActions(actions)
        
    def __parseActions(self, actions: list[str]) -> list[tuple[Callable, Any, int]]:
        retList = []
        
        for action in actions:
            kwds = action.split()
            
            actionType = kwds[0]
            dtime = int(kwds[len(kwds) - 1])
                        
            match actionType:
                case 'keypress':
                    retList.append((self.__keyboard.press, {'key' : kwds[1]}, dtime))
                case 'keyrelease':
                    retList.append((self.__keyboard.release, {'key' : kwds[1]}, dtime))
                case 'mousemove':
                    retList.append((self.__mouseMove, {'position': (int(kwds[1]), int(kwds[2]))}, dtime))
                case 'mouseclick':
                    retList.append((self.__mouseMove, {'position': (int(kwds[1]), int(kwds[2]))}, dtime))
                    retList.append((self.__mouse.press, {'button': Button[kwds[3]]}, 0))
                case 'mouserelease':
                    retList.append((self.__mouseMove, {'position': (int(kwds[1]), int(kwds[2]))}, dtime))
                    retList.append((self.__mouse.release, {'button': Button[kwds[3]]}, 0))
                case 'mousescroll':
                    retList.append((self.__mouseMove, {'dx': int(kwds[1]), 'dy': int(kwds[2])}, dtime))
                    retList.append((self.__mouse.scroll, {'dx': int(kwds[3]), 'dy': int(kwds[4])}, 0))
                case _:
                    raise Exception('Invalid action type')
        return retList
    
    def __mouseMove(self, position: tuple[int, int]):
        self.__mouse.position = position
    
    def play(self, onCompleteCallback: Callable):
        for action in self.__actions:
            function = action[0]
            kwargs = action[1]
            dtime = action[2]
            
            if dtime > 0:
                time.sleep(dtime / 10**9)
            
            # TODO check this and maybe the cancellation goes here
            
            function(**kwargs)
            
        onCompleteCallback()