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


def init(autoreset=False, wrap=None):

    if autoreset==True and wrap==False:
        raise ValueError('autoreset=True conflicts with wrap=False')

    if wrap is None:
        wrap = sys.platform.startswith('win') or autoreset

    if wrap:
        sys.stdout = AnsiToWin32(orig_stdout, autoreset=autoreset)
        sys.stderr = AnsiToWin32(orig_stderr, autoreset=autoreset)
    else:
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr

