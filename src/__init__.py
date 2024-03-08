import sys
from os import getenv
from pathlib import Path


# yoinked & modified from https://github.com/SwagLyrics/SwagLyrics-For-Spotify/blob/master/swaglyrics/__init__.py#L8-L32
# create unsupported.txt in os specific user directory
# doc: https://github.com/ActiveState/appdirs/blob/master/appdirs.py#L44 derivative
def __user_data_dir() -> Path:
    r"""
    Get OS specific data directory path for SwagLyrics.

    Typical user data directories are:
        macOS:    ~/Library/Application Support/SwagLyrics
        Unix:     ~/.local/share/SwagLyrics   # or in $XDG_DATA_HOME, if defined
        Win 10:   C:\Users\<username>\AppData\Local\SwagLyrics
    For Unix, we follow the XDG spec and support $XDG_DATA_HOME if defined.
    :param file_name: file to be fetched from the data dir
    :return: full path to the user-specific data dir
    """
    # get os specific path
    if sys.platform.startswith("win"):
        os_path = getenv("LOCALAPPDATA")
    else:
        # linux
        os_path = "~/.local/share"

    if os_path is None:
        raise Exception('Data Path Not Found')
    
    path = (Path(os_path) / "MacroRecorderPython").expanduser()
    
    __create_dir(path)
    __create_dir(path / 'macros')
    if not Path.exists(path / 'prefs.json'):
        Path.touch(path / 'prefs.json')
        
    return path

def __create_dir(path: Path):
    if not Path.exists(path):
        Path.mkdir(path)
        
app_data_path = __user_data_dir()