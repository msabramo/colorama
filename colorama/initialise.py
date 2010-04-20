import sys

from .ansitowin32 import AnsiToWin32

def init(autoreset=False, wrap=True):

    if autoreset==True and wrap==False:
        raise ValueError('autoreset=True conflicts with wrap=False')

    if (sys.platform.startswith('win') and wrap) or autoreset:
        sys.stdout = wrap_stream(sys.stdout, autoreset)
        sys.stderr = wrap_stream(sys.stderr, autoreset)

def wrap_stream(stream, autoreset):
    real_stream = stream
    if isinstance(stream, AnsiToWin32):
        real_stream = stream.wrapped
    return AnsiToWin32(real_stream, autoreset=autoreset)

