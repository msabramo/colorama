import atexit
import sys

from .ansi import Style
from .ansitowin32 import AnsiToWin32


orig_stdout = sys.stdout
orig_stderr = sys.stderr


@atexit.register
def reset_all():
    AnsiToWin32(orig_stdout).write(Style.RESET_ALL)
    AnsiToWin32(orig_stderr).write(Style.RESET_ALL)


def init(autoreset=False, wrap=True):

    if autoreset==True and wrap==False:
        raise ValueError('autoreset=True conflicts with wrap=False')

    if (sys.platform.startswith('win') and wrap) or autoreset:
        sys.stdout = wrap_stream(sys.stdout, autoreset)
        sys.stderr = wrap_stream(sys.stderr, autoreset)
    else:
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr


def wrap_stream(stream, autoreset):
    if stream is orig_stdout or stream is orig_stderr:
        stream = AnsiToWin32(stream)
    stream.autoreset = autoreset
    return stream

