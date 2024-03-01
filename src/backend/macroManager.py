from logging import Manager
from backend.simpleActionListener import SimpleActionListener
from backend.simpleMacroPlayer import SimpleMacroPlayer
from src.backend.keystrokeNotifier import KeystrokeNotifier
from typing import Callable, final
from enum import Enum, auto
from threading import Lock

class __ManagerState(Enum):
    RECORDING = auto()
    PLAYING = auto()
    REFRESH = auto() # REDUNDANT FOR THE MOMENT 
    IDLE = auto()
    
class MacroManager():
    def __init__(self) -> None:        
        self.__keystrokenotifier = KeystrokeNotifier(self.__keyStrokeCallback)
        self.__keystrokenotifier.start()
        
        self.__recorder = SimpleActionListener(self.__actionParser)
        self.__actionsRecorded = []
        
        self.__macros = {}
        
        self.__state = __ManagerState.IDLE
        
        self.__lock = Lock()
                
    def startRecording(self, onRecordingFinishedCallback: Callable) -> None:
        if self.__lock.acquire(blocking=False):
            self.__setState(__ManagerState.RECORDING)
            self.__actionsRecorded.clear()
            self.__recorder.start(lambda: (self.__lock.release(), self.__setState(__ManagerState.IDLE)))
    
    def stopRecording(self) -> None:
        self.__recorder.stop()
        # TODO maybe do something with the whole data thing huh?
        
    def refresh(self, macros: dict[str, SimpleMacroPlayer]) -> bool:
        if self.__lock.acquire(blocking=False):
            self.__macros = macros.copy()
            self.__lock.release()
            return True
        return False
    
    def startPlaying(self, macro: SimpleMacroPlayer):
        if self.__lock.acquire(blocking=False):
            self.__state = __ManagerState.PLAYING
            macro.play(lambda: (self.__lock.release, self.__setState(__ManagerState.IDLE)))
        
    def __keyStrokeCallback(self, pressedKeys: list[str]):
        pressedString = ''.join(pressedKeys)
        match self.__state:
            case __ManagerState.IDLE:
                if not pressedString in self.__macros:
                    return
                
                self.startPlaying(self.__macros[pressedString])
                
                ## TODO what about start recording via shortcut?
                
            case __ManagerState.PLAYING:
                pass # TODO maybe cancel?
            case __ManagerState.RECORDING:
                pass # TODO check for "stop" keystroke
            case _:
                pass
    
    def __actionParser(self, action: str):
        self.__actionsRecorded.append(action)
        
    def __setState(self, state: __ManagerState):
        self.__state = state