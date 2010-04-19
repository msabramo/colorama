
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

    ANSI_RE = re.compile('\033\[(\d+)m')

    def __init__(self, wrapped, autoreset=False):
        self.wrapped = wrapped
        self.autoreset = autoreset
        self.enabled = sys.platform.startswith('win')

    def __getattr__( self, name ):
        return getattr( self.wrapped, name )

    def write( self, text ):
        if self.enabled:
            self.write_and_convert( text )
        else:
            self.wrapped.write( text )

        if self.autoreset:
            # but call win32 directly, don't convert this
            self.write_and_convert( Ansi.RESET_ALL )

    def write_and_convert(self, text):
        cursor = 0
        for match in self.ANSI_RE.finditer(text):
            # write regular text up to next ANSI sequence
            start, end = match.span()
            if cursor < start:
                snippet = text[cursor:start]
                self.wrapped.write( snippet )
            cursor = end

            # convert ANSI sequence to win32 calls
            ansi_code = int(match.group(1))
            if ansi_code in win32_calls:
                win32_calls[ansi_code]()
        if cursor < len(text) - 1:
            self.wrapped.write( text[cursor:] )



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

# from winbase.h
STD_OUTPUT_HANDLE= -11
HANDLE = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


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


    @property
    def combined_attrs(self):
        fg = self._fore + self._intense_fore * INTENSE
        bg = self._back + self._intense_back * INTENSE
        return fg + bg * 16


    def set_text_attr(self):
        success = windll.kernel32.SetConsoleTextAttribute(
            HANDLE, self.combined_attrs)
        assert success


    def get_current_attr(self):
        """
        Returns the character attributes (colors) of the console screen buffer.
        """
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        windll.kernel32.GetConsoleScreenBufferInfo( HANDLE, byref(csbi) )
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

