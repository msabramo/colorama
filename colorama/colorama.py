
import sys
import re

class AnsiCode(object):
    RESET_ALL = 0
    BRIGHT = 1
    DIM = 2
    NORMAL = 22
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    DEFAULT = 39
    BLACK_BG = 40
    RED_BG = 41
    GREEN_BG = 42
    YELLOW_BG = 43
    BLUE_BG = 44
    MAGENTA_BG = 45
    CYAN_BG = 46
    WHITE_BG = 47
    DEFAULT_BG = 49

CSI = '\033['
ESCAPE = CSI + '%dm'

class Ansi(object):
    pass

for name in dir(AnsiCode):
    if not name.startswith('_'):
        code = getattr(AnsiCode, name)
        setattr(Ansi, name, ESCAPE % (code,))


class ColorStream(object):

    def __init__(self, wrapped):
        self.wrapped = wrapped

    def write(self, text):
        if sys.platform.startswith('win'):
            for snippet in ansi_to_win32(text):
                self.wrapped.write(snippet)
        else:
            self.wrapped.write(text)
            self.wrapped.write(Ansi.RESET_ALL)

    def __getattr__(self, name):
        return getattr(self.wrapped, name)


def wrap(stream):
    return ColorStream(stream)


ansi_re = re.compile('\033\[(\d+)m')

def ansi_to_win32(text):
    """
    yield the snippets of text between ansi codes
    for each ansi code encountered, make win32 calls to approximate it
    """
    start = 0
    for match in ansi_re.finditer(text):
        # yield the next snippet of text
        span = match.span()
        if span[0] > start:
            yield text[start:span[0]]
        start = span[1]

        # convert ANSI codes from match into win32 calls
        ansi_code = int(match.group(1))
        if ansi_code in win32_calls:
            win32_calls[ansi_code]()

    yield text[start:]


# from winbase.h
STD_OUTPUT_HANDLE= -11

from ctypes import Structure, c_short, c_ushort, byref, windll

SHORT = c_short
WORD = c_ushort

class COORD(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("X", SHORT),
    ("Y", SHORT)]

class SMALL_RECT(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("Left", SHORT),
    ("Top", SHORT),
    ("Right", SHORT),
    ("Bottom", SHORT)]

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("dwSize", COORD),
    ("dwCursorPosition", COORD),
    ("wAttributes", WORD),
    ("srWindow", SMALL_RECT),
    ("dwMaximumWindowSize", COORD)]


std_out_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


# from wincon.h
BLACK     = 0x0000
BLUE      = 0x0001
GREEN     = 0x0002
CYAN      = 0x0003
RED       = 0x0004
MAGENTA   = 0x0005
YELLOW    = 0x0006
GREY      = 0x0007
INTENSE   = 0x0008


class MsWinTerm(object):

    def __init__(self):
        self._default_fore = GREY
        self._default_back = BLACK
        self.reset()


    def reset(self):
        self._fore = self._default_fore
        self._back = self._default_back
        self._intense_fore = True
        self._intense_back = False

    def reset_all(self):
        self.reset()
        self.set_text_attr()


    def fore(self, color=None):
        if color is None:
            color = self._default_fore
        self._fore = color
        self.set_text_attr()

    def back(self, color=None):
        if color is None:
            color = self._default_back
        self._back = color
        self.set_text_attr()

    def dim(self):
        self._intense_fore = False
        self._intense_back = False
        self.set_text_attr()

    def normal(self):
        self._intense_fore = True
        self._intense_back = False
        self.set_text_attr()

    def bright(self):
        self._intense_fore = True
        self._intense_back = True
        self.set_text_attr()


    def get_text_attr(self):
        fg = self._fore + self._intense_fore * INTENSE
        bg = self._back + self._intense_back * INTENSE
        return fg + bg * 16


    def set_text_attr(self):
        attr = self.get_text_attr()
        success = windll.kernel32.SetConsoleTextAttribute(std_out_handle, attr)
        assert success


    def get_current_attr(self):
        """
        Returns the character attributes (colors) of the console screen buffer.
        """
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        windll.kernel32.GetConsoleScreenBufferInfo(
            std_out_handle, byref(csbi))
        return csbi.wAttributes

winterm = MsWinTerm()

win32_calls = {
    AnsiCode.RESET_ALL: winterm.reset_all,
    AnsiCode.BRIGHT: winterm.bright,
    AnsiCode.DIM: winterm.dim,
    AnsiCode.NORMAL: winterm.normal,
    AnsiCode.BLACK: lambda: winterm.fore(BLACK),
    AnsiCode.RED: lambda: winterm.fore(RED),
    AnsiCode.GREEN: lambda: winterm.fore(GREEN),
    AnsiCode.YELLOW: lambda: winterm.fore(YELLOW),
    AnsiCode.BLUE: lambda: winterm.fore(BLUE),
    AnsiCode.MAGENTA: lambda: winterm.fore(MAGENTA),
    AnsiCode.CYAN: lambda: winterm.fore(CYAN),
    AnsiCode.WHITE: lambda: winterm.fore(GREY),
    AnsiCode.DEFAULT: winterm.fore,
    AnsiCode.BLACK_BG: lambda: winterm.back(BLACK),
    AnsiCode.RED_BG: lambda: winterm.back(RED),
    AnsiCode.GREEN_BG: lambda: winterm.back(GREEN),
    AnsiCode.YELLOW_BG: lambda: winterm.back(YELLOW),
    AnsiCode.BLUE_BG: lambda: winterm.back(BLUE),
    AnsiCode.MAGENTA_BG: lambda: winterm.back(MAGENTA),
    AnsiCode.CYAN_BG: lambda: winterm.back(CYAN),
    AnsiCode.WHITE_BG: lambda: winterm.back(GREY),
    AnsiCode.DEFAULT_BG: winterm.back,
}

