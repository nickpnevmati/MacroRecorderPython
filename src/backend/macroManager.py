from logging import Manager
from backend.simpleActionListener import SimpleActionListener
from backend.simpleMacroPlayer import SimpleMacroPlayer
from src.backend.keystrokeNotifier import KeystrokeNotifier
from typing import Callable
from enum import Enum, auto

class __ManagerState(Enum):
    RECORDING = auto()
    PLAYING = auto()
    IDLE = auto()
    
class MacroManager():
    def __init__(self) -> None:        
        self.__keystrokenotifier = KeystrokeNotifier(self.__keyStrokeCallback)
        self.__keystrokenotifier.start()
        
        self.__recorder = SimpleActionListener(self.__actionParser)
        self.__actionsRecorded = []
        
        self.__macros = {}
        
        self.__state = __ManagerState.IDLE
                
    def startRecording(self, onRecordingFinishedCallback: Callable) -> None:
        if not self.__setStateRecording():
            return
        
        self.__actionsRecorded.clear()
        self.__recorder.start()
    
    def stopRecording(self) -> None:
        self.__recorder.stop()
        # TODO do something with the recording lmao
        self.__resetStateToIdle()
        
    def refresh(self) -> None:
        pass # TODO foreach macro file, load macro and do the necessary checks
    
    def startPlaying(self, macro: SimpleMacroPlayer):
        if not self.__setStatePlaying():
            return
        
        macro.play(self.__resetStateToIdle)
        
    def __keyStrokeCallback(self, pressedKeys: list[str]):
        match self.__state:
            case __ManagerState.IDLE:
                pass # TODO check for macro shortcuts
            case __ManagerState.PLAYING:
                pass # TODO maybe cancel?
            case __ManagerState.RECORDING:
                pass # TODO check for "stop" keystroke
            case _:
                pass
    
    def __actionParser(self, action: str):
        self.__actionsRecorded.append(action)
        
    def __setStateRecording(self) -> bool:
        if self.__state is not __ManagerState.IDLE:
            return False
        self.__state = __ManagerState.RECORDING
        return True
    
    def __setStatePlaying(self) -> bool:
        if self.__state is not __ManagerState.IDLE:
            return False
        self.__state = __ManagerState.PLAYING
        return True
        
    def __resetStateToIdle(self) -> None:
        self.__state = __ManagerState.IDLE