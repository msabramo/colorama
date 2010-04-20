import sys

from .ansitowin32 import AnsiToWin32

def init(autoreset=False):
    if sys.platform.startswith('win') or autoreset:
        sys.stdout = wrap(sys.stdout, autoreset)
        sys.stderr = wrap(sys.stderr, autoreset)

def wrap(stream, autoreset):
    real_stream = stream
    if isinstance(stream, AnsiToWin32):
        real_stream = stream.wrapped
    return AnsiToWin32(real_stream, autoreset=autoreset)

