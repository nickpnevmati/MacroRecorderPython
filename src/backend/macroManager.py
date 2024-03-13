from logging import Manager
from src.backend.simpleActionListener import SimpleActionListener
from src.backend.simpleMacroPlayer import SimpleMacroPlayer
from src.backend.keystrokeNotifier import KeystrokeNotifier
from typing import Callable, final
from enum import Enum, auto
from threading import Lock

class _ManagerState(Enum):
    RECORDING = auto()
    PLAYING = auto()
    REFRESH = auto() # REDUNDANT FOR THE MOMENT 
    IDLE = auto()
    
class RecorderSettings():    
    def __init__(self, captureMouseMovement: bool = True) -> None:
        self.captureMouseMovement = captureMouseMovement
    
class MacroManager():
    def __init__(self) -> None:
        self.__keystrokenotifier = KeystrokeNotifier(self.__keyStrokeCallback)
        
        self.__recorder = SimpleActionListener(self.__actionParser)
        self.__actionsRecorded = []
        
        self.__macros = {}
        
        self.__state = _ManagerState.IDLE
        
        self.__lock = Lock()
        
        self.__keystrokenotifier.start()
                
    def startRecording(self, onRecordingFinishedCallback: Callable, settings: RecorderSettings = RecorderSettings()) -> None:
        if self.__lock.acquire(blocking=False):
            self.__setState(_ManagerState.RECORDING)
            
            self.__actionsRecorded.clear()
            
            self.__recorder.start(lambda: (
                self.__lock.release(), 
                self.__setState(_ManagerState.IDLE), 
                onRecordingFinishedCallback(),
                ))
    
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
            self.__state = _ManagerState.PLAYING
            macro.play(lambda: (self.__lock.release, self.__setState(_ManagerState.IDLE)))
            
    def getActions(self) -> dict:
        return { 'actions' : self.__actionsRecorded.copy() }
        
    def __keyStrokeCallback(self, pressedKeys: list[str]):
        pressedString = ''.join(pressedKeys)
        match self.__state:
            case _ManagerState.IDLE:
                if not pressedString in self.__macros:
                    return
                
                self.startPlaying(self.__macros[pressedString])
                
                ## TODO what about start recording via shortcut?
                
            case _ManagerState.PLAYING:
                pass # TODO maybe cancel?
            case _ManagerState.RECORDING:
                if pressedString == "ctrlb":
                    self.__recorder.stop()
                    # TODO
            case _:
                pass
    
    def __actionParser(self, action: str):
        self.__actionsRecorded.append(action)
        
    def __setState(self, state: _ManagerState):
        self.__state = state