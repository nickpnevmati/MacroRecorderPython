from ast import Call, MatchSingleton
from genericpath import isfile
from io import StringIO
from pynput.keyboard._base import Key, KeyCode
from src.backend.macroPlayer import MacroPlayer
from src.backend.macroRecorder import MacroRecorder
import pathlib
import re
import json
from typing import Callable
from pynput.keyboard import Listener
import threading
import enum
import os

class __ShortcutListener():
    def __init__(self, notify: Callable[[list[str]], None], onStop: Callable) -> None:
        self.keyLock: threading.Lock = threading.Lock()
        self.keys: list = list()
        
        self.onStop = onStop
        
        self.notifyLock = threading.Lock()
        self.notifyLock.acquire(blocking=True)
        self.notify: Callable[[list[str]], None] = notify
        
        self.listener = Listener(on_press=self.__onPress, on_release=self.__onRelease)
        self.listener.start()
    
    def start(self):
        self.notifyLock.release()
        self.notify(self.keys)
    
    def stop(self):
        self.onStop()
        
    def __onPress(self, key):
        with self.keyLock:
            self.keys.append(key)
            keys = self.keys.copy()
            
            # Only 1 source may call "notify" at a time, this may cause dropped events
            if not self.notifyLock.acquire(blocking=False):
                return
            try:
                self.notify(keys)
            finally:
                self.notifyLock.release()
    
    def __onRelease(self, key):
        with self.keyLock:
            self.keys.remove(key)
            
class __ManagerState(enum.Enum):
    IDLE = enum.auto()
    RECORDING = enum.auto()
    PLAYING = enum.auto()

class MacroManager():
    def __init__(self) -> None:
        self.__macroFilePath: str = '' #TODO 1 actually set the path for the macros
        self.__macros: dict[tuple, MacroPlayer] = dict()
        self.__shortcutListener: __ShortcutListener = __ShortcutListener(self.__checkShortcuts, self.__lock.release)
        self.__lock = threading.Lock()
        self.__stringIO = StringIO()
        self.__recorder: MacroRecorder = MacroRecorder(self.__stringIO)
        self.__shortcutListener.start()
        self.__state = __ManagerState.IDLE

    def loadMacros(self):
        if self.__state != __ManagerState.IDLE:
            # TODO raise exception
            return
        
        self.__macros.clear()
        
        macroFileFolder = '' # TODO 1 figure this out
        macroFilePath = pathlib.Path(macroFileFolder)
        for item in macroFilePath.iterdir():
            if not item.is_file() or re.match(r".*.macro", item.name):
                continue
            
            self.__parseMacroFile(macroFileFolder + os.path.pathsep + item.name)
        
            
    def __parseMacroFile(self, filename: str) -> None:        
        fp = open(filename, 'r')
        macro = json.load(fp)
        mSettings = macro['settings'] # NOTE redundant for now but may use later
        mShortcut = mSettings['shortcut']
        
        if mShortcut in self.__macros:
            # TODO 2 raise some exception of whatever
            return
        
        mActions: list[str]= macro['actions']
        
        # I dispise myself for writting the code that forced me to do this
        actionsFile = StringIO()
        for action in mActions:
            actionsFile.write(action + "\n")
        
        macroPlayerObject = MacroPlayer(actionsFile, self.__onMacroStop)
        
        self.__macros[mShortcut, macroPlayerObject]
    
    def __checkShortcuts(self, keysDown: list[str]) -> None:
        if len(keysDown) == 0:
            return
        
        match self.__state:
            case __ManagerState.IDLE:
                self.__checkTriggers(keysDown)
            case __ManagerState.PLAYING:
                pass # NOTE Maybe cancellation goes here
            case __ManagerState.RECORDING:
                self.__checkRecordingStop(keysDown)
            case _:
                pass

    def __checkTriggers(self, keysDown: list[str]):
        for macro in self.__macros.keys():
            if not all(key in keysDown for key in macro):
                continue
            
            if self.__state == __ManagerState.IDLE:
                self.__state = __ManagerState.PLAYING
                self.__macros[macro].start()
        # TODO 4 what about start recording?
    
    def __checkRecordingStop(self, keysDown: list[str]):
        pass # TODO
    
    def __onMacroStop(self):
        self.__state = __ManagerState.IDLE