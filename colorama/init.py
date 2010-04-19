import sys

from .ansitowin32 import AnsiToWin32

def init():
    if sys.platform.startswith('win'):
        if not isinstance(sys.stdout, AnsiToWin32):
            sys.stdout = AnsiToWin32(sys.stdout)
        if not isinstance(sys.stderr, AnsiToWin32):
            sys.stderr = AnsiToWin32(sys.stderr)

