from backend.keystrokeNotifier import KeystrokeNotifier


class MacroManager():
    def __init__(self) -> None:
        self.__keystrokenotifier = KeystrokeNotifier(self.__keyStrokeCallback)
        
    def __keyStrokeCallback(self, keys: list[str]):
        pass