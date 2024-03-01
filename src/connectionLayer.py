from src.backend.macroManager import MacroManager

class ConnectionLayer():
    def __init__(self) -> None:
        self.manager = MacroManager()
    
    def refresh(self) -> None:
        pass