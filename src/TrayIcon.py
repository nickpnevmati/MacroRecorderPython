import threading
from pystray import Icon

class IconThread(threading.Thread):
    def __init__(self, *icon_args, **icon_kwargs):
        self.icon = None
        self._icon_args = icon_args
        self._icon_kwargs = icon_kwargs

        threading.Thread.__init__(self, daemon=True)
    
    def __del__(self):
        self.stop()

    def run(self):
        self.icon = Icon(*self._icon_args, **self._icon_kwargs)
        self.icon.run()

    def stop(self):
        if self.icon:
            self.icon.stop()